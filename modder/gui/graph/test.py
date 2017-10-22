#!/usr/bin/env python
"""

This is a small demo, showing how to make an object that can be moved around.

It also contains a simple prototype for a "Connector" object
  -- a line connecting two other objects

"""
import wx
from wx.lib.floatcanvas import FloatCanvas
from wx.lib.floatcanvas import FloatCanvas as FC

from .models import Block, ConnectorLine, CanvasMixin
from modder.gui.utils import load_colors


class DrawFrame(wx.Frame, CanvasMixin):
    """
    A simple frame used for the Demo
    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        CanvasMixin.__init__(self)

        self.CreateStatusBar()
        # Add the Canvas
        self.Canvas = FloatCanvas.FloatCanvas(
            self, -1, (500, 500),
            ProjectionFun=None,
            Debug=0,
            BackgroundColor='CanvasBackgoundColor'
        )

        blocks = []
        # create the bitmaps first
        for index, Point in enumerate([(1, 1), (-4, 3), (2, 3)]):
            block = Block(Point, (2, 1), '测试 block')

            if index > 0:
                self.Canvas.AddObject(ConnectorLine(blocks[index - 1], block))

            blocks.append(block)

        # then add them to the Canvas, so they are on top of the line
        for block in blocks:
            self.Canvas.AddObject(block)
            block.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)

        self.SetupCanvasMixin()
        self.Show(True)

        return None


if __name__ == "__main__":
    app = wx.App(0)
    load_colors()

    DrawFrame(
        None, -1, "FloatCanvas Graph Test", wx.DefaultPosition, (700, 700)
    )
    app.MainLoop()
