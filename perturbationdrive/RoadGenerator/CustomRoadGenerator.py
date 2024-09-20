# This code is used in the paper
# "Model-based exploration of the frontier of behaviours for deep learning system testing"
# by V. Riccio and P. Tonella
# https://doi.org/10.1145/3368089.3409730
import copy
from typing import List, Tuple, Union
from shapely.geometry import Point

from .Roads.simulator_road import SimulatorRoad

import math
import numpy as np

from .RoadGenerator import RoadGenerator
from .Roads.road import Road
from .Roads.road_polygon import RoadPolygon
from .Roads.catmull_rom import catmull_rom


from shapely.errors import ShapelyDeprecationWarning
import warnings

warnings.simplefilter("ignore", ShapelyDeprecationWarning)


class CustomRoadGenerator(RoadGenerator):
    """Generate random roads given the configuration parameters. The"""

    NUM_INITIAL_SEGMENTS_THRESHOLD = 2
    NUM_UNDO_ATTEMPTS = 20

    def __init__(
        self,
        num_control_nodes=8,
        max_angle=90,
        seg_length=25,
        num_spline_nodes=20,
        initial_node=(0.0, 0.0, 0.0, 0.0),
    ):
        assert num_control_nodes > 1 and num_spline_nodes > 0
        assert 0 <= max_angle <= 360
        assert seg_length > 0
        assert len(initial_node) == 4
        self.num_control_nodes = num_control_nodes
        self.num_spline_nodes = num_spline_nodes
        self.initial_node = initial_node
        self.max_angle = max_angle
        self.seg_length = seg_length
        self.road_to_generate = None

        self.previous_road: Road = None

    def set_max_angle(self, max_angle: int) -> None:
        assert max_angle > 0, "Max angle must be > 0. Found: {}".format(max_angle)
        self.max_angle = max_angle

    def generate_control_nodes(
        self,
        starting_pos: Tuple[float, float, float, float],
        angles: List[int],
        seg_lengths: Union[List[int], None],
    ) -> List[Tuple[float]]:
        if not seg_lengths is None:
            assert len(angles) == len(
                seg_lengths
            ), f"Angles {angles} and lengths {seg_lengths} must have the same length"
        assert (
            len(angles) == self.num_control_nodes
        ), f"We need {self.num_control_nodes} angles {angles}"

        # set the initial node
        self.initial_node = starting_pos
        nodes = [self._get_initial_control_node(), self.initial_node]

        # i_valid is the number of valid generated control nodes.
        i_valid = 0

        while i_valid < self.num_control_nodes:
            seg_length = self.seg_length
            if seg_lengths is not None and i_valid < len(seg_lengths):
                seg_length = seg_lengths[i_valid]
                print(f"custom seg length {seg_length}")
            nodes.append(
                self._get_next_node(
                    nodes[-2],
                    nodes[-1],
                    angles[i_valid],
                    self.max_angle,
                    seg_length,
                )
            )
            i_valid += 1

        return nodes

    def is_valid(self, control_nodes, sample_nodes):
        return RoadPolygon.from_nodes(sample_nodes).is_valid()

    def generate(self, *args, **kwargs) -> str:
        """
        Needs a list of integer angles in the kwargs param `angles`.
        Optionally takes another list of segment lengths in `seg_lengths` key of kwargs.
        """

        if self.road_to_generate is not None:
            road_to_generate = copy.deepcopy(self.road_to_generate)
            self.road_to_generate = None
            return road_to_generate

        sample_nodes = None

        seg_lengths = None
        if "seg_lengths" in kwargs:
            seg_lengths = kwargs["seg_lengths"]

        control_nodes = self.generate_control_nodes(
            starting_pos=kwargs["starting_pos"],
            angles=kwargs["angles"],
            seg_lengths=seg_lengths,
        )
        control_nodes = control_nodes[0:]
        sample_nodes = catmull_rom(control_nodes, self.num_spline_nodes)

        road_points = [Point(node[0], node[1], node[2]) for node in sample_nodes]
        control_points = [Point(node[0], node[1], node[2]) for node in control_nodes]
        _, _, _, width = self.initial_node
        self.previous_road = SimulatorRoad(
            road_width=width,
            road_points=road_points,
            control_points=control_points,
        )

        return self.previous_road.serialize_concrete_representation(
            cr=self.previous_road.get_concrete_representation()
        )

    def _get_initial_point(self) -> Point:
        return Point(self.initial_node[0], self.initial_node[1])

    def _get_initial_control_node(self) -> Tuple[float, float, float, float]:
        x0, y0, z, width = self.initial_node
        x, y = self._get_next_xy(x0, y0, 270, self.seg_length)

        return x, y, z, width

    def _get_next_node(
        self,
        first_node,
        second_node: Tuple[float, float, float, float],
        angle: int,
        max_angle,
        seg_length: Union[float, None] = None,
    ) -> Tuple[float, float, float, float]:
        v = np.subtract(second_node, first_node)
        start_angle = int(np.degrees(np.arctan2(v[1], v[0])))
        angle = start_angle + angle
        if angle > start_angle + max_angle or angle < start_angle - max_angle:
            print(
                f"{5 * '+'} Warning {angle} is not in range of {start_angle - max_angle} and {start_angle + max_angle}. {5 * '+'}"
            )
            # angle = randint(start_angle - max_angle, start_angle + max_angle)
        x0, y0, z0, width0 = second_node
        if seg_length is None:
            seg_length = self.seg_length
        x1, y1 = self._get_next_xy(x0, y0, angle, seg_length)
        return x1, y1, z0, width0

    def _get_next_xy(
        self, x0: float, y0: float, angle: float, seg_length: int
    ) -> Tuple[float, float]:
        angle_rad = math.radians(angle)
        return x0 + seg_length * math.cos(angle_rad), y0 + seg_length * math.sin(
            angle_rad
        )

    def _get_next_max_angle(
        self, i: int, threshold=NUM_INITIAL_SEGMENTS_THRESHOLD
    ) -> float:
        if i < threshold or i == self.num_control_nodes - 1:
            return 0
        else:
            return self.max_angle
