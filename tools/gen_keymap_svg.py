"""Generate keymap.svg for torabo-tsuki LP (S/XS physical layout)."""
import sys
from html import escape

# (x, y, rot, rx, ry) from physical_layout_s, in 1/100 key units
POS = [
    (0, 60), (100, 25), (200, 0), (300, 13), (400, 25),
    (950, 25), (1050, 13), (1150, 0), (1250, 25), (1350, 60),
    (0, 160), (100, 125), (200, 100), (300, 113), (400, 125),
    (950, 125), (1050, 113), (1150, 100), (1250, 125), (1350, 160),
    (0, 260), (100, 225), (200, 200), (300, 213), (400, 225), (500, 240),
    (850, 240), (950, 225), (1050, 213), (1150, 200), (1250, 225), (1350, 260),
    (0, 360), (100, 325), (200, 300), (315, 350),
    (420, 350, 10, 420, 450), (522, 371, 20, 525, 470),
    (828, 371, -20, 925, 470), (930, 350, -10, 1030, 450),
    (1035, 350), (1150, 300), (1250, 325), (1350, 360),
]

# Each key: "" (empty), "tap", or ("tap", "hold"); prefix "#HELD#" = currently held layer key, "*" = new
L0 = [
    "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
    "A", "S", "D", "F", "G", "H", "J", "K", "L", ("-", "L1"),
    "Z", "X", "C", "V", "B", "Space", "B", "N", "M", ",", ".", ("/", "Shift"),
    "Ctrl", "Win", "Alt", ("英数", "Shift"), ("Space", "L1"), ("かな", "L3"),
    "BS", ("Enter", "L2"), "BS", "RAlt", "RWin", "RCtrl",
]
L1 = [
    "Tab", "", "", "", "", "*ホーム", "*直前の\nアプリ", "*アプリ\n一覧", "*通知", "",
    "Ctrl+A", "Ctrl+S", "右\nクリック", "左\nクリック", "", "*戻る", "左\nクリック", "右\nクリック", "*進む", "#HELD#L1",
    "Ctrl+Z", "Ctrl+X", "Ctrl+C", "Ctrl+V", "", "", "", "", "", "", "", "",
    "", "", "", "", "#HELD#L1", "", "", "Tab", "", "", "", "",
]
L2 = [
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
    "1", "2", "3", "4", "5", "{", "-", "=", "}", ":",
    "6", "7", "8", "9", "0", "", "", "_", "+", "[", "]", "＼",
    "", "", "", "", "*;", "", "", "#HELD#L2", "Del", "", "", "",
]
L3 = [
    "F1", "F2", "F3", "F4", "F5", "Home", "PgUp", "PgDn", "End", "Esc",
    "F6", "F7", "F8", "F9", "F10", "←", "↓", "↑", "→", "Tab",
    "F11", "F12", "USB\n出力", "BT\n出力", "BT\n次へ", "BT1\nMac", "BT2\nPad", "'", "\"", "`", "~", "|",
    "", "", "", "Del", "Tab", "#HELD#L3", "", "BT0\nデスクトップ", "", "", "BT3", "BT4",
]

LAYERS = [
    ("レイヤー0　基本", "", L0),
    ("レイヤー1　左親指Space長押し / 右小指 - 長押し", "トラックボール＝スクロール", L1),
    ("レイヤー2　右親指Enter長押し（数字・記号）", "", L2),
    ("レイヤー3　左親指かな長押し（F・矢印・Bluetooth）", "", L3),
]

COMBOS = [
    "J+K 同時押し：左クリック",
    "K+L 同時押し：右クリック",
    "U+I 同時押し：ホイールクリック",
    "S+D 同時押し：レイヤー4 ON/OFF（トラックボール横移動で戻る/進む）",
    "レイヤー2で + と [ 同時押し：Bluetooth接続をクリア",
]

S = 0.62          # px per unit
K = 100 * S       # key pitch
PAD = 3
LAYER_H = 330
W = int(1450 * S) + 40
FONT = "'Yu Gothic UI','Yu Gothic','Hiragino Sans','Noto Sans JP',sans-serif"

