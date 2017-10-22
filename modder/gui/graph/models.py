# coding: utf-8
from functools import partial

import numpy as N
import wx

from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas.Utilities import BBox


class MovingObjectMixin:
    """
    Methods required for a Moving object
    """

    def GetOutlinePoints(self):
        BB = self.BoundingBox
        OutlinePoints = N.array(
            (
                (BB[0, 0], BB[0, 1]),
                (BB[0, 0], BB[1, 1]),
                (BB[1, 0], BB[1, 1]),
                (BB[1, 0], BB[0, 1]),
            )
        )

        return OutlinePoints


class ConnectorObjectMixin:
    """
    Mixin class for DrawObjects that can be connected with lines

    Note that this versionony works for Objects that have an "XY" attribute:
      that is, one that is derived from XHObjectMixin.
    """

    def GetConnectPoint(self, other=None):
        return self.XY


class CanvasMixin(object):
    def __init__(self, *args, **kwargs):
        self._CanvasSet = False

    def SetupCanvasMixin(self):
        wx.CallAfter(self._SetupCanvasMixin)

    def _SetupCanvasMixin(self):
        if not self._CanvasSet:
            self.Moving = False

            self.Canvas.Bind(FC.EVT_MOTION, self.OnMove)
            self.Canvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp)

            self.Canvas.ZoomToBB()

    def ObjectHit(self, object):
        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoords
            self.MovingObject = object

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        and moves the object it is clicked on
        """
        if self.Moving:
            # Draw the Moving Object:
            self.MovingObject.Move(event.Coords - self.StartPoint)
            self.StartPoint = event.Coords
            self.Canvas.Draw(True)

    def OnLeftUp(self, event):
        if self.Moving:
            self.Moving = False


class Block(FC.Rectangle, MovingObjectMixin, ConnectorObjectMixin):
    """
    Block Object that can be moved
    """
    def __init__(
        self, XY, WH, Text,
        LineColor='BlockBorderColor', LineStyle='Transparent', LineWidth=4,
        FillColor='BlockBackgroundColor', FillStyle='Solid',
        InForeground=False, FontFamily='Monaco'
    ):
        self.__LineWidth = LineWidth
        self.__LineColor = LineColor
        self.__LineStyle = LineStyle
        self.__FillColor = FillColor
        self.__FillStyle = FillStyle

        self.Text = Text
        self.__Font = wx.Font(
            wx.FontInfo(18).FaceName(FontFamily).Family(wx.FONTFAMILY_SCRIPT)
        )
        if not self.__Font.IsOk():
            self.__Font = wx.Font(wx.FontInfo(18))
            print('Font fallbacked')

        FC.Rectangle.__init__(
            self, XY, WH,
            LineColor=self.__LineColor, LineStyle=self.__LineStyle,
            LineWidth=self.__LineWidth, FillColor=self.__FillColor,
            FillStyle=self.__FillStyle, InForeground=False
        )

    def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
        super()._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc=HTdc)

        gc = wx.GraphicsContext.Create(dc)
        gc.SetFont(self.__Font, wx.TheColourDatabase.Find('TextColor'))

        # FIXME currently only support single line, no layout engine yet
        text_w, text_h = gc.GetTextExtent(self.Text)
        # print('text extent:', text_w, text_h)
        X, Y = WorldToPixel(self.XY)
        W, H = ScaleWorldToPixel(self.WH)
        # this is the top left point of the text
        text_x = X + self.__LineWidth + (W - self.__LineWidth * 2 - text_w) / 2
        text_y = Y + self.__LineWidth + (H - self.__LineWidth * 2 - text_h) / 2
        gc.DrawText(self.Text, text_x, text_y)

    def GetConnectPoint(self, other=None):
        x, y = self.XY
        w, h = self.WH
        center_x, center_y = (x + w / 2, y + h / 2)

        # Can't really tell
        if other is None:
            return (center_x, center_y)
        else:
            other_x = other.GetConnectPoint()[0]

            if other_x >= center_x:
                # other block is at the right side
                return x + w, center_y
            else:
                # other block is at the left side
                return x, center_y

    def OnHover(self, obj):
        self.SetLineStyle('Solid')
        self.SetLineColor('BlockHoverBorderColor')
        if self._Canvas:
            self._Canvas.Draw(True)

    def OffHover(self, obj):
        self.SetLineStyle(self.__LineStyle)
        self.SetLineColor(self.__LineColor)
        if self._Canvas:
            self._Canvas.Draw(True)


class ConnectorLine(FC.LineOnlyMixin, FC.DrawObject,):
    """
    A Line that connects two objects --
      it uses the objects to get its coordinates
    """
    # fixme: this should be added to the Main FloatCanvas Objects some day.
    def __init__(self, Object1, Object2,
                 LineColor="ConnectorLineColor", LineStyle="Solid",
                 LineWidth=4, InForeground=False):
        FC.DrawObject.__init__(self, InForeground=InForeground)

        self.Object1 = Object1
        self.Object2 = Object2
        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth

        self.CalcBoundingBox()
        self.SetPen(LineColor, LineStyle, LineWidth)

        self.HitLineWidth = max(LineWidth, self.MinHitLineWidth)

    def CalcBoundingBox(self):
        self.BoundingBox = BBox.fromPoints(
            (
                self.Object1.GetConnectPoint(self.Object2),
                self.Object2.GetConnectPoint(self.Object1)
            )
        )
        if self._Canvas:
            self._Canvas.BoundingBoxDirty = True

    def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
        p0 = self.Object1.GetConnectPoint(self.Object2)
        p3 = self.Object2.GetConnectPoint(self.Object1)

        # We'll use a dead simple way to get the two control points:
        # The control points p1 and p2 are on the lines
        # perpendicular to the borders through points p0 and p3.
        # That's said,
        # p1 is on the line perpendicular to the border through p0,
        # and p2 for p3.

        dx = p0[0] - p3[0]

        left_point, right_point = (p0, p3) if dx < 0 else (p3, p0)

        # dy = left_point[1] - right_point[1]

        dx_abs = N.abs(dx)
        # dy_abs = N.abs(dy)

        # p1_y = left_point[1] + dy_abs * .2 if dy > 0 else left_point[1] - dy_abs * .2
        # p2_y = right_point[1] - dy_abs * .2 if dy > 0 else right_point[1] + dy_abs * .2
        p1_y = left_point[1]
        p2_y = right_point[1]

        p1 = (left_point[0] + dx_abs * .4), p1_y
        p2 = (right_point[0] - dx_abs * .4), p2_y

        Points = N.array(
            (left_point, p1, p2, right_point)
        )
        Points = WorldToPixel(Points)
        dc.SetPen(self.Pen)
        # dc.DrawLines(Points)
        dc.DrawSpline(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            # HTdc.DrawLines(Points)
            HTdc.DrawSpline(Points)
