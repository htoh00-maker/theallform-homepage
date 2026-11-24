"""제품 상세페이지용 이미지 — 2026 브로셔 PDF에서 잘라낸다 (배포 대상 아님).
실행: python prepare_brochure_images.py

원본: Design Form/2026 브로셔/최종결과/브로셔_2026_더올포엠_통합.pdf (읽기만 함)
  - 페이지의 글자를 메모리 안에서만 지운 뒤(사진 위 색상명 등) 사진 영역을 색 보정(ICC) 켜고 렌더링.
  - 좌표는 PDF 포인트(가로 595 x 세로 842) 기준.
디자인블록 첫 화면: F:/사진 모음/디자인블록/DB 상세페이지/메인사진최종.png (투명 배경 → #f4f4f4 위에 합성)
출력: ../assets/img/
"""
import os

import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.normpath(os.path.join(HERE, "..", "..", "..", "2026 브로셔", "최종결과", "브로셔_2026_더올포엠_통합.pdf"))
BLOCK_HERO = r"F:\사진 모음\디자인블록\DB 상세페이지\메인사진최종.png"
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "img"))
PAPER = (244, 244, 244)  # style.css --paper
KEEP_TEXT = {6, 10}  # 치수 숫자가 그림의 일부인 쪽
# 페이지 위 도형(NEW 상자)이 겹쳐서, PDF 안의 원본 사진을 그대로 꺼내 쓰는 것: 이름: (쪽, 저장 가로폭)
RAW = {"wt-product": (9, 1600)}  # 와이드타일 5색 제품 사진

FULL = (0, 0, 595.28, 482)  # 각 장 표지 사진 영역

# 이름: (쪽, 영역, 저장 가로폭 목록)
CLIPS = {
    # 첫 화면 (브로셔 각 장 표지)
    "wb-hero-sujeong": (4, FULL, (2400, 1200)),     # 와이드벽돌 500 매직그레이 · 경기 성남시 수정구
    "wt-hero-unyang": (8, FULL, (2400, 1200)),      # 와이드타일 500 베이비브라운 · 경기 김포시 운양동
    "cut-hero-mix": (18, FULL, (2400, 1200)),       # 컷팅 와이드벽돌 Mix
    # 와이드벽돌 — 길이별 치수 그림 (6쪽, 회색 상자 단위 · 치수 숫자 유지)
    "wb-size-500": (6, (43, 166, 291, 336), (900,)),
    "wb-size-390": (6, (305, 166, 553, 336), (900,)),
    "wb-size-340": (6, (43, 463, 291, 634), (900,)),
    "wb-size-300": (6, (305, 463, 553, 634), (900,)),
    # 와이드벽돌 — 색상 (5쪽)
    "wb-color-mgray": (5, (43, 326, 203, 399), (700,)),
    "wb-color-bblack": (5, (217, 325, 378, 399), (700,)),
    "wb-color-mblack": (5, (392, 324, 553, 401), (700,)),
    "wb-color-bbrown": (5, (43, 552, 203, 626), (700,)),
    "wb-color-mbrown": (5, (217, 552, 378, 626), (700,)),
    "wb-color-mred": (5, (392, 552, 553, 627), (700,)),
    # 와이드타일 (9 · 11쪽)
    "wt-size-500": (10, (43, 261, 291, 417), (900,)),   # 치수 그림 (10쪽)
    "wt-size-390": (10, (43, 431, 291, 587), (900,)),
    "wt-size-corner": (10, (43, 601, 291, 757), (900,)),
    "wt-color-mgray": (11, (43, 260, 212, 429), (700,)),
    "wt-color-bbrown": (11, (213, 260, 382, 430), (700,)),
    "wt-color-mbrown": (11, (384, 260, 554, 430), (700,)),
    "wt-color-mred": (11, (43, 431, 212, 598), (700,)),
    "wt-color-mblack": (11, (384, 431, 554, 601), (700,)),
    "wt-color-bblack": (11, (41, 601, 212, 771), (700,)),
    "wt-corner": (11, (384, 601, 553, 772), (700,)),
    "wt-mix": (11, (213, 431, 382, 771), (700,)),
    # 디자인블록 (13~17쪽) — f: 앞면, b: 뒷면
    "db-intro": (13, (43, 71, 552, 496), (1600,)),
    "db-02-f": (14, (60, 206, 196, 342), (600,)),
    "db-02-b": (14, (335, 206, 471, 342), (600,)),
    "db-03-f": (14, (60, 590, 238, 687), (600,)),
    "db-03-b": (14, (335, 591, 513, 686), (600,)),
    "db-04-f": (15, (71, 227, 184, 322), (600,)),
    "db-04-b": (15, (345, 228, 460, 321), (600,)),
    "db-05-f": (15, (71, 588, 184, 689), (600,)),
    "db-05-b": (15, (346, 592, 459, 685), (600,)),
    "db-06-f": (16, (60, 263, 238, 359), (600,)),
    "db-06s-f": (16, (335, 280, 513, 344), (600,)),
    "db-07-f": (16, (60, 612, 238, 664), (600,)),
    "db-07-b": (16, (335, 613, 513, 664), (600,)),
    "db-09-f": (17, (57, 249, 241, 300), (600,)),
    "db-09-b": (17, (339, 250, 509, 299), (600,)),
    "db-11-f": (17, (71, 588, 184, 688), (600,)),
    "db-11-b": (17, (346, 589, 459, 687), (600,)),
    # 컷팅제품 (19~21쪽)
    "cut-wall-mix": (19, (305, 167, 553, 338), (1000,)),
    "cut-tile-stack": (19, (304, 464, 554, 635), (1000,)),
    "cut-brick-product": (20, (42, 41, 554, 407), (1600,)),
    "cut-tile-product": (21, (42, 41, 554, 406), (1600,)),
    "cut-chip-mgray": (20, (42, 715, 84, 739), (240,)),
    "cut-chip-bblack": (20, (88, 715, 130, 740), (240,)),
    "cut-chip-mblack": (20, (136, 715, 177, 739), (240,)),
    "cut-chip-bbrown": (20, (181, 715, 223, 739), (240,)),
    "cut-chip-mbrown": (20, (228, 715, 270, 739), (240,)),
    "cut-chip-mred": (20, (276, 715, 317, 739), (240,)),
    "cut-chip-mgreen": (20, (321, 715, 363, 739), (240,)),
}


