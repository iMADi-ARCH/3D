from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setPos(-8, 42, 0)
        self.scene.setScale(0.25, 0.25, 0.25)

        # Actor
        self.panda = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.panda.setScale(0.005, 0.005, 0.005)
        self.panda.reparentTo(self.render)

        # Intervals
        posInterval1 = self.panda.posInterval(
            13,                              ## Time 
            Point3(0, -10, 0),              ## End Pos
            startPos=Point3(0, 10, 0)       ## Start Pos
        )
        posInterval2 = self.panda.posInterval(
            13, 
            Point3(0, 10, 0), 
            startPos=Point3(0, -10, 0)
        )
        hprInterval1 = self.panda.hprInterval(
            3, 
            Point3(180, 0, 0), 
            startHpr=Point3(0, 10, 0)
        )
        hprInterval2 = self.panda.hprInterval(
            3, 
            Point3(0, 0, 0), 
            startHpr=Point3(180, 0, 0)
        )

        # Pace
        self.pandapace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="PandaPace")
        self.pandapace.loop()

        # Animation
        self.panda.loop("walk")

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def spinCameraTask(self, task):
        angleDegrees = task.time * 60.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
app = MyApp()
app.run()