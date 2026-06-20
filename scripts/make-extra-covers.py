"""Generate cabin + low-carb original/modern cover pairs."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# Pumpkin-cookies notebook page — clearest cabin photo, title at top
CABIN_SRC = ROOT / "assets" / "cabin" / "Resized_20170915_205400001.jpeg"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def compose_mockup(card: Image.Image, pad: int = 48) -> Image.Image:
    card = card.convert("RGB")
    canvas = Image.new("RGB", (card.width + pad * 2, card.height + pad * 2), "#d4d0c8")
    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle((0, 0, card.width - 1, card.height - 1), fill=(10, 8, 6, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.paste(shadow, (pad + 12, pad + 14), shadow)
    canvas.paste(card, (pad, pad))
    return canvas


def trim_to_paper(img: Image.Image) -> Image.Image:
    """Crop to the bright notebook page, dropping table/floor edges."""
    gray = img.convert("L")
    mask = gray.point(lambda p: 255 if p > 150 else 0)
    mask = mask.filter(ImageFilter.MaxFilter(15))
    bbox = mask.getbbox()
    if not bbox:
        return img
    left, top, right, bottom = bbox
    pad_x = int((right - left) * 0.02)
    pad_y = int((bottom - top) * 0.02)
    left = max(0, left - pad_x)
    top = max(0, top - pad_y)
    right = min(img.width, right + pad_x)
    bottom = min(img.height, bottom + pad_y)
    return img.crop((left, top, right, bottom))


def fit_cover(img: Image.Image, target: tuple[int, int] = (918, 1224)) -> Image.Image:
    """Center-crop to 3:4, then resize — keeps the title readable in the hero."""
    tw, th = target
    ratio = tw / th
    w, h = img.size
    current = w / h
    if current > ratio:
        new_w = int(h * ratio)
        x0 = (w - new_w) // 2
        img = img.crop((x0, 0, x0 + new_w, h))
    else:
        new_h = int(w / ratio)
        y0 = max(0, (h - new_h) // 4)  # bias crop toward title at top
        img = img.crop((0, y0, w, min(h, y0 + new_h)))
    return img.resize(target, Image.Resampling.LANCZOS)


def polish_photo(img: Image.Image, *, modern: bool) -> Image.Image:
    out = ImageEnhance.Contrast(img).enhance(1.08 if modern else 1.04)
    out = ImageEnhance.Brightness(out).enhance(1.03 if modern else 1.01)
    out = ImageEnhance.Color(out).enhance(1.05 if modern else 1.02)
    if modern:
        out = ImageEnhance.Sharpness(out).enhance(1.35)
    return out


def draw_cabin_modern_cover() -> Image.Image:
    w, h = 864, 1152
    paper = "#f6f3eb"
    base = Image.new("RGB", (w, h), paper)
    draw = ImageDraw.Draw(base)

    margin = 56
    draw.rectangle((margin, margin, w - margin, h - margin), outline="#2a4035", width=3)
    draw.rectangle((margin + 18, margin + 18, w - margin - 18, h - margin - 18), outline="#6b9a78", width=1)

    # Notebook lines — stop before the title block so text stays clean
    line_left = margin + 36
    line_right = w - margin - 24
    for y in range(margin + 52, h - margin - 52, 34):
        if margin + 250 < y < h - margin - 250:
            continue
        draw.line([(line_left, y), (line_right, y)], fill=(150, 185, 220), width=1)
    draw.line([(margin + 30, margin + 24), (margin + 30, h - margin - 24)], fill=(196, 96, 96), width=2)

    title_font = load_font(88, bold=True)
    sub_font = load_font(28, bold=False)
    title = "CABIN"
    subtitle = "Handwritten notebook"

    tb = draw.textbbox((0, 0), title, font=title_font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    sb = draw.textbbox((0, 0), subtitle, font=sub_font)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]

    block_w = max(tw, sw) + 80
    block_h = th + sh + 56
    bx0 = (w - block_w) // 2
    by0 = (h - block_h) // 2
    draw.rectangle((bx0, by0, bx0 + block_w, by0 + block_h), fill=paper, outline="#c9d8c4", width=2)

    tx = (w - tw) // 2
    ty = by0 + 18
    pine = "#1e3d2a"
    for ox, oy, color in ((3, 4, "#143024"), (2, 3, "#1a3828"), (1, 2, "#204030")):
        draw.text((tx + ox, ty + oy), title, font=title_font, fill=color)
    draw.text((tx, ty), title, font=title_font, fill=pine)
    draw.text(((w - sw) // 2, ty + th + 22), subtitle, font=sub_font, fill="#3d6b4a")

    return base


def make_cabin_covers() -> None:
    img = Image.open(CABIN_SRC).convert("RGB")
    img = ImageOps.exif_transpose(img)
    img = trim_to_paper(img)
    img = fit_cover(img)
    img = polish_photo(img, modern=False)
    orig_out = ASSETS / "cabin-cover.png"
    img.save(orig_out, optimize=True, quality=90)

    modern_card = draw_cabin_modern_cover()
    compose_mockup(modern_card).save(ASSETS / "cabin-cover-modern.png", optimize=True, quality=90)
    print(f"Cabin covers -> {orig_out.name}, cabin-cover-modern.png")


def draw_binder_cover(title: str, subtitle: str, modern: bool) -> Image.Image:
    w, h = 864, 1152
    if modern:
        bg = Image.new("RGB", (w, h), "#e8efe6")
        draw = ImageDraw.Draw(bg)
        for y in range(h):
            fade = int(12 * (y / h))
            draw.line([(0, y), (w, y)], fill=(220 - fade, 235 - fade, 218 - fade))
        accent = "#3d6b4a"
        title_color = "#1e3d2a"
    else:
        bg = Image.new("RGB", (w, h), "#ffffff")
        draw = ImageDraw.Draw(bg)
        accent = "#2a4035"
        title_color = "#111111"

    margin = 64
    draw.rectangle((margin, margin, w - margin, h - margin), outline=accent, width=3 if modern else 2)

    title_font = load_font(72 if modern else 64, bold=True)
    sub_font = load_font(28, bold=False)

    tb = draw.textbbox((0, 0), title, font=title_font)
    tw = tb[2] - tb[0]
    draw.text(((w - tw) // 2, h // 2 - 90), title, font=title_font, fill=title_color)
    if subtitle:
        sb = draw.textbbox((0, 0), subtitle, font=sub_font)
        sw = sb[2] - sb[0]
        draw.text(((w - sw) // 2, h // 2 + 10), subtitle, font=sub_font, fill=accent)

    if modern:
        draw.rectangle((margin + 20, margin + 20, w - margin - 20, h - margin - 20), outline="#8ab89a", width=1)
    return bg


def make_low_carb_covers() -> None:
    plain = draw_binder_cover("LOW CARB", "Nice to have", modern=False)
    plain.save(ASSETS / "low-carb-cover.png", optimize=True, quality=90)
    modern = draw_binder_cover("LOW CARB", "Nice to have", modern=True)
    compose_mockup(modern).save(ASSETS / "low-carb-cover-modern.png", optimize=True, quality=90)
    print("Low Carb covers -> low-carb-cover.png, low-carb-cover-modern.png")


if __name__ == "__main__":
    make_cabin_covers()
    make_low_carb_covers()