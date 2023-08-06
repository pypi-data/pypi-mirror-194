# fvmouse
fvmouse is a Python package that allows you to perform the tasks of a mouse via face recognition and/or some of the shortcuts of the keyboard using voice recognition.

## Installation
Run the install.sh file to install all dependencies and the fvmouse package.

## Usage
Run the exec file created after installation
Select voice and/or face recognition. If voice is activated, select if the validation of commands will be used, this will allow to ask the user wether a word that is between a range of probability but below a threshold of confidence is the correct word. 
Once the user activates the options desired, the button to start recognition should be selected. The recognition can be stoped with the pause button anytime. If the face recognition was selected for the first time after starting the exec, instructions will given for image calibration. Otherwise, it will use the previous calibration. 
If the recognition is stopped, the user can change the recognition options and start it again or simply close the program and that will delete the calibration records if available. 


## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
https://gitlab.com/don-charlie-pc/fvmouse

Please make sure to update tests as appropriate.


## License
```
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
```