import random
from typing import Optional

import pymunk
from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.flowable import Flowable
from neoscore.core.key_event import KeyEventType
from neoscore.core.mouse_event import MouseEventType
from neoscore.core.music_font import MusicFont
from neoscore.core.path import Path
from neoscore.core.point import ORIGIN
from neoscore.core.units import Unit, Mm
from neoscore.western.clef import Clef
from neoscore.western.dynamic import Dynamic
from neoscore.western.staff import Staff
from pymunk import Vec2d

from class_extensions import MusicTextPhysics


def refresh_func(time: float) -> Optional[neoscore.RefreshFuncResult]:
    space.step(1/60)  # Evaluate the physics space
    for idx, i in enumerate(space.bodies):
        physics_list[idx].move_object(i.position)  # Match rendering to the physics space


def key_event_handler(event):
    if event.event_type == KeyEventType.PRESS:
        for i in space.bodies:
            i.apply_impulse_at_local_point((random.randint(-1000, 1000), random.randint(-1000, 1000)), (0, 0))


def mouse_event_handler(event):
    if event.event_type == MouseEventType.PRESS:
        click_vec = Vec2d(event.document_pos.x.base_value, event.document_pos.y.base_value)
        for i in space.bodies:
            dist = Vec2d.get_distance(click_vec, i.position)
            impulse = -20000/(dist**2)
            imp_vector = impulse * (click_vec - i.position)
            i.apply_impulse_at_local_point(imp_vector, (0, 0))


def draw_bounding_box(s):
    w, h = 480, 600
    Path.rect((Unit(0), Unit(0)), None, Unit(w), Unit(h), brush=Brush.no_brush())
    #  Objects can phase through walls if moving too quickly. Solution: Thick walls.
    left_wall = pymunk.Poly(s.static_body, [(0, -h), (-w, -h), (-w, 2*h), (0, 2*h)])
    right_wall = pymunk.Poly(s.static_body, [(w, -h), (2*w, -h), (2*w, 2*h), (w, 2*h)])
    bottom_wall = pymunk.Poly(s.static_body, [(-w, h), (2*w, h), (2*w, 2*h), (-w, 2*h)])
    top_wall = pymunk.Poly(s.static_body, [(-w, 0), (2*w, 0), (2*w, -h), (-w, -h)])
    left_wall.friction = 0.68
    right_wall.friction = 0.68
    bottom_wall.friction = 0.68
    top_wall.friction = 0.68
    left_wall.collision_type = 1
    bottom_wall.collision_type = 1
    right_wall.collision_type = 1
    top_wall.collision_type = 1
    s.add(left_wall)
    s.add(bottom_wall)
    s.add(right_wall)
    s.add(top_wall)


def make_my_space():
    s = pymunk.Space()
    s.gravity = (0, 981)  # 981 is pretty close to Earth gravity
    s.damping = 0.2
    draw_bounding_box(s)  # Make static walls for objects to collide with.
    h = s.add_collision_handler(1, 2)
    return s, h


if __name__ == "__main__":
    neoscore.setup()
    font = MusicFont("Bravura", Mm(2))
    space, handler = make_my_space()

    flow = Flowable(ORIGIN, None, Mm(1500), Mm(15))
    staff = Staff((Unit(0), Unit(0)), flow, Mm(1500))
    clef = Clef(staff.unit(0), staff, "treble")
    physics_list = []
    for j in range(4):
        for i in range(20):
            physics_list.append(MusicTextPhysics((staff.unit(2 * i), Mm(20 * j) + staff.unit(random.randint(0, 0)/2)),
                                                 None, "noteheadWhole", space, font=font))
    physics_list.append(MusicTextPhysics((Unit(100), staff.unit(50)), staff, "gClef", space))
    Dynamic((Unit(40), staff.unit(40)), staff, "p")

    neoscore.set_key_event_handler(key_event_handler)
    neoscore.set_mouse_event_handler(mouse_event_handler)
    neoscore.show(refresh_func)
