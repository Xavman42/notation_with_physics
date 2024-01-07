from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.path import Path
from neoscore.core.text_alignment import AlignmentY, AlignmentX
from neoscore.core.units import Unit, Mm


def rotate_and_box(smufl_text, font_size, y_position):
    font = MusicFont("Bravura", Mm(font_size))
    for i in range(9):
        text = MusicText((Unit(i * 80), Unit(y_position)), None, smufl_text, font)
        text.alignment_x = AlignmentX.CENTER
        text.alignment_y = AlignmentY.CENTER
        text.transform_origin = Unit(text.bounding_rect.width / 2), Unit(0)
        text.rotation = i * (360 / 8)
        rectangle = Path.rect((Unit(text.x - text.bounding_rect.width / 2),
                               Unit(text.y - text.bounding_rect.height / 2)), None,
                              Unit(text.bounding_rect.width),
                              Unit(text.bounding_rect.height), brush=Brush.no_brush())
        rectangle.transform_origin = Unit(text.bounding_rect.width / 2), Unit(text.bounding_rect.height / 2)
        rectangle.rotation = i * (360 / 8)


if __name__ == "__main__":
    neoscore.setup()
    rotate_and_box("noteheadWhole", 10, 0)
    rotate_and_box("accidentalSharp", 8, 100)
    rotate_and_box("accidentalParensLeft", 10, 200)
    rotate_and_box("restQuarter", 9, 300)
    rotate_and_box("gClef", 4, 400)
    rotate_and_box("rest128th", 5, 500)
    rotate_and_box("pluckedSnapPizzicatoAbove", 8, 600)
    neoscore.show()
