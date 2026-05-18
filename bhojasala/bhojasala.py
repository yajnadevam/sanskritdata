from pathlib import Path
import math

W, H = 1100, 2350
cx, cy = W / 2, 1600
cell = 80          # cell edge length
n = 5              # 5x5 grid
s = cell * math.sqrt(2) / 2   # half-diagonal of a cell

def vertex(i, j):
    # +X axis points up-right, +Y axis points up-left.
    # (0,0) = bottom, (n,0) = right, (n,n) = top, (0,n) = left
    return (cx + (i - j) * s, cy + n * s - (i + j) * s)

lines = []
# All grid lines extended by one cell on each side (each corner has two stubs).
# The j=0,1 lines and i=0,1 lines are extended much further on their respective
# negative ends (down to i=-5 or j=-5) to form a long tail toward the bottom.
for j in range(n + 1):
    # j=0 extends to i=-6 (one cell shorter than i=-7); j=1 extends to i=-6.
    # j=4 and j=5 lines extend 3 extra cell units past their normal right stub.
    left_i = {0: -6, 1: -6}.get(j, -1)
    right_i = n + 4 if j in (4, 5) else n + 1
    lines.append(vertex(left_i, j) + vertex(right_i, j))
for i in range(n + 1):
    # i=0 and i=1 both extend to j=-6 (mirror of the left side j=0, j=1 extensions).
    # i=4 and i=5 stop at j=n so the upper stubs are replaced by 1/4 arcs.
    bottom_j = {0: -6, 1: -6}.get(i, -1)
    top_j = n if i in (4, 5) else n + 1
    lines.append(vertex(i, bottom_j) + vertex(i, top_j))

# Cross-bars connecting the two tails near the bottom. The upper cross-bar is
# extended on both sides so its endpoints become tangent points of the outer arcs.
upper_cross_left_x  = cx - 3 * s * (1 + math.sqrt(2))
upper_cross_right_x = cx + 3 * s * (1 + math.sqrt(2))
lines.append((upper_cross_left_x, cy + 8 * s, upper_cross_right_x, cy + 8 * s))
lines.append((cx - 7 * s, cy + 9 * s, cx + 7 * s, cy + 9 * s))

svg_lines = "\n  ".join(
    f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}"/>'
    for x0, y0, x1, y1 in lines
)

# Concentric semicircles centered at grid (2.5, 6):
#   inner: (2,6) → (3,6), radius = cell/2
#   outer: (1,6) → (4,6), radius = 3·cell/2  (parallel to the inner)
def semicircle(p_start, p_end, radius, sweep):
    return (
        f'<path d="M {p_start[0]:.2f} {p_start[1]:.2f} '
        f'A {radius:.2f} {radius:.2f} 0 0 {sweep} {p_end[0]:.2f} {p_end[1]:.2f}" '
        f'fill="none"/>'
    )

svg_arc = "\n  ".join([
    semicircle(vertex(1, 6), vertex(2, 6), cell / 2,       1),
    semicircle(vertex(0, 6), vertex(3, 6), 3 * cell / 2,   1),
    semicircle(vertex(3, -1), vertex(4, -1), cell / 2,     0),
    semicircle(vertex(2, -1), vertex(5, -1), 3 * cell / 2, 0),
    semicircle(vertex(6, 1), vertex(6, 2), cell / 2,       0),
    semicircle(vertex(6, 0), vertex(6, 3), 3 * cell / 2,   0),
    semicircle(vertex(-1, 3), vertex(-1, 4), cell / 2,     1),
    semicircle(vertex(-1, 2), vertex(-1, 5), 3 * cell / 2, 1),
    # 135° arc bridging the j=1 line endpoint to the lower horizontal line endpoint.
    semicircle((cx - 7 * s, cy + 10 * s), (cx - 7 * s, cy + 9 * s),
               s / (2 * math.sin(math.radians(67.5))), 1),
    # Mirror of the small left arc: i=1 line endpoint to the lower horizontal right end.
    semicircle((cx + 7 * s, cy + 10 * s), (cx + 7 * s, cy + 9 * s),
               s / (2 * math.sin(math.radians(67.5))), 0),
])

