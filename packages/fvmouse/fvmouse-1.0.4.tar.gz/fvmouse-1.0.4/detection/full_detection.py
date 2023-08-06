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
import sys
import time

from detection import face_detection, voice_detection
from threading import Thread
import PySimpleGUI as gui

BUTTON_OFF = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
BUTTON_ON = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'
PLAY_ICON = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAAByElEQVRoge3ZMWsUQRjG8Z8RFSKCgoJp0qSJjVpoZ2clkk8g5CtYpU+TD5DSUkvbVCFNYiM2dhZqY6GFQooEISGai8Xu4HgmcnM3c+su+4fj2L2dmedhb+Z95x16enp6hljBxaZF5OAE7/GoaSGTchJ9tnCrWTnjE0zs19+HWMPlJkWNQzAyh2c4rq+/YBnnmpOWRjASuIfX0f0d3GlAVzLDRmBG9Ta+1r8d4wVuTFdaGqcZCVzFOn7Uz+ziKc5PR1oa/zISWMRm9OxbPCisK5lRjASW8Clqs4H5MrLSSTECs1jFQd3ue319KbewVFKNBBbwMmr/EY8z6kpmXCOBh3gX9dNYdjCpEbigWs326r6OVKvdlQn7TSKHkcCcKt4MNJAd5DQSuI83Ud87uJ15jL8oYYTf2cE3f2YH1wuMhXJGAtdU8+WnwtlBaSOBu3gVjZc9O5iWEapJ/wSf6zEHeI6bZzWYmY6u/4v+rzUirZ/snVh+hwPitpYFxNanKJ1IGk9L4xcz6Eom18bqg5ZtrDqx1Y2LDwPVG2lV8aH15aDWF+jOKpkWi8o5GKWIXTwq56BzxwqdOejpxNFbJw5DO3M83dPT02J+AbN50HbYDxzCAAAAAElFTkSuQmCC'
STOP_ICON = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAAAaklEQVRoge3ZQQqAMAxFwSre/8p6AZFUiXzKzLqLPNJVOwYAvLcVzpztU9Q8zrr/NUW3Y+JsZXsdSjdimY0ISSMkjZA0QtIISSMkjZA0QtIISSMkjZA0QtIISSMkzcxrfMo/ya1lNgIAX1zq+ANHUjXZuAAAAABJRU5ErkJggg=='


def start_detection() -> None:
    '''
    Parent process: full_detection.py
    Child processes: voice_detection.py, face_detection.py
    '''

    # Sends voice detection (non-blocking subprocess) to the background so that the parent process keeps running.
    thread_voice = Thread(target=voice_detection.main, args=(sys.argv[1:]))
    thread_voice.start()

    # Sends face detection (non-blocking subprocess) to the background so that the parent process keeps running.
    thread_face = Thread(target=face_detection.main)
    thread_face.start()

    # Activates on-screen buttons.
    gui_interface()

    # Stops current execution when voice and face detection modules exit.
    thread_voice.join()
    thread_face.join()


