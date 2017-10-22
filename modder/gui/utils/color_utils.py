# coding: utf-8
import numpy as N
import wx


def load_colors(colors_conf=None):
    '''
    Load extra color definition into global wxPython color database
    by using CSS-like syntax
    '''
    default_colors = '''
ConnectorLineColor: rgba(109, 109, 109, 1);
CanvasBackgoundColor: rgba(36, 36, 36, 1);
BlockBackgroundColor: rgba(224, 224, 224, 1);
BlockBorderColor: rgba(224, 224, 224, 1);
BlockHoverBorderColor: rgba(113, 38, 171, 1);
TextColor: rgba(0, 0, 0, 1);
'''
    colors_conf = colors_conf or default_colors
    for line in colors_conf.strip().split(';'):
        line = line.strip()
        if not line:
            continue
        color_name, color_args = line.split(':')
        color_args = color_args\
            .replace('rgba(', '')\
            .replace(')', '')\
            .strip()\
            .split(',')

        # defaults to solid color
        if len(color_args) == 4:
            alpha = float(color_args.pop())
        elif len(color_args) == 3:
            alpha = 1
        else:
            raise ValueError('Color definition must contain 3 or 4 numbers')

        color_args = list(map(int, color_args))

        # normalize alpha value
        color_args = [N.clip(cv, 0, 255) for cv in color_args]
        alpha = N.clip(alpha * 255, 0, 255)

        # add color into database
        wx.TheColourDatabase.AddColour(
            color_name.strip(), wx.Colour(*color_args, alpha=alpha)
        )
