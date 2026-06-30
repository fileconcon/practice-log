# Cue Note 用アイコン生成（8ボール + キュー）。出力: icons/*.png
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = os.path.join(os.path.dirname(__file__), "icons")
os.makedirs(OUT, exist_ok=True)

BG = (10, 14, 10)            # アプリ背景
GREEN = (61, 220, 132)       # アクセント
BLACK = (18, 18, 18)         # 8ボール
WHITE = (245, 245, 245)      # 番号パッチ
TIP = (62, 110, 200)         # キュー先端（青チョーク）
SHAFT = (220, 200, 165)      # シャフト（薄ベージュ）
GRIP = (45, 45, 50)          # グリップ

FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"


def make(size, ball_frac, ring=True, cue=True):
    s = size * 4  # 高解像度で描いて縮小（アンチエイリアス）
    img = Image.new("RGB", (s, s), BG)
    d = ImageDraw.Draw(img)
    cx = cy = s / 2
    R = s * ball_frac / 2

    if ring:
        rg = R + s * 0.045
        d.ellipse([cx - rg, cy - rg, cx + rg, cy + rg],
                  outline=GREEN, width=int(s * 0.022))

    # 8ボール（黒）
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BLACK)
    # 上部のハイライト
    hr = R * 0.55
    hx, hy = cx, cy - R * 0.45
    d.ellipse([hx - hr, hy - hr * 0.7, hx + hr, hy + hr * 0.7], fill=(55, 55, 55))
    # 白の番号パッチ
    wp = R * 0.46
    d.ellipse([cx - wp, cy - wp, cx + wp, cy + wp], fill=WHITE)
    # "8"
    font = ImageFont.truetype(FONT_PATH, int(R * 0.66))
    bbox = d.textbbox((0, 0), "8", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), "8", font=font, fill=BLACK)

    if cue:
        # キュー：左下→右上方向。先端を球の左下表面に接触させる
        angle = math.radians(45)  # 右上方向の単位ベクトル
        # 先端位置（球の左下表面）：球中心から-45度方向にRだけ離れた点
        tip_x = cx - R * math.cos(angle)
        tip_y = cy + R * math.sin(angle)
        # キュー全長
        length = R * 2.4
        # 各セグメント長
        tip_len = length * 0.04   # 青チョーク
        sh_len  = length * 0.62   # シャフト
        # 先端→チョーク終わり
        ax = tip_x - tip_len * math.cos(angle)
        ay = tip_y + tip_len * math.sin(angle)
        # チョーク終わり→シャフト終わり
        bx = ax - sh_len * math.cos(angle)
        by = ay + sh_len * math.sin(angle)
        # シャフト終わり→末端
        cx2 = tip_x - length * math.cos(angle)
        cy2 = tip_y + length * math.sin(angle)
        # 描画
        d.line([(tip_x, tip_y), (ax, ay)], fill=TIP, width=int(s * 0.020))
        d.line([(ax, ay), (bx, by)], fill=SHAFT, width=int(s * 0.022))
        d.line([(bx, by), (cx2, cy2)], fill=GRIP, width=int(s * 0.026))

    return img.resize((size, size), Image.LANCZOS)


# 通常アイコン
make(512, 0.62).save(os.path.join(OUT, "icon-512.png"))
make(192, 0.62).save(os.path.join(OUT, "icon-192.png"))
# maskable（中央セーフゾーン）
make(512, 0.50, ring=True).save(os.path.join(OUT, "icon-maskable-512.png"))
# iOS apple-touch-icon
make(180, 0.62).save(os.path.join(OUT, "apple-touch-icon.png"))
# favicon（小さいのでキュー省略）
make(32, 0.74, ring=False, cue=False).save(os.path.join(OUT, "favicon-32.png"))

print("icons generated:", os.listdir(OUT))