# Outer "parallel" arc: major arc (225°, ≈ 2/3 of a circle) tangent to j=0 at
# its endpoint and to the upper cross-bar at its extended endpoint. Bulges
# outward (down-left). Sized as the tangent fillet of the 45° wedge.
R_outer_arc = 3 * s * (2 - math.sqrt(2))
big_arc_left = (
    f'<path d="M {cx - 6 * s:.2f} {cy + 11 * s:.2f} '
    f'A {R_outer_arc:.2f} {R_outer_arc:.2f} 0 1 1 '
    f'{upper_cross_left_x:.2f} {cy + 8 * s:.2f}" '
    f'fill="none"/>'
)
# Mirror of the left big arc on the right side.
big_arc_right = (
    f'<path d="M {cx + 6 * s:.2f} {cy + 11 * s:.2f} '
    f'A {R_outer_arc:.2f} {R_outer_arc:.2f} 0 1 0 '
    f'{upper_cross_right_x:.2f} {cy + 8 * s:.2f}" '
    f'fill="none"/>'
)
svg_arc = svg_arc + "\n  " + big_arc_left + "\n  " + big_arc_right

# 1/8 arcs (45°) tangent to the i=5 and i=4 lines at (5,5) and (4,5) respectively.
# Each turns 45° CW so the end tangent points straight up.
eighth_top_5 = (
    f'<path d="M {cx:.2f} {cy - 5 * s:.2f} '
    f'A {s:.2f} {s:.2f} 0 0 1 '
    f'{cx + cell / 2 - s:.2f} {cy - 5 * s - cell / 2:.2f}" '
    f'fill="none"/>'
)
eighth_top_4 = (
    f'<path d="M {cx - s:.2f} {cy - 4 * s:.2f} '
    f'A {cell + s:.2f} {cell + s:.2f} 0 0 1 '
    f'{cx - cell / 2 - s:.2f} {cy - 5 * s - cell / 2:.2f}" '
    f'fill="none"/>'
)
svg_arc = svg_arc + "\n  " + eighth_top_5 + "\n  " + eighth_top_4

# Vertical line of length 4·cell continuing straight up from the i=5 arc end.
_top5_end_x = cx + cell / 2 - s
_top5_end_y = cy - 5 * s - cell / 2
vertical_spire = (
    f'<line x1="{_top5_end_x:.2f}" y1="{_top5_end_y:.2f}" '
    f'x2="{_top5_end_x:.2f}" y2="{_top5_end_y - 5 * cell:.2f}"/>'
)
# Parallel vertical line one cell to the left.
vertical_spire_left = (
    f'<line x1="{_top5_end_x - cell:.2f}" y1="{_top5_end_y:.2f}" '
    f'x2="{_top5_end_x - cell:.2f}" y2="{_top5_end_y - 5 * cell:.2f}"/>'
)
svg_arc = svg_arc + "\n  " + vertical_spire + "\n  " + vertical_spire_left

# Right-angle triangle on top of the parallel vertical lines (flipped vertically).
# Hypotenuse (length 4·cell) is horizontal at the line-tops level; right-angle
# apex points up 2·cell above the hypotenuse.
_lines_top_y = _top5_end_y - 5 * cell
_mid_x = _top5_end_x - cell / 2
_apex = (_mid_x, _lines_top_y - 2 * cell)
_hyp_left = (_mid_x - 2 * cell, _lines_top_y)
_hyp_right = (_mid_x + 2 * cell, _lines_top_y)
triangle_top = (
    f'<path d="M {_hyp_left[0]:.2f} {_hyp_left[1]:.2f} '
    f'L {_hyp_right[0]:.2f} {_hyp_right[1]:.2f} '
    f'L {_apex[0]:.2f} {_apex[1]:.2f} Z" '
    f'fill="none"/>'
)
# Mirror-image triangle above, sharing the same apex point.
_hyp_left_2 = (_mid_x - 2 * cell, _lines_top_y - 4 * cell)
_hyp_right_2 = (_mid_x + 2 * cell, _lines_top_y - 4 * cell)
triangle_top_2 = (
    f'<path d="M {_hyp_left_2[0]:.2f} {_hyp_left_2[1]:.2f} '
    f'L {_hyp_right_2[0]:.2f} {_hyp_right_2[1]:.2f} '
    f'L {_apex[0]:.2f} {_apex[1]:.2f} Z" '
    f'fill="none"/>'
)
svg_arc = svg_arc + "\n  " + triangle_top + "\n  " + triangle_top_2

