#################################################################################
# Copyright (C) 2023
# Juan Carlos Perez Castellanos <cuyopc@gmail.com>
# Maria Frine de la Rosa Gutierrez <frinedlr@gmail.com>
#
# This file is part of fvmouse.
#
# fvmouse can not be copied and/or distributed without the express
# permission of Juan Carlos Perez Castellanos or Maria Frine de la Rosa Gutierrez
##################################################################################

# !/usr/bin/env python3
"""
Voice commands detection, classification and execution
"""
import os
import sys
import signal
import time
import pyautogui
from edge_impulse_linux.audio import AudioImpulseRunner
import PySimpleGUI as gui
from pynput.mouse import Button, Controller

audio_runner = None
ENABLED = False
KILL = False
max_label = ''
VALIDATE = False
mouse = Controller()
last_mouse_action = None
last_mouse_position = None


def _signal_handler(sig, frame) -> None:
    """ Stop audio runner classifier gracefully on Ctrl + c"""
    if audio_runner:
        audio_runner.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, _signal_handler)


def get_model_file() -> str:
    """ Get model file name from first argument or default to optimized_model.eim """
    args = []
    if len(args) == 0:
        this_dir, _ = os.path.split(__file__)
        eim_file = os.path.join(this_dir, "data", "optimized_model.eim")
        args.append(eim_file)
    model = args[0]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    model_file = os.path.join(dir_path, model)
    return model_file


def setup_model_permissions(model_file) -> None:
    """ Ensure execution permissions are set for .eim file """
    os.system(f"chmod +x '{model_file}'")
    os.system(f"xattr -d com.apple.quarantine '{model_file}'")


def smooth_scroll(value, up=True) -> None:
    """ Emulate smooth scrolling """
    i = 0
    while i != value:
        if up:
            i += 5
        else:
            i -= 5
        pyautogui.scroll(i / 5)
        time.sleep(0.010)


def mouse_action(command, is_last=False) -> None:
    """ Perform given command as a mouse/keyboard action """
    global last_mouse_action
    global last_mouse_position
    command = command.lower()
    # If we are executing a last command, clear last_mouse_action
    # else if we are executing a normal command, store it in last_mouse_action
    if is_last:
        last_mouse_action = None
        last_mouse_position = None
    else:
        last_mouse_action = command
        last_mouse_position = pyautogui.position()
    if command == 'derecho':
        pyautogui.rightClick()
    elif command == 'click':
        pyautogui.leftClick()
    elif command == 'doble':
        mouse.click(Button.left, 2)
    elif command == 'arriba':
        smooth_scroll(25)
    elif command == 'abajo':
        smooth_scroll(-25, False)
    elif command == 'copiar':
        pyautogui.keyDown('command')
        pyautogui.press('c')
        pyautogui.keyUp('command')
    elif command == 'pegar':
        pyautogui.keyDown('command')
        pyautogui.press('v')
        pyautogui.keyUp('command')
    elif command == 'cortar':
        pyautogui.keyDown('command')
        pyautogui.press('x')
        pyautogui.keyUp('command')
    elif command == 'buscar':
        pyautogui.keyDown('command')
        pyautogui.press('f')
        pyautogui.keyUp('command')
    elif command == 'enter':
        pyautogui.press('enter')
    else:
        print("Command not available")


def validate_command() -> None:
    mouse_position = pyautogui.position()
    layout = [[gui.Text(f'Is {max_label} correct?', font=('Axial', 15))],
              [gui.Button('YES', key='Yes', font=('Axial', 13))],
              [gui.Text(f'(window will automatically close in 5 seconds)', font=('Axial', 10))]]
    window = gui.Window('Command Validation', layout, size=(260, 100), element_justification='c', finalize=True,
                        auto_close=5)
    event_key, _ = window.read()
    if event_key == 'Yes':
        # if the user selects yes in window
        window.close()
        # guardar el comando anterior y si es derecho, click, doble volverlo a hacer, borrar logica en siguientes lineas
        # double click before copy, cut or paste. Click before enter
        # if max_label in ['copiar', 'pegar', 'cortar']:
        #     mouse_action('doble')
        # elif max_label in ['enter']:
        #     mouse_action('click')
        # Run the last stored command when in validation to avoid having the
        # popup cancelling the action
        if last_mouse_action in ['doble', 'click', 'derecho']:
            if last_mouse_action != max_label:
                pyautogui.moveTo(last_mouse_position)
                mouse_action(last_mouse_action, is_last=True)
        pyautogui.moveTo(mouse_position)
        mouse_action(max_label)
    else:
        window.close()
        pyautogui.moveTo(mouse_position)


def classify_audio(model_file) -> None:
    """ Execute runner to classify audio and perform commands """
    delay_initial_time = time.time()
    global max_label, VALIDATE, ENABLED, KILL
    with AudioImpulseRunner(model_file) as runner:
        try:
            model_info = runner.init()
            # Retrieve labels from model file
            labels = model_info['model_parameters']['labels']
            print('Model parameters: ' + model_info['project']['owner'] + ' / ' + model_info['project']['name'])

            # Select audio device (default to 1)
            selected_device_id = 1

            results = dict()
            print(f"Available commands: {labels}")
            for res, audio in runner.classifier(device_id=selected_device_id):
                if KILL:
                    raise Exception
                if not ENABLED:
                    continue
                max_value = 0
                max_label = ''
                for label in labels:
                    results[label] = res['result']['classification'][label]
                    if results[label] > max_value:
                        max_value = results[label]
                        max_label = label
                if max_label and max_label not in ['noise', 'unknown'] and max_value > 0.75:
                    # Assume that commands have a separation of at least two seconds between them
                    # When time delta is less than 2 seconds -> Ignore and continue sampling, otherwise classify sample
                    if time.time() - delay_initial_time <= 2:
                        continue
                    elif max_label == 'abajo' and max_value > 0.88:
                        if max_value >= 0.96:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'arriba' and max_value > 0.90:
                        if max_value >= 0.95:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'copiar' and max_value > 0.85:
                        # mejor con volumen y audio alto
                        if max_value >= 0.99:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'cortar' and max_value > 0.895:
                        if max_value >= 0.977:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'derecho' and max_value > 0.84:
                        if max_value >= 0.90:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'doble' and max_value > 0.90:
                        if max_value >= 0.95:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'enter' and max_value > 0.85:
                        if max_value >= 0.97:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'pegar' and max_value > 0.85:
                        if max_value >= 0.95:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'click' and max_value > 0.95:
                        if max_value >= 0.99:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    elif max_label == 'buscar' and max_value > 0.80:  # checar
                        if max_value >= 0.90:
                            mouse_action(max_label)
                        else:
                            VALIDATE = True
                        print(f'{max_label} {max_value}')
                    delay_initial_time = time.time()
        except:
            pass
        finally:
            if runner:
                runner.stop()


def main() -> None:
    model_file = get_model_file()
    setup_model_permissions(model_file)
    classify_audio(model_file)


if __name__ == '__main__':
    main()
