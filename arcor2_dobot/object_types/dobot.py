from typing import Set, Optional, List
import atexit

from arcor2.object_types import Robot
from arcor2.data.common import Pose, ActionMetadata, Joint
from arcor2.data.object_type import Models
from arcor2.action import action
from arcor2.exceptions import Arcor2Exception
import arcor2.helpers as hlp

from pydobot import Dobot as PyDobot
from serial.tools import list_ports

# TODO pid as __init__ parameter?


class Dobot(Robot):
    """
    Dobot Magician.
    """

    def __init__(self, obj_id: str, pose: Pose, collision_model: Optional[Models] = None) -> None:

        super(Robot, self).__init__(obj_id, pose, collision_model)

        ports = list_ports.comports()  # from https://github.com/luismesas/pydobot/pull/21
        for thing in ports:
            if thing.vid == 6790 and thing.pid == 29987:
                port = thing.device
                break
        else:
            raise Arcor2Exception("Dobot not found!")

        self._dobot = PyDobot(port)  # TODO rather use something like /dev/dobot?
        atexit.register(self.cleanup)

    def cleanup(self):
        self._dobot.close()

    def get_end_effectors_ids(self) -> Set[str]:
        return {"default"}

    def get_end_effector_pose(self, end_effector_id: str) -> Pose:  # global pose
        x, y, z = self._dobot.pose()[0:3]  # in mm

        p = Pose()
        p.position.x = x / 1000.0
        p.position.y = y / 1000.0
        p.position.z = z / 1000.0

        return hlp.make_pose_abs(self.pose, p)

    def robot_joints(self) -> List[Joint]:

        joints = self._dobot.pose()[4:]
        ret = []
        for idx, j in enumerate(joints):
            ret.append(Joint(f"joint{idx+1}", j))

        return ret

    @action
    def move(self, pose: Pose, velocity: float, acceleration: float, rotation: float) -> None:
        """
        Moves the robot's end-effector to a specific pose.
        :param pose: Target pose.
        :param velocity: Speed of move (percent).
        :param acceleration: Acceleration of move (percent).
        :param rotation: End effector rotation.
        :return:
        """

        rp = hlp.make_pose_rel(self.pose, pose)

        self._dobot.speed(velocity, acceleration)
        self._dobot.move_to(rp.position.x * 1000.0, rp.position.y * 1000.0, rp.position.z * 1000.0, rotation, wait=True)

    @action
    def suck(self) -> None:
        self._dobot.suck(True)

    @action
    def release(self) -> None:
        self._dobot.suck(False)

    move.__action__ = ActionMetadata(free=True, blocking=True)
    suck.__action__ = ActionMetadata(free=True, blocking=True)
    release.__action__ = ActionMetadata(free=True, blocking=True)


Dobot.DYNAMIC_PARAMS = {
    "end_effector_id": (Dobot.get_end_effectors_ids.__name__, set()),
}