C = {
    "bg": "#ffffff", "key": "#f3f4f6", "stroke": "#c9ccd1", "text": "#1f2328",
    "hold": "#6b7280", "held": "#374151", "heldtext": "#ffffff",
    "new": "#dcfce7", "newstroke": "#16a34a", "empty": "#fafafa", "title": "#111827",
}


def key_svg(i, label, oy):
    p = POS[i]
    x, y = p[0] * S + 20, p[1] * S + oy
    tf = ""
    if len(p) == 5:
        tf = f' transform="rotate({p[2]} {p[3] * S + 20:.1f} {p[4] * S + oy:.1f})"'
    tap, hold = (label if isinstance(label, tuple) else (label, ""))
    fill, stroke, color = C["key"], C["stroke"], C["text"]
    if tap.startswith("#HELD#"):
        tap, fill, stroke, color = tap[6:] + "\n押下中", C["held"], C["held"], C["heldtext"]
    elif tap.startswith("*") and len(tap) > 1:
        tap, fill, stroke = tap[1:], C["new"], C["newstroke"]
    elif tap == "":
        fill = C["empty"]
    out = [f'<g{tf}>',
           f'<rect x="{x + PAD:.1f}" y="{y + PAD:.1f}" width="{K - 2 * PAD:.1f}" height="{K - 2 * PAD:.1f}" '
           f'rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>']
    lines = tap.split("\n")
    cx = x + K / 2
    cy = y + K / 2 - (6 if hold else 0)
    longest = max(len(l) for l in lines)
    fs = 15 if longest <= 3 else 12 if longest <= 5 else 10.5
    if len(lines) > 1:
        fs = min(fs, 12)
    start = cy - (len(lines) - 1) * fs * 0.6
    for n, line in enumerate(lines):
        out.append(f'<text x="{cx:.1f}" y="{start + n * fs * 1.2:.1f}" font-size="{fs}" fill="{color}" '
                   f'text-anchor="middle" dominant-baseline="central">{escape(line)}</text>')
    if hold:
        out.append(f'<text x="{cx:.1f}" y="{y + K - 12:.1f}" font-size="10" fill="{C["hold"]}" '
                   f'text-anchor="middle" dominant-baseline="central">長押し {escape(hold)}</text>')
    out.append("</g>")
    return "\n".join(out)


def main(path):
    total_h = 70 + LAYER_H * len(LAYERS) + 40 + 22 * len(COMBOS) + 30
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" '
         f'viewBox="0 0 {W} {total_h}" font-family="{FONT}">',
         f'<rect width="100%" height="100%" fill="{C["bg"]}"/>',
         f'<text x="20" y="34" font-size="22" font-weight="bold" fill="{C["title"]}">torabo-tsuki LP XS キーマップ</text>',
         f'<rect x="{W - 300}" y="18" width="18" height="18" rx="4" fill="{C["new"]}" stroke="{C["newstroke"]}"/>',
         f'<text x="{W - 276}" y="32" font-size="13" fill="{C["text"]}">Pad向けに追加</text>',
         f'<rect x="{W - 170}" y="18" width="18" height="18" rx="4" fill="{C["held"]}"/>',
         f'<text x="{W - 146}" y="32" font-size="13" fill="{C["text"]}">押さえるキー</text>']
    oy = 70
    for title, note, keys in LAYERS:
        o.append(f'<text x="20" y="{oy + 4}" font-size="16" font-weight="bold" fill="{C["title"]}">{escape(title)}</text>')
        if note:
            o.append(f'<text x="{W - 20}" y="{oy + 4}" font-size="13" fill="{C["hold"]}" text-anchor="end">{escape(note)}</text>')
        for i, label in enumerate(keys):
            o.append(key_svg(i, label, oy + 18))
        oy += LAYER_H
    o.append(f'<text x="20" y="{oy + 4}" font-size="16" font-weight="bold" fill="{C["title"]}">コンボ</text>')
    for n, c in enumerate(COMBOS):
        o.append(f'<text x="30" y="{oy + 30 + n * 22}" font-size="13" fill="{C["text"]}">・{escape(c)}</text>')
    o.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(o))


if __name__ == "__main__":
    main(sys.argv[1])
