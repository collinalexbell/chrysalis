#!/usr/bin/env python

# Author: Collin Bell
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


base = ShowBase()
base.disableMouse()
base.camera.setPos(0, -10, 0)


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



# helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners

def makeSquare(x1, y1, z1, x2, y2, z2):
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)

        normal.addData3(LVector3(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1).normalize())
        normal.addData3(LVector3(2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1).normalize())
        normal.addData3(LVector3(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1).normalize())
        normal.addData3(LVector3(2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1).normalize())

        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)


    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)

        normal.addData3(LVector3(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1).normalize())
        normal.addData3(LVector3(2 * x2 - 1, 2 * y2 - 1, 2 * z1 - 1).normalize())
        normal.addData3(LVector3(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1).normalize())
        normal.addData3(LVector3(2 * x1 - 1, 2 * y1 - 1, 2 * z2 - 1).normalize())

        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

    def add_diff_colors():
        color.addData4f(1.0, 0.0, 0.0, 1.0)
        color.addData4f(0.0, 1.0, 0.0, 1.0)
        color.addData4f(0.0, 0.0, 1.0, 1.0)
        color.addData4f(1.0, 0.0, 1.0, 1.0)

    add_diff_colors()

    texcoord.addData2f(0.0, 1.0)
    texcoord.addData2f(0.0, 0.0)
    texcoord.addData2f(1.0, 0.0)
    texcoord.addData2f(1.0, 1.0)

    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = Geom(vdata)
    square.addPrimitive(tris)
    return square

# Note: it isn't particularly efficient to make every face as a separate Geom.
# instead, it would be better to create one Geom holding all of the faces.
def make_cube():
    square0 = makeSquare(-1, -1, -1, 1, -1, 1)
    square1 = makeSquare(-1, 1, -1, 1, 1, 1)
    square2 = makeSquare(-1, 1, 1, 1, -1, 1)
    square3 = makeSquare(-1, 1, -1, 1, -1, -1)
    square4 = makeSquare(-1, -1, -1, -1, 1, 1)
    square5 = makeSquare(1, -1, -1, 1, 1, 1)
    cube_node = GeomNode('square')
    cube_node.addGeom(square0)
    cube_node.addGeom(square1)
    cube_node.addGeom(square2)
    cube_node.addGeom(square3)
    cube_node.addGeom(square4)
    cube_node.addGeom(square5)
    return cube_node

cube_node = make_cube()
cube = render.attachNewNode(cube_node)

# OpenGl by default only draws "front faces" (polygons whose vertices are
# specified CCW).
cube.setTwoSided(True)


class ButtonCommandCenter(DirectObject):

    def __init__(self):
        self.testTexture = loader.loadTexture("maps/envir-reeds.png")
        self.accept("1", self.toggleTex)
        self.accept("2", self.toggleLightsSide)
        self.accept("3", self.toggleLightsUp)

        self.LightsOn = False
        self.LightsOn1 = False
        slight = Spotlight('slight')
        slight.setColor((1, 1, 1, 1))
        lens = PerspectiveLens()
        slight.setLens(lens)
        self.slnp = render.attachNewNode(slight)
        self.slnp1 = render.attachNewNode(slight)

    def toggleTex(self):
        global cube
        if cube.hasTexture():
            cube.setTextureOff(1)
        else:
            cube.setTexture(self.testTexture)

    def toggleLightsSide(self):
        global cube
        self.LightsOn = not self.LightsOn

        if self.LightsOn:
            render.setLight(self.slnp)
            self.slnp.setPos(cube, 10, -400, 0)
            self.slnp.lookAt(10, 0, 0)
        else:
            render.setLightOff(self.slnp)

    def toggleLightsUp(self):
        global cube
        self.LightsOn1 = not self.LightsOn1

        if self.LightsOn1:
            render.setLight(self.slnp1)
            self.slnp1.setPos(cube, 10, 0, 400)
            self.slnp1.lookAt(10, 0, 0)
        else:
            render.setLightOff(self.slnp1)

t = ButtonCommandCenter()
base.run()