# Trapezium on top of the upper triangle. Base = upper triangle's hypotenuse
# (4·cell); top = half that (2·cell); height = 4/3 × base = 16·cell/3.
_trap_base_y = _lines_top_y - 4 * cell
_trap_top_y = _trap_base_y - 16 * cell / 3

# Vertical bisector extended up through the trapezium top.
triangle_bisector = (
    f'<line x1="{_mid_x:.2f}" y1="{_trap_top_y:.2f}" '
    f'x2="{_mid_x:.2f}" y2="{_lines_top_y:.2f}"/>'
)
svg_arc = svg_arc + "\n  " + triangle_bisector
trapezium = (
    f'<path d="M {_mid_x - 2 * cell:.2f} {_trap_base_y:.2f} '
    f'L {_mid_x + 2 * cell:.2f} {_trap_base_y:.2f} '
    f'L {_mid_x + cell:.2f} {_trap_top_y:.2f} '
    f'L {_mid_x - cell:.2f} {_trap_top_y:.2f} Z" '
    f'fill="none"/>'
)
svg_arc = svg_arc + "\n  " + trapezium

# Horizontal lines slicing the trapezium into 4 vertically-equal sections.
trap_slices = "\n  ".join(
    f'<line x1="{_mid_x - (2 - t) * cell:.2f}" '
    f'y1="{_trap_base_y - t * 16 * cell / 3:.2f}" '
    f'x2="{_mid_x + (2 - t) * cell:.2f}" '
    f'y2="{_trap_base_y - t * 16 * cell / 3:.2f}"/>'
    for t in (0.25, 0.5, 0.75)
)
svg_arc = svg_arc + "\n  " + trap_slices

# Devanagari text inside the trapezium, triangles, and above the trapezium.
def _txt(x, y, s, size=36):
    return (
        f'<text class="txt" x="{x:.2f}" y="{y:.2f}" '
        f'font-size="{size}" text-anchor="middle">{s}</text>'
    )

# "श्रीः" above the trapezium top
_text_elements = [_txt(_mid_x, _trap_top_y - cell / 2, "श्रीः", size=44)]

# Vowel pairs in trapezium slices (top to bottom).
_vowel_pairs = [("अ", "आ"), ("इ", "ई"), ("उ", "ऊ"), ("ऋ", "ॠ")]
_slice_ts = [7/8, 5/8, 3/8, 1/8]  # slice centers from top to bottom
for (a, b), t in zip(_vowel_pairs, _slice_ts):
    y = _trap_base_y - t * 16 * cell / 3
    off = (2 - t) * cell / 2
    _text_elements.append(_txt(_mid_x - off, y, a, size=34))
    _text_elements.append(_txt(_mid_x + off, y, b, size=34))

# Upper triangle (apex down) — ए ऐ
_text_elements.append(_txt(_mid_x - cell / 2, _lines_top_y - 10 * cell / 3, "ए", size=34))
_text_elements.append(_txt(_mid_x + cell / 2, _lines_top_y - 10 * cell / 3, "ऐ", size=34))
# Lower triangle (apex up) — ओ औ
_text_elements.append(_txt(_mid_x - cell / 2, _lines_top_y - 2 * cell / 3, "ओ", size=34))
_text_elements.append(_txt(_mid_x + cell / 2, _lines_top_y - 2 * cell / 3, "औ", size=34))

