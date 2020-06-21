from typing import Optional, List, FrozenSet
import os

from pydobot import dobot
import quaternion

from arcor2.data.common import StrEnum
from arcor2.object_types import Robot
from arcor2.data.common import Pose, ActionMetadata, Joint, ProjectRobotJoints
from arcor2.data.object_type import Models
from arcor2.action import action
import arcor2.helpers as hlp

import arcor2_dobot

# TODO pid as __init__ parameter?
# TODO jogging


class MoveType(StrEnum):

    JUMP: str = "JUMP"
    JOINTS: str = "JOINTS"
    LINEAR: str = "LINEAR"


MOVE_TYPE_MAPPING = {
    MoveType.JUMP: dobot.MODE_PTP_JUMP_XYZ,
    MoveType.JOINTS: dobot.MODE_PTP_MOVJ_XYZ,
    MoveType.LINEAR: dobot.MODE_PTP_MOVL_XYZ
}


class DobotMagician(Robot):
    """
    Dobot Magician.
    """

    urdf_package_path = os.path.join(os.path.dirname(arcor2_dobot.__file__), "data", "dobot-magician.zip")

    def __init__(self, obj_id: str, name: str, pose: Pose, collision_model: Optional[Models] = None) -> None:

        super(Robot, self).__init__(obj_id, name, pose, collision_model)
        self._dobot = dobot.Dobot("/dev/dobot")  # TODO get device from object configuration

    def cleanup(self):
        self._dobot.close()

    def get_end_effectors_ids(self) -> FrozenSet[str]:
        return frozenset({"default"})

    def grippers(self) -> FrozenSet[str]:
        return frozenset()

    def suctions(self) -> FrozenSet[str]:
        return frozenset({"default"})

    def get_end_effector_pose(self, end_effector_id: str) -> Pose:  # global pose
        pos = self._dobot.position()  # in mm

        p = Pose()
        p.position.x = pos.x / 1000.0
        p.position.y = pos.y / 1000.0
        p.position.z = pos.z / 1000.0
        p.orientation.set_from_quaternion(quaternion.from_euler_angles(0, 0, self._dobot.r))

        return hlp.make_pose_abs(self.pose, p)

    def robot_joints(self) -> List[Joint]:

        joints = self._dobot.joints()
        return [
            Joint("magician_joint_1", joints.j1),
            Joint("magician_joint_2", joints.j2),
            Joint("magician_joint_3", joints.j3-joints.j2),
            Joint("magician_joint_4", joints.j2-joints.j3),
            Joint("magician_joint_5", joints.j4),
            ]

    def move_to_pose(self, target_pose: Pose, end_effector: str, speed: float) -> None:
        self.move(target_pose, MoveType.LINEAR, speed*100, 50.0)

    def move_to_joints(self, target_joints: ProjectRobotJoints, speed: float) -> None:
        assert target_joints.robot_id == self.id
        raise NotImplementedError("Dobot does not support setting joints so far.")

    @action
    def home(self):
        """
        Run the homing procedure.
        """

        self._dobot.wait_for_cmd(self._dobot.home())

    @action
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

        rp = hlp.make_pose_rel(self.pose, pose)
        rotation = quaternion.as_euler_angles(rp.orientation.as_quaternion())[2]
        self._dobot.speed(velocity, acceleration)
        self._dobot.wait_for_cmd(self._dobot.move_to(rp.position.x * 1000.0,
                                                     rp.position.y * 1000.0,
                                                     rp.position.z * 1000.0,
                                                     rotation,
                                                     MOVE_TYPE_MAPPING[move_type]))

    @action
    def suck(self) -> None:
        self._dobot.wait_for_cmd(self._dobot.suck(True))

    @action
    def release(self) -> None:
        self._dobot.wait_for_cmd(self._dobot.suck(False))

    home.__action__ = ActionMetadata(free=True, blocking=True)
    move.__action__ = ActionMetadata(free=True, blocking=True)
    suck.__action__ = ActionMetadata(free=True, blocking=True)
    release.__action__ = ActionMetadata(free=True, blocking=True)


DobotMagician.DYNAMIC_PARAMS = {
    "end_effector_id": (DobotMagician.get_end_effectors_ids.__name__, set()),
}
