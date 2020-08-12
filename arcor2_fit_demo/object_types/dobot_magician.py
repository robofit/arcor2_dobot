import os
import time
from dataclasses import dataclass
from typing import List, Set, cast

import arcor2.transformations as tr
from arcor2 import DynamicParamTuple as DPT
from arcor2.data.common import ActionMetadata, Joint, Pose, StrEnum
from arcor2.exceptions import Arcor2Exception
from arcor2.object_types.abstract import Robot, Settings

from pydobot import dobot  # type: ignore

import quaternion  # type: ignore

import serial  # type: ignore

import arcor2_fit_demo

# TODO pid as __init__ parameter?
# TODO jogging


@dataclass
class DobotSettings(Settings):

    port: str = "/dev/dobot"
    calibrate_on_init: bool = False
    simulator: bool = False


class DobotException(Arcor2Exception):
    pass


class MoveType(StrEnum):

    JUMP: str = "JUMP"
    JOINTS: str = "JOINTS"
    LINEAR: str = "LINEAR"


class Joints(StrEnum):

    J1: str = "magician_joint_1"
    J2: str = "magician_joint_2"
    J3: str = "magician_joint_3"
    J4: str = "magician_joint_4"
    J5: str = "magician_joint_5"


MOVE_TYPE_MAPPING = {
    MoveType.JUMP: dobot.MODE_PTP_JUMP_XYZ,
    MoveType.JOINTS: dobot.MODE_PTP_MOVJ_XYZ,
    MoveType.LINEAR: dobot.MODE_PTP_MOVL_XYZ
}


class DobotMagician(Robot):
    """
    Dobot Magician.
    """

    _ABSTRACT = False

    urdf_package_path = os.path.join(os.path.dirname(arcor2_fit_demo.__file__), "data", "dobot-magician.zip")

    def __init__(self, obj_id: str, name: str, pose: Pose, settings: DobotSettings) -> None:
        super(DobotMagician, self).__init__(obj_id, name, pose, settings)

        if not self.settings.simulator:

            try:
                self._dobot = dobot.Dobot(self.settings.port)
            except serial.serialutil.SerialException as e:
                raise DobotException("Could not connect to the robot.") from e

            if self.settings.calibrate_on_init:
                self.home()

        else:

            self._pose = Pose()

    @property
    def settings(self) -> DobotSettings:
        return cast(DobotSettings, super(DobotMagician, self).settings)

    def cleanup(self):

        if not self.settings.simulator:
            self._dobot.close()

    def get_end_effectors_ids(self) -> Set[str]:
        return {"default"}

    def grippers(self) -> Set[str]:
        return set()

    def suctions(self) -> Set[str]:
        return {"default"}

    def get_end_effector_pose(self, end_effector_id: str) -> Pose:  # global pose

        if self.settings.simulator:
            return self._pose

        pos = self._dobot.position()  # in mm

        p = Pose()
        p.position.x = pos.x / 1000.0
        p.position.y = pos.y / 1000.0
        p.position.z = pos.z / 1000.0
        p.orientation.set_from_quaternion(quaternion.from_euler_angles(0, 0, self._dobot.r))

        return tr.make_pose_abs(self.pose, p)

    def robot_joints(self) -> List[Joint]:

        if self.settings.simulator:
            return [
                Joint(Joints.J1, 0),
                Joint(Joints.J2, 0),
                Joint(Joints.J3, 0),
                Joint(Joints.J4, 0),
                Joint(Joints.J5, 0)
            ]

        joints = self._dobot.joints()
        return [
            Joint(Joints.J1, joints.j1),
            Joint(Joints.J2, joints.j2),
            Joint(Joints.J3, joints.j3 - joints.j2),
            Joint(Joints.J4, -joints.j3),
            Joint(Joints.J5, joints.j4)
        ]

    def move_to_pose(self, end_effector: str, target_pose: Pose, speed: float) -> None:
        self.move(target_pose, MoveType.LINEAR, speed * 100, 50.0)

    def move_to_joints(self, target_joints: List[Joint], speed: float) -> None:
        raise NotImplementedError("Dobot does not support setting joints so far.")

    def home(self):
        """
        Run the homing procedure.
        """

        if self.settings.simulator:
            time.sleep(2.0)
            return

        self._dobot.wait_for_cmd(self._dobot.home())

    def move(self, pose: Pose, move_type: MoveType, velocity: float = 50., acceleration: float = 50.) -> None:
        """
        Moves the robot's end-effector to a specific pose.
        :param pose: Target pose.
        :move_type: Move type.
        :param velocity: Speed of move (percent).
        :param acceleration: Acceleration of move (percent).
        :return:
        """

        assert .0 <= velocity <= 100.
        assert .0 <= acceleration <= 100.

        if self.settings.simulator:
            time.sleep((100.0 - velocity) * 0.05)
            self._pose = pose
            return

        rp = tr.make_pose_rel(self.pose, pose)
        rotation = quaternion.as_euler_angles(rp.orientation.as_quaternion())[2]
        self._dobot.speed(velocity, acceleration)
        self._dobot.wait_for_cmd(self._dobot.move_to(rp.position.x * 1000.0,
                                                     rp.position.y * 1000.0,
                                                     rp.position.z * 1000.0,
                                                     rotation,
                                                     MOVE_TYPE_MAPPING[move_type]))

    def suck(self) -> None:

        if not self.settings.simulator:
            self._dobot.wait_for_cmd(self._dobot.suck(True))

    def release(self) -> None:

        if not self.settings.simulator:
            self._dobot.wait_for_cmd(self._dobot.suck(False))

    home.__action__ = ActionMetadata(blocking=True)  # type: ignore
    move.__action__ = ActionMetadata(blocking=True)  # type: ignore
    suck.__action__ = ActionMetadata(blocking=True)  # type: ignore
    release.__action__ = ActionMetadata(blocking=True)  # type: ignore


DobotMagician.DYNAMIC_PARAMS = {
    "end_effector_id": DPT(DobotMagician.get_end_effectors_ids.__name__, set()),
}