svg_arc = svg_arc + "\n  " + "\n  ".join(_text_elements)

# 4 horizontal dividers splitting the section between the parallel vertical
# lines (below the triangles) into 5 equal slices, with consonants in each.
_spire_left_x = _top5_end_x - cell
_spire_right_x = _top5_end_x
_spire_bottom_y = _top5_end_y
_spire_top_y = _top5_end_y - 5 * cell
_spire_mid_x = (_spire_left_x + _spire_right_x) / 2
_slice_h = cell  # 5*cell total / 5 slices

_spire_dividers = "\n  ".join(
    f'<line x1="{_spire_left_x:.2f}" y1="{_spire_bottom_y - k * _slice_h:.2f}" '
    f'x2="{_spire_right_x:.2f}" y2="{_spire_bottom_y - k * _slice_h:.2f}"/>'
    for k in (1, 2, 3, 4)
)
_spire_text = "\n  ".join(
    _txt(_spire_mid_x,
         _spire_top_y + (i + 0.5) * _slice_h,
         ch, size=34)
    for i, ch in enumerate(["ह", "य", "व", "र", "ल"])
)
svg_arc = svg_arc + "\n  " + _spire_dividers + "\n  " + _spire_text

# Tangent 45° arc at (9, 5) curving the j=5 line outward direction up to vertical,
# followed by a vertical line up to the trapezium top's y level.
_arc95_end_x = cx + 5 * s - cell / 2
_arc95_end_y = cy - 9 * s - cell / 2
arc_95 = (
    f'<path d="M {cx + 4 * s:.2f} {cy - 9 * s:.2f} '
    f'A {s:.2f} {s:.2f} 0 0 0 '
    f'{_arc95_end_x:.2f} {_arc95_end_y:.2f}" '
    f'fill="none"/>'
)
_lines95_top_y = _trap_top_y + 3 * cell / 2  # hairpin top aligned with trapezium top
vertical_95 = (
    f'<line x1="{_arc95_end_x:.2f}" y1="{_arc95_end_y:.2f}" '
    f'x2="{_arc95_end_x:.2f}" y2="{_lines95_top_y:.2f}"/>'
)
# Parallel vertical lines to the right (one cell apart, same y range).
vertical_95_extras = "\n  ".join(
    f'<line x1="{_arc95_end_x + k * cell:.2f}" y1="{_arc95_end_y:.2f}" '
    f'x2="{_arc95_end_x + k * cell:.2f}" y2="{_lines95_top_y:.2f}"/>'
    for k in (1, 2, 3)
)
svg_arc = svg_arc + "\n  " + arc_95 + "\n  " + vertical_95 + "\n  " + vertical_95_extras

# Arc joining (9, 4) (j=4 line endpoint) to the bottom of the right vertical
# line, tangent to both. Mirror geometry of the (4, 5) arc on the left side.
arc_94 = (
    f'<path d="M {cx + 5 * s:.2f} {cy - 8 * s:.2f} '
    f'A {cell + s:.2f} {cell + s:.2f} 0 0 0 '
    f'{_arc95_end_x + cell:.2f} {_arc95_end_y:.2f}" '
    f'fill="none"/>'
)
svg_arc = svg_arc + "\n  " + arc_94

# Hairpin bend at the top of the four right-side vertical lines.
# Outer arc connects lines 1 and 4 (chord 3·cell); inner arc connects lines
# 2 and 3 (chord cell). Both are 180° semicircles bulging up.
hairpin_outer = (
    f'<path d="M {_arc95_end_x:.2f} {_lines95_top_y:.2f} '
    f'A {3 * cell / 2:.2f} {3 * cell / 2:.2f} 0 0 1 '
    f'{_arc95_end_x + 3 * cell:.2f} {_lines95_top_y:.2f}" '
    f'fill="none"/>'
)
hairpin_inner = (
    f'<path d="M {_arc95_end_x + cell:.2f} {_lines95_top_y:.2f} '
    f'A {cell / 2:.2f} {cell / 2:.2f} 0 0 1 '
    f'{_arc95_end_x + 2 * cell:.2f} {_lines95_top_y:.2f}" '
    f'fill="none"/>'
)
svg_arc = svg_arc + "\n  " + hairpin_outer + "\n  " + hairpin_inner

