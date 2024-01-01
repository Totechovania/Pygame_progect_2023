from FrameController import FrameController
from Frames.ButtonDemonstratinon import ButtonDemonstration
from utilities import apply_global_settings, set_shared_variables, terminate



if __name__ == '__main__':
    apply_global_settings()
    set_shared_variables()

    #main_menu = TestFrame(supposed_to_be='Пример работы с фреймами.') # Здесь должен быть фрейм, отвечающий за главное меню(или заставку).
    main_menu = ButtonDemonstration()

    controller = FrameController(main_menu)
    controller.run()

    terminate()
