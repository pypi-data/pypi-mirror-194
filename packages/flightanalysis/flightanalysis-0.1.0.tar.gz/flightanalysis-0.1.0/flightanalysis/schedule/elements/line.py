
import numpy as np
from geometry import Transformation, Point, PX, PY, PZ, Coord
from flightanalysis.base.table import Time
from flightanalysis.state import State
from enum import Enum
from . import El, DownGrades, DownGrade
from flightanalysis.criteria import *


class Line(El):
    parameters = El.parameters + "length,roll,rate".split(",")

    def __init__(self, speed, length, roll=0, uid:str=None):
        super().__init__(uid, speed)
        if length < 0:
            raise ValueError("Cannot create line with negative length")
        self.length = length
        self.roll = roll
    
    @property
    def intra_scoring(self):
        _intra_scoring = DownGrades([
            DownGrade("speed", "measure_speed", intra_f3a_speed),
            DownGrade("ip_track", "measure_ip_track", intra_f3a_angle),
            DownGrade("op_track", "measure_op_track", intra_f3a_angle),
        ])

        if not self.roll == 0:
            _intra_scoring.add(DownGrade("roll_rate", "measure_roll_rate", intra_f3a_roll_rate))
            _intra_scoring.add(DownGrade("roll_amount", "measure_end_roll_angle", basic_angle_f3a))
        else:
            _intra_scoring.add(DownGrade("roll_angle", "measure_roll_angle_error", intra_f3a_angle))
        return _intra_scoring



    def describe(self):
        d1 = "line" if self.roll==0 else f"{self.roll} roll"
        return f"{d1}, length = {self.length} m"

    def to_dict(self):
        return dict(
            kind=self.__class__.__name__,
            length=self.length,
            roll=self.roll,
            speed=self.speed,
            uid=self.uid
        )

    def scale(self, factor):
        return self.set_parms(length=self.length * factor)

    @property
    def rate(self):
        return abs(self.roll) * self.speed / self.length

    def create_template(self, transform: Transformation) -> State:
        """contstruct a State representing the judging frame for this line element

        Args:
            transform (Transformation): initial position and orientation
            speed (float): speed in judging frame X axis
            simple (bool, optional): just create the first and last points of the section. Defaults to False.

        Returns:
            State: [description]
        """
        sec= State.from_transform(
            transform, 
            time = Time(0, 1/State._construct_freq),
            vel=PX(self.speed)
        ).extrapolate(duration=self.length / self.speed)

        return self._add_rolls(sec, self.roll)

    def match_axis_rate(self, roll_rate: float):
        # roll rate in radians per second
        if not self.roll == 0.0:
            return self.set_parms(
                length=abs(self.roll) * self.speed / roll_rate)
        else:
            return self.set_parms()

    def match_intention(self, transform: Transformation, flown: State):
        jit = flown.judging_itrans(transform)
        return self.set_parms(
            length=jit.att.inverse().transform_point(flown.pos - jit.pos).x[-1],
            roll=np.sign(np.mean(flown.p)) * abs(self.roll),
            speed=np.mean(flown.u)
        )

    @staticmethod
    def from_roll(speed: float, rate: float, angle: float):
        return Line(speed, rate * angle * speed, angle )

    def copy_direction(self, other):
        return self.set_parms(roll=abs(self.roll) * np.sign(other.roll))


        