# Sparśa consonants (5 vargas × 5) inside the 25 grid squares, rotated -45° so
# each character reads along the diagonal direction of its row. क sits in the
# square (0,5)-(1,4) at the left point of the diamond; म sits in the opposite
# square (4,1)-(5,0) at the right point.
_sparsha = [
    ["क", "ख", "ग", "घ", "ङ"],
    ["च", "छ", "ज", "झ", "ञ"],
    ["ट", "ठ", "ड", "ढ", "ण"],
    ["त", "थ", "द", "ध", "न"],
    ["प", "फ", "ब", "भ", "म"],
]
_consonant_elements = []
for varga_idx, row in enumerate(_sparsha):
    j_sq = 4 - varga_idx
    for i_sq, ch in enumerate(row):
        ex = cx + (i_sq - j_sq) * s
        ey = cy + n * s - (i_sq + j_sq + 1) * s
        _consonant_elements.append(
            f'<text x="{ex:.2f}" y="{ey:.2f}" font-size="36" '
            f'text-anchor="middle" dominant-baseline="central" '
            f'transform="rotate(-45 {ex:.2f} {ey:.2f})">{ch}</text>'
        )
svg_arc = svg_arc + "\n  " + "\n  ".join(_consonant_elements)

# Narrow central strip between the two cross-bars, divided into 5 equal sections
# by 4 vertical dividers. Each section holds one diacritic / yogavāha.
_hbar_upper_y = cy + 8 * s
_hbar_lower_y = cy + 9 * s
_hbar_section_w = cell
_hbar_total_w = 5 * _hbar_section_w
_hbar_left = cx - _hbar_total_w / 2
_hbar_chars = ["ँ", "ᳵ", "ᳶ", "ं", "ः"]

_hbar_dividers = "\n  ".join(
    f'<line x1="{_hbar_left + k * _hbar_section_w:.2f}" y1="{_hbar_upper_y:.2f}" '
    f'x2="{_hbar_left + k * _hbar_section_w:.2f}" y2="{_hbar_lower_y:.2f}"/>'
    for k in (1, 2, 3, 4)
)

_hbar_texts = "\n  ".join(
    f'<text x="{_hbar_left + (k + 0.5) * _hbar_section_w:.2f}" '
    f'y="{(_hbar_upper_y + _hbar_lower_y) / 2:.2f}" font-size="34" '
    f'text-anchor="middle" dominant-baseline="central">{ch}</text>'
    for k, ch in enumerate(_hbar_chars)
)

svg_arc = svg_arc + "\n  " + _hbar_dividers + "\n  " + _hbar_texts

# श ष स placed inside the 3 grid squares (i_sq=0, j_sq=-1,-2,-3) between the
# parallel i=0 and i=1 lines as they descend from प toward the upper cross-bar.
# Dividers are the j=-1 and j=-2 line segments crossing the strip.
_sib_div1 = (
    f'<line x1="{cx + s:.2f}" y1="{cy + 6 * s:.2f}" '
    f'x2="{cx + 2 * s:.2f}" y2="{cy + 5 * s:.2f}"/>'
)
_sib_div2 = (
    f'<line x1="{cx + 2 * s:.2f}" y1="{cy + 7 * s:.2f}" '
    f'x2="{cx + 3 * s:.2f}" y2="{cy + 6 * s:.2f}"/>'
)
_sib_centers = [("श", cx + 1 * s, cy + 5 * s),
                ("ष", cx + 2 * s, cy + 6 * s),
                ("स", cx + 3 * s, cy + 7 * s)]
