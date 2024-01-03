from FrameController import FrameController
from utilities import apply_global_settings, set_shared_variables, terminate
from Frames.MainMenu import MainMenu
from Frames.TileTestFrame import TileTestFrame


if __name__ == '__main__':
    apply_global_settings()
    set_shared_variables()

    main_menu = TileTestFrame()

    controller = FrameController(main_menu)
    controller.run()

    terminate()