def gui_interface() -> None:
    """

    """
    # Define buttons layout.
    layout_audio_video = [[gui.Text('AUDIO OFF'),
                           gui.Button(image_data=BUTTON_OFF, key='Audio',
                                      button_color=(gui.theme_background_color(), gui.theme_background_color()),
                                      border_width=0, metadata=False),
                           gui.Text('AUDIO ON')],
                          [gui.Text('VIDEO OFF'),
                           gui.Button(image_data=BUTTON_OFF, key='Video',
                                      button_color=(gui.theme_background_color(), gui.theme_background_color()),
                                      border_width=0, metadata=False),
                           gui.Text('VIDEO ON')]
                          ]
    layout_play_stop = [[gui.Button(image_data=PLAY_ICON, key='Play', border_width=0, metadata=False,
                                    button_color=gui.theme_background_color()),
                         gui.Button(image_data=STOP_ICON, key='Stop', border_width=0, metadata=True,
                                    button_color=gui.theme_background_color()),
                         gui.Button('EXIT', key='exit', size=4, button_color='DarkRed')]
                        ]
    layout_config_validation = [[gui.Text('VALIDATION OF VOICE COMMANDS', font=('Axial', 12))],
                                [gui.Text('OFF'),
                                 gui.Button(image_data=BUTTON_OFF, key='Validation',
                                            button_color=(gui.theme_background_color(), gui.theme_background_color()),
                                            border_width=0, metadata=False),
                                 gui.Text('ON')]]

    # Display windows
    window_audio_video = gui.Window('Feature Configuration', layout_audio_video, no_titlebar=True,
                                    location=(1185, 137),
                                    size=(240, 125),
                                    element_justification='c', finalize=True)
    window_play_stop = gui.Window('Detection control', layout_play_stop, titlebar_font=('Axial', 12),
                                  location=(1223, 35),
                                  size=(202, 65),
                                  element_justification='c', finalize=True)
    window_config_audio_validation = gui.Window('Commands Validation', layout_config_validation, no_titlebar=True,
                                                location=(1185, 272),
                                                size=(240, 75),
                                                element_justification='c', finalize=True)
    window_config_audio_validation.hide()
    window_play_stop.hide()
    while True:  # Event Loop until break
        # Read events from windows
        window_name, event_key, values = gui.read_all_windows(timeout=150)
        if event_key == 'exit':
            print('exiting program')
            voice_detection.KILL = True
            face_detection.KILL = True
            window_audio_video.close()
            window_config_audio_validation.close()
            window_play_stop.close()
            exit()
        if window_audio_video['Audio'].metadata or window_audio_video['Video'].metadata:
            window_play_stop.un_hide()
        else:
            window_play_stop.hide()
        if (window_audio_video['Audio'].metadata == True) and (window_play_stop['Stop'].metadata == True):
            window_config_audio_validation.un_hide()
        else:
            window_config_audio_validation.hide()
        if window_config_audio_validation['Validation'].metadata == True:
            validation_activated = True
        else:
            validation_activated = False
        if window_name == window_play_stop and event_key in (gui.WIN_CLOSED, 'Exit'):
            exit(1)
        if event_key in (gui.WIN_CLOSED, 'Exit'):
            print('Exit program')
            break
        elif event_key == 'Audio':
            window_audio_video['Audio'].metadata = not window_audio_video['Audio'].metadata
            print(f"Audio Detection: {window_audio_video['Audio'].metadata}")
            window_audio_video['Audio'].update(
                image_data=BUTTON_ON if window_audio_video['Audio'].metadata else BUTTON_OFF)
            # window_config_validation.un_hide()
        elif event_key == 'Validation':
            window_config_audio_validation['Validation'].metadata = not window_config_audio_validation[
                'Validation'].metadata
            print(f"Audio Validation: {window_config_audio_validation['Validation'].metadata}")
            window_config_audio_validation['Validation'].update(
                image_data=BUTTON_ON if window_config_audio_validation['Validation'].metadata else BUTTON_OFF)
        elif event_key == 'Video':
            window_audio_video['Video'].metadata = not window_audio_video['Video'].metadata
            print(f"Face Tracking: {window_audio_video['Video'].metadata}")
            window_audio_video['Video'].update(
                image_data=BUTTON_ON if window_audio_video['Video'].metadata else BUTTON_OFF)
        elif event_key == 'Play':
            window_play_stop['Play'].metadata = True
            window_play_stop['Stop'].metadata = False
            window_play_stop['Play'].update(button_color=('white', '#2fa4e7'))
            # Close settings windows while the detection is running.
            window_audio_video.hide()
            print('Start Detection')
            if window_audio_video['Video'].metadata:
                if not face_detection.face_center_x:
                    face_detection.calibrate_offsets()
                face_detection.ENABLED = True
            if window_audio_video['Audio'].metadata:
                time.sleep(2)
                voice_detection.ENABLED = True
        elif event_key == 'Stop':
            window_play_stop['Play'].update(button_color=gui.theme_background_color())
            window_play_stop['Stop'].metadata = True
            window_play_stop['Play'].metadata = False
            print('Stop Detection')
            voice_detection.ENABLED = False
            face_detection.ENABLED = False
            # Open settings windows while the detection is running.
            window_audio_video.un_hide()
        if voice_detection.VALIDATE:
            if validation_activated:
                face_detection_status = face_detection.ENABLED
                face_detection.ENABLED = False
                voice_detection.ENABLED = False
                voice_detection.validate_command()
                voice_detection.VALIDATE = False
                voice_detection.ENABLED = True
                face_detection.ENABLED = face_detection_status
    window_audio_video.close()
    window_config_audio_validation.close()
    window_play_stop.close()


def main() -> None:
    try:
        start_detection()
    except:
        print("Exiting...")
        exit(1)


if __name__ == '__main__':
    main()