_sib_text = "\n  ".join(
    f'<text x="{sx:.2f}" y="{sy:.2f}" font-size="34" '
    f'text-anchor="middle" dominant-baseline="central" '
    f'transform="rotate(-45 {sx:.2f} {sy:.2f})">{ch}</text>'
    for ch, sx, sy in _sib_centers
)
svg_arc = svg_arc + "\n  " + _sib_div1 + "\n  " + _sib_div2 + "\n  " + _sib_text

# ह in the parallelogram between the i=0 and i=1 lines, bounded above and below
# by the two horizontal cross-bars (sits just to the right of the visarga ः).
# Corners: (cx+3s, cy+8s), (cx+5s, cy+8s), (cx+6s, cy+9s), (cx+4s, cy+9s).
_ha_x = cx + 4.5 * s
_ha_y = (_hbar_upper_y + _hbar_lower_y) / 2
_ha_text = (
    f'<text x="{_ha_x:.2f}" y="{_ha_y:.2f}" font-size="34" '
    f'text-anchor="middle" dominant-baseline="central">ह</text>'
)
svg_arc = svg_arc + "\n  " + _ha_text

# Mirror of the right parallelogram: between j=0 and j=1 lines and the two
# cross-bars, on the left side. Contains ऌ upright.
# Corners: (cx-3s, cy+8s), (cx-5s, cy+8s), (cx-6s, cy+9s), (cx-4s, cy+9s).
_jna_x = cx - 4.5 * s
_jna_y = (_hbar_upper_y + _hbar_lower_y) / 2
_jna_text = (
    f'<text x="{_jna_x:.2f}" y="{_jna_y:.2f}" font-size="34" '
    f'text-anchor="middle" dominant-baseline="central">ऌ</text>'
)
svg_arc = svg_arc + "\n  " + _jna_text

# Strip between j=0 and j=1 (left side) divided into squares by 2 dividers
# (i=-1 and i=-2 segments). ॐ goes in the square just above the left
# parallelogram; क्ष goes one square further up. Rotated -45°.
_left_div1 = (
    f'<line x1="{cx - s:.2f}" y1="{cy + 6 * s:.2f}" '
    f'x2="{cx - 2 * s:.2f}" y2="{cy + 5 * s:.2f}"/>'
)
_left_div2 = (
    f'<line x1="{cx - 2 * s:.2f}" y1="{cy + 7 * s:.2f}" '
    f'x2="{cx - 3 * s:.2f}" y2="{cy + 6 * s:.2f}"/>'
)
_left_centers = [("क्ष", cx - 3 * s, cy + 7 * s),
                 ("ज्ञ", cx - 2 * s, cy + 6 * s)]
_left_text = "\n  ".join(
    f'<text x="{sx:.2f}" y="{sy:.2f}" font-size="34" '
    f'text-anchor="middle" dominant-baseline="central" '
    f'transform="rotate(-45 {sx:.2f} {sy:.2f})">{ch}</text>'
    for ch, sx, sy in _left_centers
)
svg_arc = svg_arc + "\n  " + _left_div1 + "\n  " + _left_div2 + "\n  " + _left_text

# Declension (vibhakti) affixes filling the strip from (5,5) along j=5/j=4
# (diagonal), through the tangent arc transition, up the vertical 1/vertical 2
# corridor, and around the LEFT half of the hairpin bend. Divided into 7 equal
# sections along the strip's centerline; one case per section (3 affixes each).
def _centerline_pt(t):
    L_diag = 4 * cell
    L_arc = (s + cell / 2) * math.pi / 4
    L_vert = _arc95_end_y - _lines95_top_y
    L_bend = cell * math.pi  # full 180° bend (left half + right half)
    if t < L_diag:
        return (cx + s / 2 + t / math.sqrt(2),
                cy - 4.5 * s - t / math.sqrt(2),
                -45.0)
    t -= L_diag
    if t < L_arc:
        cx0, cy0 = cx + 4 * s - cell / 2, cy - 9 * s - cell / 2
        R = s + cell / 2
        theta = math.radians(45 * (1 - t / L_arc))
        return (cx0 + R * math.cos(theta),
                cy0 + R * math.sin(theta),
                math.degrees(math.atan2(-math.cos(theta), math.sin(theta))))
    t -= L_arc
    if t < L_vert:
        return cx + 5 * s, _arc95_end_y - t, -90.0
    t -= L_vert
    if t < L_bend:
        bend_cx = _arc95_end_x + 1.5 * cell
        alpha = (t / L_bend) * math.pi
        return (bend_cx - cell * math.cos(alpha),
                _lines95_top_y - cell * math.sin(alpha),
                math.degrees(math.atan2(-math.cos(alpha), math.sin(alpha))))
    t -= L_bend
    # Descending v3/v4 corridor (centerline at x = cx + 5s + 2*cell)
    return cx + 5 * s + 2 * cell, _lines95_top_y + t, 90.0

