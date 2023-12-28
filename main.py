from FrameController import FrameController
from utilities import apply_global_settings, set_shared_variables, terminate
from Frames.TestFrame import TestFrame


if __name__ == '__main__':
    apply_global_settings()
    set_shared_variables()

    main_menu = TestFrame() # Здесь должен быть фрейм, отвечающий за главное меню(или заставку).

    controller = FrameController(main_menu)
    controller.run()

    terminate()
