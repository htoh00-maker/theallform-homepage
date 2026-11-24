"""site-v2 이미지 준비 (배포 대상 아님). 실행: python prepare_images.py

원본: Design Form/2026 브로셔/포트폴리오_보정/웹용_sRGB (수직·톤 보정 완료, 건물색 유지 검사 통과본)
출력: ../assets/img/<이름>-2400.jpg, <이름>-1200.jpg  (srcset 용)
캡션은 브로셔 '포트폴리오 추춘.pdf' 원문에서 확인한 제품명·현장 위치.
"""
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE = Design Form/homepage/site-v2/_scripts
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "2026 브로셔", "포트폴리오_보정", "웹용_sRGB"))
OLD = os.path.normpath(os.path.join(HERE, "..", "..", "site", "assets", "img"))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "img"))

# 이름: (원본 파일, 크기 목록)
IMAGES = {
    "hero-pyeongchang": ("page 60 (1).jpg", (2400, 1200)),       # 와이드 500 매직블랙 · 서울 종로구 평창동
    "brick-hapjeong": ("page 36-37 (1).jpg", (2400, 1200)),      # 와이드 390 매직레드 · 서울 마포구 합정동 (2026 브로셔 7·44쪽 기준, 옛 포트폴리오는 340)
    "tile-cheongna": ("page 55 (2).jpg", (2400, 1200)),          # 타일 500 베이비브라운 · 인천 서구 청라동
    "block-ilsan": ("page 52-53 (2).jpg", (2400, 1200)),         # 디자인블록 02번 · 경기 고양시 일산서구
    "color-dongtan": ("page 56 (1).jpg", (2400, 1200)),          # 와이드 500 5색 · 경기 화성시 동탄
    "case-sujeong": ("page 24-25 (1).JPG", (1200,)),             # 와이드 500 매직그레이 · 경기 성남시 수정구
    "case-bundang": ("page 30-31 (2).JPG", (1200,)),             # 와이드 390 매직레드 · 경기 성남시 분당구
    "case-dongbaek": ("page 57 (1).jpg", (1200,)),               # 와이드 390 매직브라운 · 경기 용인시 동백동
    "case-dongcheon": ("page 58 (2).jpg", (1200,)),              # 와이드 500 매직그레이/매직레드 · 경기 용인시 수지구 동천동
    "case-yangpyeong": ("page 61 (1).jpg", (1200,)),             # 와이드 500 매직블랙 · 경기 양평군
    "case-jecheon": ("page 38 (1).JPG", (1200,)),                # 디자인블록 04번 · 충북 제천시 송학면
    # 하위 페이지용 (파일명에 현장·제품이 적힌 보정본)
    "brick-junggye": ("추가 중계동 390 매직브라운 (1).jpg", (2400, 1200)),   # 와이드 390 매직브라운 · 서울 노원구 중계동
    "block-baekseok": ("추가 천안 백석대 블록02 (1).jpg", (2400, 1200)),   # 디자인블록 02번 · 충남 천안 백석대학교
    "block-baekseok-v": ("추가 천안 백석대 블록02 (3).jpg", (1200,)),
}

# 하위 페이지용 — 기존 site/ 자산 재사용 (캡션은 site/ 원래 표기, 1400px 이하라 카드 크기로만 사용)
OLD_COPIES = {
    "case-dogok": "projects/gangnam-dogok.jpg",              # 500 베이비브라운 · 서울 강남구 도곡동
    "case-nakseongdae": "projects/gwanak-nakseongdae.jpg",   # 500 그레이 · 서울 관악구 낙성대
    "case-gongneung": "projects/nowon-gongneung.jpg",        # 500 베이비블랙 · 서울 노원구 공릉동
    "case-yeomri": "projects/mapo-yeomri.jpg",               # 와이드타일 베이비브라운 · 서울 마포구 염리동
    "case-gogi": "projects/yongin-gogi.jpg",                 # 와이드타일 매직브라운 · 용인 수지구 고기동
    "case-dangsan": "projects/yeongdeungpo-dangsan.jpg",     # 390 그레이 · 서울 영등포구 당산동
    "case-jamwon": "projects/seocho-jamwon.jpg",             # 500 베이비브라운 · 서울 서초구 잠원동
    "cut-corner": "products/cutting/detail-corner.jpg",      # 컷팅벽돌 코너 디테일
    "cut-corridor": "products/cutting/context-corridor.jpg", # 컷팅벽돌 통로 입면
}
# 그대로 복사 (작은 제품 사진·절단면)
OLD_RAW = {
    "cut-gray.jpg": "products/cutting/cut-gray.jpg",
    "cut-red.jpg": "products/cutting/cut-red.jpg",
    "cut-black.jpg": "products/cutting/cut-black.jpg",
    "block-02.png": "products/design-block/d-02f-1.png",
    "block-03.jpg": "products/design-block/d-03f.jpg",
    "block-05.jpg": "products/design-block/d-05f.jpg",
    "block-09.png": "products/design-block/d-9f.png",
    "block-11.jpg": "products/design-block/d-11f.jpg",
}


def save(im, name, width):
    w, h = im.size
    if w > width:
        im = im.resize((width, round(h * width / w)), Image.LANCZOS)
    im.save(os.path.join(OUT, f"{name}-{width}.jpg"), quality=82, optimize=True, progressive=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (src, widths) in IMAGES.items():
        stem = os.path.splitext(src)[0]
        im = Image.open(os.path.join(SRC, stem + ".jpg")).convert("RGB")
        for wdt in widths:
            save(im, name, wdt)
    # 기존 사이트 자산 재사용 (컷팅제품 히어로, 로고, 컬러칩)
    save(Image.open(os.path.join(OLD, "products", "cutting", "hero-facade.jpg")).convert("RGB"), "cutting-facade", 2000)
    save(Image.open(os.path.join(OLD, "products", "cutting", "hero-facade.jpg")).convert("RGB"), "cutting-facade", 1200)
    Image.open(os.path.join(OLD, "logo", "afm-logo.jpg")).save(os.path.join(OUT, "afm-logo.jpg"), quality=90)
    for chip in ("gray", "black", "bblack", "brown", "bbrown", "red", "green"):
        Image.open(os.path.join(OLD, "products", "wide-brick", chip + ".png")).save(os.path.join(OUT, f"chip-{chip}.png"))
    for name, rel in OLD_COPIES.items():
        save(Image.open(os.path.join(OLD, rel)).convert("RGB"), name, 1200)
    for name, rel in OLD_RAW.items():
        shutil.copyfile(os.path.join(OLD, rel), os.path.join(OUT, name))
    print("done:", len(os.listdir(OUT)), "files")


if __name__ == "__main__":
    main()