_L_diag = 4 * cell
_L_arc = (s + cell / 2) * math.pi / 4
_L_vert = _arc95_end_y - _lines95_top_y  # length of v1/v2 (unchanged)
_L_bend = cell * math.pi
# Sup section (left side: diagonal + arc + v1/v2 corridor) holds 21 cells.
_L_sup = _L_diag + _L_arc + _L_vert
_sub_cell = _L_sup / 21
# TiN section (right side: v3/v4 corridor going down, extended) mirrors the
# 21 sup slots: top 18 hold tiN affixes, bottom 3 are extra (empty) slots.
_L_tin = 21 * _sub_cell
_t_tin_start = _L_sup + _L_bend
# v3 and v4 extend downward only as far as the bottom of the 18th tiN slot
# (the cell containing महिङ्); below that, a tapering "snake tail" replaces
# what would have been the 3 extra slots.
_tin_end_y = _lines95_top_y + 18 * _sub_cell
_v3v4_ext = "\n  ".join(
    f'<line x1="{_arc95_end_x + k * cell:.2f}" y1="{_arc95_end_y:.2f}" '
    f'x2="{_arc95_end_x + k * cell:.2f}" y2="{_tin_end_y:.2f}"/>'
    for k in (2, 3)
)
# Cone tapering from cell-wide at _tin_end_y down to a small rounded tip at
# the symmetric end of the strip (_lines95_top_y + 21 * _sub_cell).
_tail_tip_y = _lines95_top_y + _L_tin
_tail_v3_x = _arc95_end_x + 2 * cell
_tail_v4_x = _arc95_end_x + 3 * cell
_tail_mid_x = (_tail_v3_x + _tail_v4_x) / 2
_tail_tip_r = 0.2 * _sub_cell
_tail_path = (
    f'<path d="M {_tail_v3_x:.2f} {_tin_end_y:.2f} '
    f'L {_tail_mid_x - _tail_tip_r:.2f} {_tail_tip_y - _tail_tip_r:.2f} '
    f'A {_tail_tip_r:.2f} {_tail_tip_r:.2f} 0 0 0 '
    f'{_tail_mid_x + _tail_tip_r:.2f} {_tail_tip_y - _tail_tip_r:.2f} '
    f'L {_tail_v4_x:.2f} {_tin_end_y:.2f}" fill="none"/>'
)
svg_arc = svg_arc + "\n  " + _v3v4_ext + "\n  " + _tail_path

_affix_table_sup = [
    ["सु", "औ", "जस्"],
    ["अम्", "औट्", "शस्"],
    ["टा", "भ्याम्", "भिस्"],
    ["ङे", "भ्याम्", "भ्यस्"],
    ["ङसि", "भ्याम्", "भ्यस्"],
    ["ङस्", "ओस्", "आम्"],
    ["ङि", "ओस्", "सुप्"],
]
_affix_table_tin = [
    ["तिप्", "तस्", "झि"],
    ["सिप्", "थस्", "थ"],
    ["मिप्", "वस्", "मस्"],
    ["त", "आताम्", "झ"],
    ["थास्", "आथाम्", "ध्वम्"],
    ["इट्", "वहि", "महिङ्"],
]
_sup_affixes = [a for row in _affix_table_sup for a in row]
_tin_affixes = [a for row in _affix_table_tin for a in row]