def save(im, name, width):
    w, h = im.size
    if w > width:
        im = im.resize((width, round(h * width / w)), Image.LANCZOS)
    suffix = f"-{width}" if name.endswith(("hero-sujeong", "hero-unyang", "hero-mix", "db-hero")) else ""
    im.save(os.path.join(OUT, f"{name}{suffix}.jpg"), quality=84, optimize=True, progressive=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    pymupdf.TOOLS.set_icc(True)
    doc = pymupdf.open(PDF)  # 메모리에서만 수정, 저장 안 함
    cleaned = set()
    for name, (pno, rect, widths) in CLIPS.items():
        page = doc[pno - 1]
        if pno not in cleaned and pno not in KEEP_TEXT:  # 글자만 지우고 사진·도형은 유지
            for b in page.get_text("blocks"):
                page.add_redact_annot(pymupdf.Rect(b[:4]))
            page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
            cleaned.add(pno)
        clip = pymupdf.Rect(rect) & page.rect
        dpi = max(150, min(600, round(max(widths) / clip.width * 72 * 1.05)))
        pix = page.get_pixmap(dpi=dpi, clip=clip, alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        for wdt in widths:
            save(im, name, wdt)
        print(f"{name}: p{pno} {im.size} -> {widths}")

    for name, (pno, width) in RAW.items():
        xref = max(doc[pno - 1].get_images(), key=lambda i: i[2] * i[3])[0]
        pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.Pixmap(doc, xref))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        save(im, name, width)
        print(f"{name}: p{pno} raw {im.size}")

    hero = Image.open(BLOCK_HERO).convert("RGBA")
    bg = Image.new("RGBA", hero.size, PAPER + (255,))
    flat = Image.alpha_composite(bg, hero).convert("RGB")
    for wdt in (2400, 1200):
        save(flat, "db-hero", wdt)
    print("db-hero:", hero.size)


if __name__ == "__main__":
    main()
