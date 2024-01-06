from FrameController import FrameController
from utilities.change_settings import set_shared_variables  #, play_background_music
from utilities.system import terminate, apply_global_settings
from Frames.MainMenu import MainMenu
from Frames.FightFrame import FightFrame

if __name__ == '__main__':
    apply_global_settings()
    set_shared_variables()

    main_menu = FightFrame()
    #play_background_music("music.mp3")
    controller = FrameController(main_menu)
    controller.run()

    terminate()
