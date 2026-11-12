"""Editable PowerPoint of the method overview (Fig. 2).

One 16:9-like slide: the cleaned BioRender artwork (figures/biorender/overview_clean.png,
made by fig_overview_br.py) as a locked-size picture, with every label as a separate
Times New Roman text box taken from the same LAYOUT table as the paper figure, so the
slide and the PDF stay aligned. Edit text in PowerPoint; move boxes if you change wording.
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
sys.path.insert(0, os.path.dirname(__file__))
from fig_overview_br import LAYOUT, FW, FH, CLEAN, ROOT, split_math

SLIDE_W = 13.333                       # inches
SLIDE_H = SLIDE_W * FH / FW
PT_SCALE = SLIDE_W / 6.875             # paper figure is 6.875 in wide
FONT = "Times New Roman"


def emu_x(x):
    return Emu(int(x / FW * Inches(SLIDE_W)))


def emu_y(y):
    return Emu(int(y / FH * Inches(SLIDE_H)))


def main():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(SLIDE_W), Inches(SLIDE_H)
    slide = prs.slides.add_slide(prs.slide_layouts[6])          # blank
    pic = slide.shapes.add_picture(CLEAN, 0, 0, prs.slide_width, prs.slide_height)
    pic.name = "BioRender artwork (text removed)"

    for n, (x, y, s, size, o) in enumerate(LAYOUT):
        lines = s.split("\n")
        pt = size * PT_SCALE
        # box generous enough for the longest line; text is aligned inside it
        w = max(len(l) for l in lines) * pt * 0.62 / 72 * FW / SLIDE_W + 20
        h = len(lines) * pt * 1.2 / 72 * FH / SLIDE_H + 6
        rot = o.get("rot", 0)
        bw, bh = (w, h) if not rot else (w, h)
        ha = o.get("ha", "center")
        left = x if ha == "left" else x - bw / 2
        top = y - bh / 2
        tb = slide.shapes.add_textbox(emu_x(left), emu_y(top), emu_x(bw), emu_y(bh))
        tb.name = f"label {n}: {lines[0][:30]}"
        if rot:
            tb.rotation = -rot % 360
        tf = tb.text_frame
        tf.word_wrap = True          # LibreOffice centres unwrapped text; wrap keeps alignment
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        for li, line in enumerate(lines):
            para = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
            para.alignment = PP_ALIGN.LEFT if ha == "left" else PP_ALIGN.CENTER
            para.line_spacing = 0.9
            for txt, math in split_math(line):
                run = para.add_run()
                run.text = txt
                f = run.font
                f.name = FONT
                f.size = Pt(round(pt, 1))
                f.bold = bool(o.get("b"))
                f.italic = bool(o.get("i")) or math
                f.color.rgb = RGBColor(0x14, 0x14, 0x14)
    out = os.path.join(ROOT, "figures", "overview.pptx")
    prs.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
