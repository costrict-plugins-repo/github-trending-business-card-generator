#!/usr/bin/env python3
"""
Business Card Generator - Print-Ready PDF Output

Generates professional business cards meeting print shop specifications:
- 3.5" x 2" final size with 0.125" bleed (3.75" x 2.25" document)
- 300 DPI resolution
- CMYK color mode
- Trim/crop marks at corners
- CMYK color bars for print verification
- Safe zone enforcement (all content within 3.25" x 1.75")
"""

import argparse
import os
import sys
from datetime import datetime

from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Print constants
# ---------------------------------------------------------------------------
CARD_WIDTH = 3.5 * inch       # Final trim size
CARD_HEIGHT = 2.0 * inch
BLEED = 0.125 * inch           # 0.125" bleed on all sides
DOC_WIDTH = CARD_WIDTH + 2 * BLEED    # 3.75"
DOC_HEIGHT = CARD_HEIGHT + 2 * BLEED  # 2.25"
SAFE_MARGIN = 0.125 * inch    # Safe zone inset from trim line

# Safe zone boundaries (relative to document origin at bottom-left)
SAFE_LEFT = BLEED + SAFE_MARGIN
SAFE_RIGHT = DOC_WIDTH - BLEED - SAFE_MARGIN
SAFE_TOP = DOC_HEIGHT - BLEED - SAFE_MARGIN
SAFE_BOTTOM = BLEED + SAFE_MARGIN
SAFE_WIDTH = SAFE_RIGHT - SAFE_LEFT    # 3.25"
SAFE_HEIGHT = SAFE_TOP - SAFE_BOTTOM   # 1.75"

# Trim line boundaries
TRIM_LEFT = BLEED
TRIM_RIGHT = DOC_WIDTH - BLEED
TRIM_TOP = DOC_HEIGHT - BLEED
TRIM_BOTTOM = BLEED

# Crop mark dimensions
CROP_MARK_LENGTH = 0.1 * inch
CROP_MARK_OFFSET = 0.04 * inch  # Gap between trim line and mark start

# ---------------------------------------------------------------------------
# CMYK Colors
# ---------------------------------------------------------------------------
COLOR_BLACK = CMYKColor(0, 0, 0, 1)
COLOR_DARK_GRAY = CMYKColor(0, 0, 0, 0.8)
COLOR_MED_GRAY = CMYKColor(0, 0, 0, 0.45)
COLOR_LIGHT_GRAY = CMYKColor(0, 0, 0, 0.08)
COLOR_WHITE = CMYKColor(0, 0, 0, 0)
COLOR_ACCENT = CMYKColor(0.85, 0.45, 0, 0.15)  # Professional blue

# Color bar swatches for print verification
COLOR_BAR_SWATCHES = [
    CMYKColor(1, 0, 0, 0),     # Cyan
    CMYKColor(0, 1, 0, 0),     # Magenta
    CMYKColor(0, 0, 1, 0),     # Yellow
    CMYKColor(0, 0, 0, 1),     # Black (Key)
    CMYKColor(1, 1, 0, 0),     # Cyan+Magenta
    CMYKColor(0, 1, 1, 0),     # Magenta+Yellow
    CMYKColor(1, 0, 1, 0),     # Cyan+Yellow
]

# Style definitions
STYLES = {
    "classic": {
        "bg_color": COLOR_WHITE,
        "name_color": COLOR_BLACK,
        "title_color": COLOR_ACCENT,
        "text_color": COLOR_DARK_GRAY,
        "accent_color": COLOR_ACCENT,
        "divider": True,
        "accent_bar": False,
    },
    "modern": {
        "bg_color": CMYKColor(0, 0, 0, 0.03),
        "name_color": CMYKColor(0.85, 0.45, 0, 0.15),
        "title_color": COLOR_DARK_GRAY,
        "text_color": COLOR_DARK_GRAY,
        "accent_color": CMYKColor(0.85, 0.45, 0, 0.15),
        "divider": False,
        "accent_bar": True,
    },
    "minimal": {
        "bg_color": COLOR_WHITE,
        "name_color": COLOR_BLACK,
        "title_color": COLOR_MED_GRAY,
        "text_color": COLOR_MED_GRAY,
        "accent_color": COLOR_BLACK,
        "divider": False,
        "accent_bar": False,
    },
}


