import math
from typing import Optional

import pymunk
from neoscore.core.brush import BrushDef, Brush
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText, MusicStringDef
from neoscore.core.path import Path
from neoscore.core.pen import PenDef, Pen
from neoscore.core.point import PointDef, ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.text_alignment import AlignmentX, AlignmentY
from neoscore.core.units import Unit
from pymunk import Space, Poly


class MusicTextPhysics(MusicText):
    """MusicText, but with physics!"""
    def __init__(
            self,
            pos: PointDef,
            parent: Optional[PositionedObject],
            text: MusicStringDef,
            space: Optional[Space],
            font: Optional[MusicFont] = None,
            brush: Optional[BrushDef] = None,
            pen: Optional[PenDef] = None,
            scale: float = 1,
            rotation: float = 0,
            background_brush: Optional[BrushDef] = None,
            breakable: bool = True,
            alignment_x: AlignmentX = AlignmentX.CENTER,
            alignment_y: AlignmentY = AlignmentY.CENTER,
            transform_origin: PointDef = ORIGIN,
            debug: bool = False,
    ):
        """
        Args:
            pos: The position of the text.
            parent: The parent of the glyph. If no ``font`` is given,
                this or one of its ancestors must implement :obj:`.HasMusicFont`.
            text: The text to display. Can be given as a SMuFL glyph name
                or other shorthand forms. See ``MusicStringDef``.
            space: The physics space.
            font: The music font to be used. If not specified, ``parent`` must
                implement :obj:`.HasMusicFont` or have an ancestor which does.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            scale: A scaling factor to be applied in addition to the size of the music font.
            rotation: Angle in degrees. Note that breakable rotated text is
                not currently supported.
            background_brush: Optional brush used to paint the text's bounding rect
                behind it.
            breakable: Whether this object should break across lines in
                :obj:`.Flowable` containers.
            alignment_x: The text's horizontal alignment relative to ``pos``.
                Note that text which is not ``LEFT`` aligned does not currently display
                correctly when breaking across flowable lines.
            alignment_y: The text's vertical alignment relative to ``pos``.
            transform_origin: The origin point for rotation and scaling transforms.
            debug: Whether the bounding rectangle is displayed.
        """
        MusicText.__init__(
            self,
            pos,
            parent,
            text,
            font,
            brush,
            pen,
            scale,
            rotation,
            background_brush,
            breakable,
            alignment_x,
            alignment_y,
            transform_origin,
        )
        self.debug = debug
        if debug:
            self.debug_rect = Path.rect(self.pos + Point(self.bounding_rect.x, self.bounding_rect.y),
                                        None,
                                        self.bounding_rect.width,
                                        self.bounding_rect.height,
                                        Brush.no_brush(),
                                        Pen())
            self.debug_rect.transform_origin = (
                self.bounding_rect.width / 2,
                self.bounding_rect.height / 2
            )
            self.debug_rect.rotation = self.rotation

        body = pymunk.Body()
        body.position = (self.x.base_value - self.bounding_rect.width.base_value / 2,
                         self.y.base_value - self.bounding_rect.height.base_value / 2)
        poly = Poly.create_box(body, (self.bounding_rect.width.base_value, self.bounding_rect.height.base_value))
        poly.mass = (self.bounding_rect.width.base_value/10 + self.bounding_rect.height.base_value/10)
        poly.collision_type = 2   # Objects have type 2 collision and can collide with type 1 (walls) and other type 2
        poly.friction = 0.68
        space.add(body, poly)  # Add this object to the physics space

    def move_object(self, new_pos):
        #  new_pos is the position of a single object in the pymunk physics space.
        self.x = Unit(new_pos.x)
        self.y = Unit(new_pos.y)
        self.rotation = math.degrees(new_pos.angle)
        if self.debug:
            self.debug_rect.x = Unit(new_pos.x) - self.bounding_rect.width/2
            self.debug_rect.y = Unit(new_pos.y) - self.bounding_rect.height/2
            self.debug_rect.rotation = math.degrees(new_pos.angle)
