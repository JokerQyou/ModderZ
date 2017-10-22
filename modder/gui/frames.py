# coding: utf-8
import wx
from wx.lib.floatcanvas import FloatCanvas as FC

from modder import MOD_REGISTRY
from modder.gui.graph.models import Block, ConnectorLine, CanvasMixin


class ModManagerFrame(wx.Frame, CanvasMixin):

    def __init__(self):
        wx.Frame.__init__(
            self, None, -1, "FloatCanvas Graph Test", wx.DefaultPosition, (700, 700)
        )
        CanvasMixin.__init__(self)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetupUI()
        self.Center()

    def SetupLayout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.Canvas, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.ModList, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

    def SetupUI(self):
        self.Canvas = FC.FloatCanvas(
            self, -1, (500, 300),
            ProjectionFun=None,
            Debug=0,
            BackgroundColor='CanvasBackgoundColor'
        )

        self.ModList = wx.ListCtrl(
            self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_HRULES
        )
        self.ModList.InsertColumn(0, 'Name', format=wx.LIST_FORMAT_LEFT, width=200)
        self.ModList.InsertColumn(1, 'Events', format=wx.LIST_FORMAT_LEFT, width=200)
        # self.ModList.InsertColumn(2, 'File', format=wx.LIST_FORMAT_LEFT, width=100)

        blocks = []
        lines = []
        mods = {}

        for index, (eventname, modlist) in enumerate(MOD_REGISTRY.items()):
            event_blocks = filter(lambda o: o.Text == eventname, blocks)
            if not any(event_blocks):
                event_block = Block((0, index * 2), (6, 1), eventname)
                blocks.append(event_block)
            else:
                event_block = list(event_blocks)[0]

            for index, mod in enumerate(modlist):
                mod_name = mod.__doc__ or mod.__name__
                if not any(filter(lambda o: o.Text == mod_name, blocks)):
                    mod_block = Block((7, index * 2 - 1), (4, 1), mod_name)
                    lines.append(ConnectorLine(event_block, mod_block))
                    blocks.append(mod_block)
                if mod not in mods:
                    mods[mod] = [eventname]
                else:
                    mods[mod].append(eventname)

        for mod, events in mods.items():
            self.ModList.Append([mod.__doc__ or mod.__name__, ', '.join(events)])

        self.Canvas.AddObjects(lines)
        self.Canvas.AddObjects(blocks)
        for block in blocks:
            self.Canvas.AddObject(block)
            block.Bind(FC.EVT_FC_ENTER_OBJECT, block.OnHover)
            block.Bind(FC.EVT_FC_LEAVE_OBJECT, block.OffHover)
            block.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)

        self.SetupLayout()
        self.SetupCanvasMixin()

    def OnClose(self, evt):
        self.Hide()
