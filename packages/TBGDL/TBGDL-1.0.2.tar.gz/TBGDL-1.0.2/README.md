# TBGDL
A Python library for creating text-based games.

# Features
tbgdl_print(text, color) - Like print but also adds the ability to color the text. Makes cool ASCII art too!

tbgdl_clear() - Clears the screen.

tbgdl_quit() - Quits the application.

tbgdl_getinput() - Gets user input.

tbgdl_new_scene(command1, command2, command3, command4, command5, command6, command7, command8, command9, command10) - Can only be used in a variable, else that scene can't be referenced anywhere else in your code. If you have empty spaces, replace them up to command10 with 0. tbgdl_getinput() cannot be used in this function.

tbgdl_load_scene(scene) - Loads the variable that you stored your scene in.

tbgdl_playsound(note, sound) - Make beeps with it. The notes need to be in a string, and the sound param is the duration of the beep. 

# Variables
default - The default color white. Can only be used when a function needs a color.

red - The color red. Can only be used when a function needs a color.

black - The color black. Can only be used when a function needs a color.

blue - The color blue. Can only be used when a function needs a color.

magenta - The color magenta. Can only be used when a function needs a color.

yellow - The color yellow. Can only be used when a function needs a color.

cyan - The color cyan. Can only be used when a function needs a color.

green - The color green. Can only be used when a function needs a color.

# Requirements

colorama - For tbgdl_print(text, color) command.

musicalbeeps - For tbgdl_playsound(note, sound) command.
