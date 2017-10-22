# coding: utf-8
def launch_gui():
    from .app import ModderGuiApp
    from .utils import load_colors

    modder = ModderGuiApp(False)
    load_colors()
    modder.MainLoop()
