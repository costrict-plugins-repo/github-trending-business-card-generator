# Business Card Generator

A Claude Code plugin that generates professional, print-ready business card PDFs with 300 DPI, CMYK colors, proper bleed, trim marks, and safe zones — ready to send to any print shop.

## Features

- **Print-ready output**: 300 DPI, CMYK colors, proper bleed, trim marks
- **Three styles**: Classic, Modern, Minimal
- **Safe zone enforcement**: All text stays within the printable area
- **CMYK color bars**: Included for print shop verification
- **Optional logo**: Place a company logo on the card

## Installation

### As a Claude Code Plugin

```bash
/plugin install business-card-generator
```

Or load manually during development:

```bash
claude --plugin-dir ./business-card-generator
```

### Prerequisites

The plugin requires Python 3.7+ with ReportLab and Pillow:

```bash
pip install reportlab pillow
```

## Usage

### With Claude (Natural Language)

Just tell Claude what you need:

> "Generate a business card for Jane Smith, Senior Engineer at Acme Corp, jane@acme.com, (555) 123-4567"

> "Make me a minimal style business card with my name and email"

> "Create business cards — use the modern style"

### With the Slash Command

```
/business-card-generator:business-card
```

Claude will ask for your details and generate the card.

### Direct Command Line

```bash
python scripts/card_generator.py \
  --name "Jane Smith" \
  --title "Senior Software Engineer" \
  --company "Acme Corp" \
  --phone "(555) 123-4567" \
  --email "jane@acme.com" \
  --website "www.acme.com" \
  --style classic
```

### Options

| Flag        | Required | Description                          |
|-------------|----------|--------------------------------------|
| `--name`    | Yes      | Full name                            |
| `--title`   | No       | Job title                            |
| `--company` | No       | Company name                         |
| `--phone`   | No       | Phone number                         |
| `--email`   | No       | Email address                        |
| `--website` | No       | Website URL                          |
| `--logo`    | No       | Path to logo image (PNG/JPG)         |
| `--output`  | No       | Custom output file path              |
| `--style`   | No       | `classic`, `modern`, or `minimal`    |

### Styles

- **classic** — White background, blue accent, divider line between name and contact info
- **modern** — Light gray background, blue accent bar on the left edge
- **minimal** — White background, grayscale palette, clean lines

## Print Specifications

| Property         | Value                              |
|------------------|------------------------------------|
| Final card size  | 3.5" x 2" (88.9mm x 50.8mm)      |
| With bleed       | 3.75" x 2.25" (95.25mm x 57.15mm)|
| Bleed            | 0.125" (3.175mm) all sides        |
| Safe zone        | 3.25" x 1.75" (content area)      |
| Resolution       | 300 DPI                            |
| Color mode       | CMYK                               |
| Trim marks       | Yes, at all four corners           |
| Color bars       | CMYK verification bars included    |

## Output

Generated PDFs are saved to `output/` with timestamped filenames:

```
output/card_Jane_Smith_20260211_143022.pdf
```

## Testing

Generate a test card to verify everything works:

```bash
python scripts/card_generator.py --name "Test User" --title "QA Engineer" --email "test@example.com"
```

Open the resulting PDF and verify:
1. Crop marks visible at all four corners
2. CMYK color bars below the card
3. Text is within the safe zone (not touching trim edges)
4. Background extends to document edges (bleed area)

## License

MIT
