#!/usr/bin/env python3
"""Generate tingantabandha.svg — a stylised Sanskrit verb conjugation table
laid out as a rotated diamond grid with snakes, triangle, ganas, and shlokas.

Run: python3 tingantabandha.py  →  writes tingantabandha.svg
"""

from pathlib import Path

FONT = "'Noto Sans Devanagari', 'Mangal', 'Sanskrit Text', serif"

# ---------------------------------------------------------------------------
# Cell contents (9 cols x 18 rows). Col 1 is hard-coded as a list below.
# ---------------------------------------------------------------------------

COL_DATA = [
    # col_x, comment, list of 18 endings (rows 1..18, P then A)
    (36, "व = लट्",
     ["ति", "तस्", "अन्ति", "सि", "थस्", "थ", "मि", "वस्", "मस्",
      "ते", "आते", "अन्ते", "से", "आथे", "ध्वे", "ए", "वहे", "महे"]),
    (108, "स = विधिलिङ्",
     ["यात्", "याताम्", "युस्", "यास्", "यातम्", "यात", "याम्", "याव", "याम्",
      "ईत", "ईयाताम्", "ईरन्", "ईथास्", "ईयाथाम्", "ईध्वम्", "ईय", "ईवहि", "ईमहि"]),
    (180, "वि = लोट्",
     ["तु", "ताम्", "अन्तु", "हि", "तम्", "त", "आनि", "आव", "आम",
      "ताम्", "आताम्", "अन्ताम्", "स्व", "आथाम्", "ध्वम्", "ऐ", "आवहै", "आमहै"]),
    (252, "ह्य = लङ्",
     ["त्", "ताम्", "अन्", "स्", "तम्", "त", "अम्", "व", "म",
      "त", "आताम्", "अन्त", "थास्", "आथाम्", "ध्वम्", "ई", "वहि", "महि"]),
    (324, "अ = लुङ्",
     ["त्", "ताम्", "अन्", "स्", "तम्", "त", "अम्", "व", "म",
      "त", "आताम्", "अन्त", "थास्", "आथाम्", "ध्वम्", "ई", "वहि", "महि"]),
    (396, "प = लिट्",
     ["अ", "अतुस्", "उस्", "थल्", "अथुस्", "अ", "अ", "व", "म",
      "ए", "आते", "इरे", "से", "आथे", "ध्वे", "ए", "वहे", "महे"]),
    (468, "स्व = लुट्",
     ["ता", "तारौ", "तारस्", "तासि", "तास्थस्", "तास्थ", "तास्मि", "तास्वस्", "तास्मस्",
      "ता", "तारौ", "तारस्", "तासे", "तासाथे", "ताध्वे", "ताहे", "तास्वहे", "तास्महे"]),
    (540, "आ = आशीर्लिङ्",
     ["यात्", "यास्ताम्", "यासुस्", "यास्", "यास्तम्", "यास्त", "यासम्", "यास्व", "यास्म",
      "सीष्ट", "सीयास्ताम्", "सीरन्", "सीष्ठास्", "सीयास्थाम्", "सीध्वम्", "सीय", "सीवहि", "सीमहि"]),
    (612, "भ = लृट्",
     ["स्यति", "स्यतस्", "स्यन्ति", "स्यसि", "स्यथस्", "स्यथ", "स्यामि", "स्यावस्", "स्यामस्",
      "स्यते", "स्येते", "स्यन्ते", "स्यसे", "स्येथे", "स्यध्वे", "स्ये", "स्यावहे", "स्यामहे"]),
    (684, "क्रि = लृङ्",
     ["स्यत्", "स्यताम्", "स्यन्", "स्यस्", "स्यतम्", "स्यत", "स्यम्", "स्याव", "स्याम्",
      "स्यत", "स्येताम्", "स्यन्त", "स्यथास्", "स्येथाम्", "स्यध्वम्", "स्ये", "स्यावहि", "स्यामहि"]),
]

COLUMN_HEADERS = ["व", "स", "वि", "ह्य", "अ", "प", "स्व", "आ", "भ", "क्रि"]

