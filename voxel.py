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

# helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners

class Voxel:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def makeSquare(self, x1, y1, z1, x2, y2, z2, offset_point):
        # offset_point: tuple, gets transformed to Vector and then used to
        # translate the square
        format = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData('square', format, Geom.UHDynamic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        nx1 = x1
        ny1 = y1
        nz1 = z1
        nx2 = x2
        ny2 = y2
        nz2 = z2


        x1 = x1 + offset_point[0]
        y1 = y1 + offset_point[1] 
        z1 = z1 + offset_point[2]
        x2 = x2 + offset_point[0]
        y2 = y2 + offset_point[1]
        z2 = z2 + offset_point[2]

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
    def get_panda_render_node(self):
        square0 = self.makeSquare(-1, -1, -1, 1, -1, 1, (self.x, self.y, self.z))
        square1 = self.makeSquare(-1, 1, -1, 1, 1, 1,  (self.x, self.y, self.z))
        square2 = self.makeSquare(-1, 1, 1, 1, -1, 1,  (self.x, self.y, self.z))
        square3 = self.makeSquare(-1, 1, -1, 1, -1, -1,  (self.x, self.y, self.z))
        square4 = self.makeSquare(-1, -1, -1, -1, 1, 1,  (self.x, self.y, self.z))
        square5 = self.makeSquare(1, -1, -1, 1, 1, 1,  (self.x, self.y, self.z))
        cube_node = GeomNode('square')
        cube_node.addGeom(square0)
        cube_node.addGeom(square1)
        cube_node.addGeom(square2)
        cube_node.addGeom(square3)
        cube_node.addGeom(square4)
        cube_node.addGeom(square5)
        return cube_node

