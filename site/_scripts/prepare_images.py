"""Resize/compress source photos into the site's assets/img folder.
One-off local prep script (not deployed). Run with: python prepare_images.py
"""
import os
from PIL import Image, ImageOps

SRC_POOL = r"F:\사진 모음\시공사진\Pool"
SRC_BRAND = r"F:\OHT\Ai\LLM Wiki Ux\Project\.claude\skills\theallform-visual-marketing-skill\assets\brand\logo box-final.jpg"
SRC_PRODUCTS = r"F:\OHT\Ai\LLM Wiki Ux\Project\.claude\skills\theallform-visual-marketing-skill\assets\products"
OUT_ROOT = r"F:\OHT\Ai\LLM Wiki Ux\Project\homepage\site\assets\img"

def save_resized(src, dst, max_w, quality=78):
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    if img.width > max_w:
        h = int(img.height * (max_w / img.width))
        img = img.resize((max_w, h), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    img.save(dst, "JPEG", quality=quality, optimize=True)
    print(f"{dst}  {img.width}x{img.height}  {os.path.getsize(dst)//1024}KB")

# Hero image
save_resized(
    os.path.join(SRC_POOL, "01 강남구 도곡동500 베이비브라운 (1).jpg"),
    os.path.join(OUT_ROOT, "hero", "hero-gangnam-dogok.jpg"),
    2400, 80,
)

# Logo (kept modest size; used as small square badge)
save_resized(SRC_BRAND, os.path.join(OUT_ROOT, "logo", "afm-logo.jpg"), 400, 90)

# 시공사례 gallery: one representative shot per project, spread across colors/regions
gallery = [
    ("01 강남구 도곡동500 베이비브라운 (3).jpg", "gangnam-dogok.jpg"),
    ("03 관악구 낙성대 낙성벤처타운 500 그레이 (2).jpg", "gwanak-nakseongdae.jpg"),
    ("06 노원구 공릉동 500ㅣ 베이비블랙 (1).jpg", "nowon-gongneung.jpg"),
    ("08 마포구 염리동 베브라운 타일 (2).jpg", "mapo-yeomri.jpg"),
    ("21 용인시 기흥구 동백동 390 매직브라운 (3).jpg", "yongin-dongbaek.jpg"),
    ("23 용인시 수지구 고기동  매직브라운 타일 (5).jpg", "yongin-gogi.jpg"),
    ("28 인천 서구 청라동 500 베브라운 (2).jpg", "incheon-cheongna.jpg"),
    ("33 종로구 평창동 500  그레이 매직블랙 (3).jpg", "jongno-pyeongchang.jpg"),
    ("20 영등포구 당산동 390 그레이 (4).jpg", "yeongdeungpo-dangsan.jpg"),
    ("14 서초구 잠원동 500 베이비브라운 (2).jpg", "seocho-jamwon.jpg"),
]
for fname, out in gallery:
    save_resized(os.path.join(SRC_POOL, fname), os.path.join(OUT_ROOT, "projects", out), 1400, 76)

# Product color swatches (wide brick)
wb_src = os.path.join(SRC_PRODUCTS, "wide-brick")
swatches = ["Gray.png", "Red.png", "Black.png", "Brown.png", "green.png", "BBlack.png", "Bbrown.png"]
for s in swatches:
    p = os.path.join(wb_src, s)
    if os.path.exists(p):
        img = Image.open(p)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        if img.width > 500:
            h = int(img.height * (500 / img.width))
            img = img.resize((500, h), Image.LANCZOS)
        out_path = os.path.join(OUT_ROOT, "products", "wide-brick", s.lower())
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        img.save(out_path, "PNG", optimize=True)
        print(f"{out_path}  {img.width}x{img.height}")

# Design block patterns (front-facing only)
db_src = os.path.join(SRC_PRODUCTS, "design-block")
db_pick = ["D-02(F)-1.png", "D-03(F).png", "D-05(F).png", "D-9(F).png", "D-11(F).jpg"]
for s in db_pick:
    p = os.path.join(db_src, s)
    if os.path.exists(p):
        img = Image.open(p)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        if img.width > 700:
            h = int(img.height * (700 / img.width))
            img = img.resize((700, h), Image.LANCZOS)
        ext = "png" if img.mode == "RGBA" else "jpg"
        out_path = os.path.join(OUT_ROOT, "products", "design-block", os.path.splitext(s)[0].lower().replace("(", "").replace(")", "") + "." + ext)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        if ext == "jpg":
            img = img.convert("RGB")
            img.save(out_path, "JPEG", quality=85, optimize=True)
        else:
            img.save(out_path, "PNG", optimize=True)
        print(f"{out_path}  {img.width}x{img.height}")

# Cutting products (컷팅제품) — real jobsite + studio cutout photos
cut_meeting_src = r"F:\사진 모음\미팅용 사진 정리\컷팅벽돌_타일"
cut_product_src = r"F:\사진 모음\컷팅제품\180\누끼"
cutting_jobsite = [
    ("KakaoTalk_20250723_133919413_06.jpg", "hero-facade.jpg", 2000),
    ("KakaoTalk_20250723_133919413_07.jpg", "detail-corner.jpg", 1400),
    ("20190107_134244.jpg", "context-corridor.jpg", 1400),
]
for fname, out, max_w in cutting_jobsite:
    save_resized(os.path.join(cut_meeting_src, fname), os.path.join(OUT_ROOT, "products", "cutting", out), max_w, 78)

cutting_cutouts = [("AWR-180G.jpg", "cut-gray.jpg"), ("AWR-180BMK.jpg", "cut-black.jpg"), ("AWR-180R.jpg", "cut-red.jpg")]
for fname, out in cutting_cutouts:
    save_resized(os.path.join(cut_product_src, fname), os.path.join(OUT_ROOT, "products", "cutting", out), 500, 88)

print("done")