def _divider_at(t):
    px, py, ang = _centerline_pt(t)
    ar = math.radians(ang)
    nx, ny = -math.sin(ar), math.cos(ar)
    return (f'<line x1="{px + cell / 2 * nx:.2f}" y1="{py + cell / 2 * ny:.2f}" '
            f'x2="{px - cell / 2 * nx:.2f}" y2="{py - cell / 2 * ny:.2f}"/>')

_strip_dividers = []
_strip_texts = []
# Sup section: 20 internal dividers + 21 affixes.
for _k in range(1, 21):
    _strip_dividers.append(_divider_at(_k * _sub_cell))
for _k, _affix in enumerate(_sup_affixes):
    _t = (_k + 0.5) * _sub_cell
    _px, _py, _ang = _centerline_pt(_t)
    _in_vert_up = _L_diag + _L_arc <= _t < _L_sup
    _rot = 0.0 if _in_vert_up else _ang
    _strip_texts.append(
        f'<text x="{_px:.2f}" y="{_py:.2f}" font-size="20" '
        f'text-anchor="middle" dominant-baseline="central" '
        f'transform="rotate({_rot:.2f} {_px:.2f} {_py:.2f})">{_affix}</text>'
    )
# TiN section: 18 internal dividers between the 18 tiN affixes plus a closing
# divider at the bottom of महिङ् (where the snake tail begins).
for _k in range(1, 19):
    _strip_dividers.append(_divider_at(_t_tin_start + _k * _sub_cell))
# Two extra dividers in the bend, symmetric about the apex. Their natural
# radial orientation makes the outer ends spread further apart than the inner
# ends (≈ 3:1 ratio because outer radius is 1.5·cell and inner is 0.5·cell).
_bend_mid = _L_sup + _L_bend / 2
_bend_off = _L_bend / 12
_strip_dividers.append(_divider_at(_bend_mid - _bend_off))
_strip_dividers.append(_divider_at(_bend_mid + _bend_off))
for _k, _affix in enumerate(_tin_affixes):
    _t = _t_tin_start + (_k + 0.5) * _sub_cell
    _px, _py, _ang = _centerline_pt(_t)
    _strip_texts.append(
        f'<text x="{_px:.2f}" y="{_py:.2f}" font-size="20" '
        f'text-anchor="middle" dominant-baseline="central">{_affix}</text>'
    )

svg_arc = svg_arc + "\n  " + "\n  ".join(_strip_dividers + _strip_texts)

svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      line, path {{ stroke:#000; stroke-width:2.2; stroke-linecap:round; fill:none; }}
    </style>
  </defs>
  <rect width="100%" height="100%" fill="#fff"/>
  {svg_lines}
  {svg_arc}
</svg>
"""

HERE = Path(__file__).resolve().parent
OUT = HERE / "bhojasala.svg"
OUT.write_text(svg, encoding="utf-8")
print(f"Wrote {OUT}")

PNG = HERE / "bhojasala.png"
_chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if Path(_chrome).exists():
    import subprocess
    # Chrome headless renders SVG with HarfBuzz, so Devanagari conjuncts and
    # combining marks (श्रीः, क्ष, ज्ञ, भ्याम्, etc.) shape correctly — unlike
    # cairosvg, which uses cairo's toy text API and can't shape complex scripts.
    subprocess.run(
        [_chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--screenshot={PNG}", f"--window-size={int(W)},{int(H)}",
         f"file://{OUT}"],
        check=True, capture_output=True,
    )
    print(f"Wrote {PNG}")
else:
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(PNG),
                         output_width=W, output_height=H)
        print(f"Wrote {PNG} (via cairosvg — Devanagari will not shape)")
    except Exception as e:
        print("Preview PNG not created:", e)