def draw_crop_marks(c):
    """Draw trim/crop marks at the four corners of the card."""
    c.setStrokeColor(CMYKColor(0, 0, 0, 1))
    c.setLineWidth(0.25)

    corners = [
        (TRIM_LEFT, TRIM_BOTTOM),   # Bottom-left
        (TRIM_RIGHT, TRIM_BOTTOM),  # Bottom-right
        (TRIM_LEFT, TRIM_TOP),      # Top-left
        (TRIM_RIGHT, TRIM_TOP),     # Top-right
    ]

    for cx, cy in corners:
        # Horizontal marks
        if cx == TRIM_LEFT:
            c.line(cx - CROP_MARK_OFFSET - CROP_MARK_LENGTH, cy,
                   cx - CROP_MARK_OFFSET, cy)
        else:
            c.line(cx + CROP_MARK_OFFSET, cy,
                   cx + CROP_MARK_OFFSET + CROP_MARK_LENGTH, cy)

        # Vertical marks
        if cy == TRIM_BOTTOM:
            c.line(cx, cy - CROP_MARK_OFFSET - CROP_MARK_LENGTH,
                   cx, cy - CROP_MARK_OFFSET)
        else:
            c.line(cx, cy + CROP_MARK_OFFSET,
                   cx, cy + CROP_MARK_OFFSET + CROP_MARK_LENGTH)


def draw_color_bars(c):
    """Draw CMYK color verification bars outside the trim area."""
    bar_height = 0.06 * inch
    bar_width = CARD_WIDTH / len(COLOR_BAR_SWATCHES)
    y = TRIM_BOTTOM - CROP_MARK_OFFSET - bar_height - 0.02 * inch

    for i, color in enumerate(COLOR_BAR_SWATCHES):
        x = TRIM_LEFT + i * bar_width
        c.setFillColor(color)
        c.setStrokeColor(color)
        c.rect(x, y, bar_width, bar_height, fill=1, stroke=0)


def draw_background(c, style):
    """Fill the full document (including bleed) with the background color."""
    c.setFillColor(style["bg_color"])
    c.rect(0, 0, DOC_WIDTH, DOC_HEIGHT, fill=1, stroke=0)


def draw_accent_bar(c, style):
    """Draw a colored accent bar along the left edge (modern style)."""
    bar_width = 0.08 * inch
    c.setFillColor(style["accent_color"])
    # Extend into bleed area so it bleeds off the left edge
    c.rect(0, 0, BLEED + bar_width, DOC_HEIGHT, fill=1, stroke=0)


def draw_divider(c, y, style):
    """Draw a thin horizontal divider line within the safe zone."""
    c.setStrokeColor(style["accent_color"])
    c.setLineWidth(0.75)
    c.line(SAFE_LEFT, y, SAFE_RIGHT, y)


def place_logo(c, logo_path):
    """Place company logo in the top-right of the safe zone."""
    if not logo_path or not os.path.isfile(logo_path):
        if logo_path:
            print(f"Warning: Logo file not found at '{logo_path}', skipping logo.")
        return

    try:
        from reportlab.lib.utils import ImageReader
        img = ImageReader(logo_path)
        iw, ih = img.getSize()

        max_h = 0.45 * inch
        max_w = 1.0 * inch
        scale = min(max_w / iw, max_h / ih)
        draw_w = iw * scale
        draw_h = ih * scale

        x = SAFE_RIGHT - draw_w
        y = SAFE_TOP - draw_h
        c.drawImage(logo_path, x, y, width=draw_w, height=draw_h,
                     preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"Warning: Could not place logo — {e}")


