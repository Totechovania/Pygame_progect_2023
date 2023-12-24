from FrameController import FrameController


if __name__ == '__main__':
    main_menu = MainMenu() # Здесь должен быть фрейм, отвечающий за главное меню(или заставку).

    controller = FrameController(main_menu)
    controller.run()

