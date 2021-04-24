#!/usr/bin/env python

# Author: kuberlog
# Date: 2021-04-21

# Derived from example by:
#    Kwasi Mensah (kmensah@andrew.cmu.edu)
#    copyright 2005-08-02
#    forked by Collin Bell on 2021-04-21

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import lookAt
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens
from panda3d.core import CardMaker
from panda3d.core import Light, Spotlight
from panda3d.core import TextNode
from panda3d.core import LVector3
import sys
import os
import voxel
from voxel import Voxel
import time
from cyborg import Cyborg

base = ShowBase()
base.disableMouse()
base.camera.setPos(0, -100, 0)


title = OnscreenText(text="Chrysalis OS",
                     style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
                     parent=base.a2dBottomRight, align=TextNode.ARight)
escapeEvent = OnscreenText(text="1): Load REaLSpaCE tm",
                           style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.08),
                           align=TextNode.ALeft, scale=.05,
                           parent=base.a2dTopLeft)
spaceEvent = OnscreenText(text="2): Load ChrysalisSpace",
                          style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.14),
                          align=TextNode.ALeft, scale=.05,
                          parent=base.a2dTopLeft)
upDownEvent = OnscreenText(text="3): LoadToggleSpace",
                           style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.20),
                           align=TextNode.ALeft, scale=.05,
                           parent=base.a2dTopLeft)



cubes = [Voxel(3,3,3), 
         Voxel(0,0,0),
         Voxel(-3, -3, -3),
         Voxel(3,-3,-3),
         Voxel(3,3,-3),
         Voxel(-3,3,-3),
         Voxel(3,-3,3),
         Voxel(-3,-3,3),
        ]
for _, cube in enumerate(cubes):
    cube = render.attachNewNode(cube.get_panda_render_node())
    # OpenGl by default only draws "front faces" (polygons whose vertices are specified CCW).
    # I may want to get rid of this if not needed
    cube.setTwoSided(True)

cyborg = Cyborg()
base.run()