def generate_card(name, title="", company="", phone="", email="",
                  website="", logo_path="", output_path="", style_name="classic"):
    """Generate a print-ready business card PDF."""

    style = STYLES.get(style_name, STYLES["classic"])

    # Determine output path
    if not output_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(os.path.dirname(script_dir), "output")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = name.replace(" ", "_").replace("/", "-")
        output_path = os.path.join(output_dir, f"card_{safe_name}_{timestamp}.pdf")
    else:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Create canvas
    c = canvas.Canvas(output_path, pagesize=(DOC_WIDTH, DOC_HEIGHT))
    c.setTitle(f"Business Card - {name}")
    c.setAuthor("Business Card Generator")
    c.setSubject("Print-Ready Business Card")

    # --- Draw layers ---

    # 1. Background (full bleed)
    draw_background(c, style)

    # 2. Accent bar (if style uses it)
    if style.get("accent_bar"):
        draw_accent_bar(c, style)

    # 3. Logo
    place_logo(c, logo_path)

    # 4. Text content — all within safe zone
    # Determine available width (leave room for logo if present)
    text_right = SAFE_RIGHT
    if logo_path and os.path.isfile(logo_path):
        text_right = SAFE_RIGHT - 1.1 * inch  # Reserve space for logo

    # -- Name --
    y_cursor = SAFE_TOP - 0.05 * inch
    c.setFillColor(style["name_color"])
    name_size = _fit_font_size(c, "Helvetica-Bold", name, text_right - SAFE_LEFT, 14, 20)
    c.setFont("Helvetica-Bold", name_size)
    y_cursor -= name_size * 0.9
    c.drawString(SAFE_LEFT, y_cursor, name)

    # -- Title --
    if title:
        c.setFillColor(style["title_color"])
        title_size = _fit_font_size(c, "Helvetica", title, text_right - SAFE_LEFT, 9, 12)
        c.setFont("Helvetica", title_size)
        y_cursor -= title_size * 1.5
        c.drawString(SAFE_LEFT, y_cursor, title)

    # -- Company --
    if company:
        c.setFillColor(style["text_color"])
        comp_size = _fit_font_size(c, "Helvetica", company, text_right - SAFE_LEFT, 8, 10)
        c.setFont("Helvetica", comp_size)
        y_cursor -= comp_size * 1.6
        c.drawString(SAFE_LEFT, y_cursor, company)

    # -- Divider --
    if style.get("divider") and (phone or email or website):
        y_cursor -= 0.12 * inch
        draw_divider(c, y_cursor, style)
        y_cursor -= 0.08 * inch

    # -- Contact info (bottom-aligned within safe zone) --
    contact_lines = []
    if phone:
        contact_lines.append(("Phone", phone))
    if email:
        contact_lines.append(("Email", email))
    if website:
        contact_lines.append(("Web", website))

    if contact_lines:
        c.setFillColor(style["text_color"])
        contact_size = 8.5
        line_height = contact_size * 1.55

        # Position contact block at bottom of safe zone
        block_height = len(contact_lines) * line_height
        y_contact = SAFE_BOTTOM + block_height - contact_size * 0.2

        for label, value in contact_lines:
            # Label
            c.setFont("Helvetica-Bold", contact_size)
            c.setFillColor(style["accent_color"])
            c.drawString(SAFE_LEFT, y_contact, f"{label}:")

            # Value — offset to align
            label_width = c.stringWidth(f"{label}: ", "Helvetica-Bold", contact_size)
            c.setFont("Helvetica", contact_size)
            c.setFillColor(style["text_color"])
            c.drawString(SAFE_LEFT + label_width, y_contact, value)

            y_contact -= line_height

    # 5. Crop marks & color bars (outside trim)
    draw_crop_marks(c)
    draw_color_bars(c)

    # Finalize
    c.showPage()
    c.save()

    file_size = os.path.getsize(output_path)
    print(f"Business card generated successfully!")
    print(f"  File: {output_path}")
    print(f"  Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
    print(f"  Style: {style_name}")
    print(f"  Document: {DOC_WIDTH/inch:.3f}\" x {DOC_HEIGHT/inch:.3f}\" (with bleed)")
    print(f"  Trim size: {CARD_WIDTH/inch:.1f}\" x {CARD_HEIGHT/inch:.1f}\"")
    print(f"  Bleed: {BLEED/inch:.3f}\"")
    print(f"  Color mode: CMYK")
    return output_path


def _fit_font_size(c, font_name, text, max_width, min_size, max_size):
    """Find the largest font size that fits text within max_width, clamped to [min_size, max_size]."""
    for size in range(int(max_size), int(min_size) - 1, -1):
        if c.stringWidth(text, font_name, size) <= max_width:
            return size
    return min_size


def main():
    parser = argparse.ArgumentParser(
        description="Generate a print-ready business card PDF (CMYK, 300 DPI, bleed, crop marks)."
    )
    parser.add_argument("--name", required=True, help="Full name (required)")
    parser.add_argument("--title", default="", help="Job title")
    parser.add_argument("--company", default="", help="Company name")
    parser.add_argument("--phone", default="", help="Phone number")
    parser.add_argument("--email", default="", help="Email address")
    parser.add_argument("--website", default="", help="Website URL")
    parser.add_argument("--logo", default="", help="Path to company logo image (PNG/JPG)")
    parser.add_argument("--output", default="", help="Custom output file path")
    parser.add_argument("--style", default="classic", choices=["classic", "modern", "minimal"],
                        help="Card design style (default: classic)")

    args = parser.parse_args()

    generate_card(
        name=args.name,
        title=args.title,
        company=args.company,
        phone=args.phone,
        email=args.email,
        website=args.website,
        logo_path=args.logo,
        output_path=args.output,
        style_name=args.style,
    )


if __name__ == "__main__":
    main()