VERTICAL_COL_LABELS = [
    "वर्तमान = लट्",
    "सम्भावना = विधिलिङ्",
    "विधि = लोट्",
    "ह्यस्तन-अतीत = लङ्",
    "अतीत-सामान्य = लुङ्",
    "परोक्ष = लिट्",
    "श्वस्तन-भविष्यत् = लुट्",
    "आशीः = आशीर्लिङ्",
    "भविष्यत् = लृट्",
    "क्रियातिपत्ति / क्रियातिक्रम = लृङ्",
]

# 10 ganas: gana name, affix (or None if no affix), index in 1..10
GANAS = [
    ("भ्वादि", "अ"),
    ("अदादि", None),
    ("जुहोत्यादि", None),
    ("दिवादि", "यन्"),
    ("स्वादि", "नु"),
    ("तुदादि", "अ"),
    ("रुधादि", "न"),
    ("तनादि", "उ"),
    ("क्र्यादि", "ना"),
    ("चुरादि", "अय"),
]


def build_svg() -> str:
    lines = []
    a = lines.append

    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-525 -725 1850 2350" width="900" height="1143">')
    a('  <style>')
    a('    .grid { stroke: #222; stroke-width: 1.2; fill: none; }')
    a('    .loop { stroke: #222; stroke-width: 1.2; fill: none; }')
    a('  </style>')
    a('')
    a('  <g transform="rotate(-45 360 360)">')
    a('')

    # ----- Vertical grid lines (11) -----
    a('    <g class="grid">')
    for x in range(0, 720 + 1, 72):
        y1 = -252 if x == 720 else -40
        y2 = 1242 if x == 0 else 760
        a(f'      <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}"/>')
    a('    </g>')
    a('')

    # ----- Horizontal grid lines (19) -----
    a('    <g class="grid">')
    for y in range(0, 720 + 1, 40):
        x1 = -522 if y == 720 else -72
        x2 = 972 if y == 0 else 792
        a(f'      <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>')
    a('    </g>')
    a('')

    # ----- Top loops (r=36, inward). Pairs (0,72)...(576,648) -----
    a('    <g class="loop">')
    for x in (0, 144, 288, 432, 576):
        a(f'      <path d="M {x},-40 A 36,36 0 0,1 {x + 72},-40"/>')
    a('    </g>')
    a('')

    # ----- Bottom loops (r=36). Pairs (72,144)...(648,720) -----
    a('    <g class="loop">')
    for x in (72, 216, 360, 504, 648):
        a(f'      <path d="M {x},760 A 36,36 0 0,0 {x + 72},760"/>')
    a('    </g>')
    a('')

    # ----- Left loops (r=20). Pairs (0,40)...(640,680) -----
    a('    <g class="loop">')
    for y in range(0, 640 + 1, 80):
        a(f'      <path d="M -72,{y} A 20,20 0 0,0 -72,{y + 40}"/>')
    a('    </g>')
    a('')

    # ----- Triangle base -----
    a('    <line class="grid" x1="-522" y1="720" x2="0" y2="1242"/>')
    a('')

    # ----- Triangle arm loops (3 per arm, r=25.456) -----
    a('    <g class="loop">')
    for cx in (-435, -348, -261):
        a(f'      <circle cx="{cx}" cy="694.544" r="25.456"/>')
    for cy in (981, 1068, 1155):
        a(f'      <circle cx="25.456" cy="{cy}"  r="25.456"/>')
    a('    </g>')
    a('')

    # ----- Triangle-arm loop labels -----
    a(f'    <g font-family="{FONT}" text-anchor="middle" fill="#222" font-size="21">')
    for x, label in zip((-266, -353, -440), ("सन्", "य", "अय")):
        a(f'      <text x="{x}" y="700" transform="rotate(45 {x} 700)">{label}</text>')
    for y, label in zip((986, 1073, 1160), ("इयन्", "काम्य", "आय")):
        a(f'      <text x="20.456" y="{y}" transform="rotate(45 20.456 {y})">{label}</text>')
    a('    </g>')
    a('')

    # ----- Triangle-base affixes + interior label + gana names -----
    a(f'    <g font-family="{FONT}" text-anchor="middle" fill="#222" font-size="21">')
    # Affixes (only for ganas with an affix)
    affix_positions = [(-527, 761), (-365, 923), (-311, 977), (-257, 1031),
                       (-203, 1085), (-149, 1139), (-95, 1193), (-41, 1247)]
    affixes_to_render = [g[1] for g in GANAS if g[1] is not None]
    for (x, y), affix in zip(affix_positions, affixes_to_render):
        a(f'      <text x="{x}" y="{y}" transform="rotate(45 {x} {y})">{affix}</text>')

    # Triangle interior 3-line label
    for x, y, label in [(-65.2, 785.2, "तिङ्"), (-130.5, 850.5, "१६"), (-195.7, 915.7, "प्रत्यय")]:
        a(f'      <text x="{x}" y="{y}" font-size="27" transform="rotate(45 {x} {y})">{label}</text>')

    # Gana names, centred below each circle
    gana_positions = [(-557.4, 791.4), (-503.4, 845.4), (-449.4, 899.4), (-395.4, 953.4),
                      (-341.4, 1007.4), (-287.4, 1061.4), (-233.4, 1115.4),
                      (-179.4, 1169.4), (-125.4, 1223.4), (-71.4, 1277.4)]
    for (x, y), (name, _) in zip(gana_positions, GANAS):
        a(f'      <text x="{x}" y="{y}" transform="rotate(45 {x} {y})">{name}</text>')
    a('    </g>')
    a('')

    # ----- Triangle base circles (10) -----
    a('    <g class="loop">')
    for i in range(10):
        cx = -522 + 54 * i
        cy = 756 + 54 * i
        a(f'      <circle cx="{cx}" cy="{cy}" r="25.456"/>')
    a('    </g>')
    a('')

    # ----- Top inward segments (halved) -----
    a('    <line class="grid" x1="720" y1="-252" x2="762" y2="-210"/>')
    a('    <line class="grid" x1="930" y1="-42"  x2="972" y2="0"/>')
    a('')

    # ----- Right loops (r=20). Pairs (40,80)...(680,720) -----
    a('    <g class="loop">')
    for y in range(40, 680 + 1, 80):
        a(f'      <path d="M 792,{y} A 20,20 0 0,1 792,{y + 40}"/>')
    a('    </g>')
    a('')

    # ----- Top-row column headers (व स वि ...) -----
    a(f'    <g font-family="{FONT}" text-anchor="middle" fill="#222" font-size="27">')
    for i, ch in enumerate(COLUMN_HEADERS):
        a(f'      <text x="{36 + 72 * i}" y="-10">{ch}</text>')
    a('    </g>')
    a('')

    # ----- Row labels (परस्मैपद प्र, etc.) -----
    a(f'    <g font-family="{FONT}" text-anchor="end" fill="#222" font-size="27">')
    a('      <text x="-120" y="20">परस्मैपद<tspan dx="30">प्र</tspan></text>')
    a('      <text x="-120" y="140">म</text>')
    a('      <text x="-120" y="260">उ</text>')
    a('      <text x="-120" y="380">आत्मनेपद<tspan dx="30">प्र</tspan></text>')
    a('      <text x="-120" y="500">म</text>')
    a('      <text x="-120" y="620">उ</text>')
    a('    </g>')
    a('')

    # ----- Left-row numerals (१ २ ३ cycling for 18 rows) -----
    a(f'    <g font-family="{FONT}" text-anchor="middle" fill="#222" font-size="21">')
    cycle = ["१", "२", "३"]
    for i in range(18):
        a(f'      <text x="-32" y="{25 + 40 * i}">{cycle[i % 3]}</text>')
    a('    </g>')
    a('')

    # ----- Right-row numerals (१० for every row) -----
    a(f'    <g font-family="{FONT}" text-anchor="middle" fill="#222" font-size="21">')
    for i in range(18):
        a(f'      <text x="752" y="{25 + 40 * i}">१०</text>')
    a('    </g>')
    a('')

    # ----- ३० on every row where the left numeral is ३ (rows 3,6,9,12,15,18) -----
    a(f'    <g font-family="{FONT}" text-anchor="middle" fill="#222" font-size="27">')
    for row_idx in range(2, 18, 3):  # 0-based: rows 3,6,9,12,15,18 → 2,5,8,11,14,17
        a(f'      <text x="842" y="{25 + 40 * row_idx}">३०</text>')
    a('    </g>')
    a('')

    # ----- Cell contents (162 endings) -----
    a(f'    <g font-family="{FONT}" text-anchor="middle" fill="#222" font-size="21">')
    for col_x, label, endings in COL_DATA:
        a(f'      <!-- Col x={col_x}: {label} -->')
        for i, ending in enumerate(endings):
            a(f'      <text x="{col_x}" y="{25 + 40 * i}">{ending}</text>')
    a('    </g>')
    a('')

    # ----- Vertical column labels (page-horizontal in display via local rotate(45)) -----
    a(f'    <g font-family="{FONT}" text-anchor="end" fill="#222" font-size="18">')
    for i, label in enumerate(VERTICAL_COL_LABELS):
        x = 36 + 72 * i
        a(f'      <text x="{x}" y="-90" transform="rotate(45 {x} -90)">{label}</text>')
    a('    </g>')
    a('')

    a('  </g>')  # close rotation group
    a('')

    # ===== OUTSIDE ROTATION GROUP =====

    # ----- Snakes -----
    a('  <g class="loop">')
    a('    <!-- Left side: HEAD of the snake. -->')
    a('    <path d="M 241.3 -327.3 A 34.64 34.64 0 0 0 241.3 -387.3 A 25.64 25.64 0 0 1 271.3 -437.3 A 30.78 30.78 0 0 0 215.3 -440.3 A 50.64 50.64 0 0 0 210.3 -422.3 A 73.5 73.5 0 0 0 240.3 -370.3 A 35.40 35.40 0 0 1 241.3 -327"/>')
    a('    <circle cx="243.3" cy="-450" r="2"/>')
    a('    <!-- Right side: TAIL. -->')
    a('    <path d="M 478.7 -327.3 A 34.64 34.64 0 0 1 478.7 -387.3 A 34.64 34.64 0 0 0 478.7 -447.3"/>')
    a('  </g>')
    a('')

    # ----- Bottom-corner extensions + 225° tangent arcs -----
    a('  <g class="loop">')
    a('    <line x1="-9" y1="1238" x2="-77.28427" y2="1306.28427"/>')
    a('    <line x1="-9" y1="1238" x2="-105.56854" y2="1238"/>')
    a('    <path d="M -77.28427 1306.28427 A 40 40 0 1 1 -105.56854 1238"/>')
    a('    <line x1="729" y1="1238" x2="797.28427" y2="1306.28427"/>')
    a('    <line x1="729" y1="1238" x2="825.56854" y2="1238"/>')
    a('    <path d="M 797.28427 1306.28427 A 40 40 0 1 0 825.56854 1238"/>')
    a('  </g>')
    a('')

    # ----- Sanskrit verses + अथ श्रीः धातुः -----
    a(f'  <g font-family="{FONT}" text-anchor="middle" fill="#222">')
    verses = [
        (-628, "इयम् उदयादित्य-नरवर्म-महीभुजोः ।"),
        (-596, "महेशस्वामिनोर्वर्णस्थित्यै सिद्धासिपुत्रिका ॥"),
        (-548, "उदयादित्यदेवस्य वर्णनागकृपाणिका ।"),
        (-516, "कवीनां च नृपाणां च वेषो वक्षसि रोपितः ॥"),
    ]
    for y, verse in verses:
        a(f'    <text x="360" y="{y}" font-size="30">{verse}</text>')
    for y, word in [(-367, "अथ"), (-399, "श्रीः"), (-431, "धातुः")]:
        a(f'    <text x="360" y="{y}" font-size="30">{word}</text>')
    a('  </g>')

    a('</svg>')
    return "\n".join(lines) + "\n"


def main():
    out_path = Path(__file__).parent / "tingantabandha.svg"
    out_path.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
