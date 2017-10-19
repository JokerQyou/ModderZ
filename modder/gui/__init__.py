# coding: utf-8
def launch_gui():
    from .app import ModderGuiApp

    modder = ModderGuiApp(False)
    modder.MainLoop()
