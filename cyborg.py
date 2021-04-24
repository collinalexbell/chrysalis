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
import direct.task


class Memory:
    def __init__(self, memory_description):
        self.description = memory_description
        self.when = time.time()

    def __repr__(self):
        return f"{self.description} at {self.when}"

class Cyborg(DirectObject):

    def __init__(self):
        self.y = -100
        self.x = 0
        self.z = 0
        self.is_memoizing = False
        self.camera_rotation = 0
        self.accept("w", self.up)
        self.accept("s", self.down)
        self.accept("a", self.strafe_left)
        self.accept("d", self.strafe_right)
        self.accept("q", self.left)
        self.accept("e", self.right)
        self.accept("v", self.chrysalate)
        self.accept("m", self.start_memoizations)
        self.accept("n", self.stop_memoizations)
        self.accept("p", self.play_memoization)
        self.memory = []
        print(taskMgr)

        self.LightsOn = False
        self.LightsOn1 = False
        slight = Spotlight('slight')
        slight.setColor((1, 1, 1, 1))
        lens = PerspectiveLens()
        slight.setLens(lens)
        self.slnp = render.attachNewNode(slight)
        self.slnp1 = render.attachNewNode(slight)

    def memoize_movement(self, movement):
        if(self.is_memoizing):
            self.memory.append(Memory(movement))
            print(self.memory)

    def start_memoizations(self):
        self.is_memoizing = True 
        self.memory = []

    def stop_memoizations(self):
        self.is_memoizing = False

    def get_fn_from_description(self, des):
        if(des == "left"):
            print("left")
            return self.left
        elif (des == "right"):
            print("right")
            return self.right
        elif (des == "strafe_left"):
            print("strafe_left")
            return self.strafe_left
        elif (des == "strafe_right"):
            print("strafe_right")
            return self.strafe_right
        elif (des == "up"):
            print("up")
            return self.up
        elif (des == "down"):
            print("down")
            return self.down


    def play_memoization(self):
        cur_time = time.time()
        first_memory = self.memory[0]

        for index, cur_memory in enumerate(self.memory[1:]):
            fn = self.get_fn_from_description(cur_memory.description)
            sleep_time = cur_memory.when - first_memory.when
            print(sleep_time)
            taskMgr.doMethodLater(sleep_time, fn, str(cur_memory), extraArgs=[])

    def left(self):
        self.camera_rotation = self.camera_rotation + 10
        base.camera.setHpr(self.camera_rotation, 0, 0)
        self.memoize_movement("left")

    def right(self):
        self.camera_rotation = self.camera_rotation - 10
        base.camera.setHpr(self.camera_rotation, 0, 0)
        self.memoize_movement("right")

    def up(self):
        self.y = self.y + 10
        base.camera.setPos(self.x, self.y, self.z)
        self.memoize_movement("up")
        
    def down(self):
        self.y = self.y - 10
        base.camera.setPos(self.x, self.y, self.z)
        self.memoize_movement("down")
        
    def strafe_left(self):
        self.x = self.x - 10
        base.camera.setPos(self.x, self.y, self.z)
        self.memoize_movement("strafe_left")

    def strafe_right(self):
        self.x = self.x + 10
        base.camera.setPos(self.x, self.y, self.z)
        self.memoize_movement("strafe_right")

    def chrysalate(self):
        brick = Voxel(self.x, self.y, self.z)
        brick = render.attachNewNode(brick.get_panda_render_node())
        # OpenGl by default only draws "front faces" (polygons whose vertices are specified CCW).
        # I may want to get rid of this if not needed
        brick.setTwoSided(True)

