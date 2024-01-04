from FrameController import FrameController
from utilities import apply_global_settings, set_shared_variables, terminate, play_background_music
from Frames.MainMenu import MainMenu


if __name__ == '__main__':
    apply_global_settings()
    set_shared_variables()

    main_menu = MainMenu()
    play_background_music("music.mp3")
    controller = FrameController(main_menu)
    controller.run()

    terminate()
