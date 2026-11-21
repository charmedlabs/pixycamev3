"""Intersection parsing in get_linetracking_data (runs off-robot with stubs)."""
import builtins
import importlib
import io
import os
import struct
import sys
import types
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_pixy2():
    # Stub the EV3-only modules and the board-info check done at import time.
    for name in ('smbus', 'ev3dev2', 'ev3dev2.sensor', 'ev3dev2.port'):
        sys.modules.setdefault(name, types.ModuleType(name))
    sys.modules['smbus'].SMBus = object
    sys.modules['ev3dev2.sensor'].INPUT_1 = sys.modules['ev3dev2.sensor'].INPUT_2 = None
    sys.modules['ev3dev2.sensor'].INPUT_3 = sys.modules['ev3dev2.sensor'].INPUT_4 = None
    sys.modules['ev3dev2.port'].LegoPort = object
    real_open = builtins.open

    def fake_open(path, *a, **k):
        if str(path).startswith('/sys/class/board-info/'):
            return io.StringIO('BOARD_INFO_MODEL=LEGO MINDSTORMS EV3\n')
        return real_open(path, *a, **k)

    with mock.patch.object(os, 'listdir', return_value=['board0']), \
            mock.patch.object(builtins, 'open', fake_open):
        sys.modules.pop('pixycamev3.pixy2', None)
        return importlib.import_module('pixycamev3.pixy2')


def test_intersection_branches_follow_pixy2_layout():
    pixy2 = _load_pixy2()
    # Pixy2 Intersection: x, y, n, reserved, then 6 x {index, reserved, int16 angle}.
    lines = [(3, 90), (7, -45), (11, 180)] + [(0, 0)] * 3
    feature = bytes([40, 30, 3, 0]) + b''.join(
        struct.pack('<BBh', idx, 0, ang) for idx, ang in lines)
    payload = bytes([2, len(feature)]) + feature
    reads = [list(payload[:2]), list(payload[2:])]

    cam = pixy2.Pixy2.__new__(pixy2.Pixy2)
    cam.pixy2_request = lambda data, rtype: [175, 193, rtype, len(payload), 0, 0]
    cam._i2c_read = lambda n: reads.pop(0)

    features = cam.get_linetracking_data()
    ints = features.intersections[0]
    assert (ints.x, ints.y, ints.nr_of_branches) == (40, 30, 3)
    assert [(b.index, b.angle) for b in ints.branches] == [(3, 90), (7, -45), (11, 180)]
