from FrameController import FrameController
from Frames.MainMenu import MainMenu
from utilities import apply_global_settings, set_shared_variables, terminate
from Frames.TileTestFrame import TileTestFrame


if __name__ == '__main__':
    apply_global_settings()
    set_shared_variables()

    #main_menu = TestFrame(supposed_to_be='Пример работы с фреймами.') # Здесь должен быть фрейм, отвечающий за главное меню(или заставку).
    main_menu = MainMenu()

    controller = FrameController(main_menu)
    controller.run()

    terminate()
