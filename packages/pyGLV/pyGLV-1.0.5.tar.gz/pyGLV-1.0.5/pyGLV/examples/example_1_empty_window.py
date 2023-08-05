"""
Running the basic RenderWindow with the concrete basic Compoment of the decorator
patter, that is the SDL2Window, without any decorator on top
"""

from pyGLV.GUI.Viewer import SDL2Window

gWindow = SDL2Window(openGLversion=4)
gWindow.init()



running = True
# MAIN RENDERING LOOP

while running:
    gWindow.display()
    running = gWindow.event_input_process(running)
    gWindow.display_post()
gWindow.shutdown()
