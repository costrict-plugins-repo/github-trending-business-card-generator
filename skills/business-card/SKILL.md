---
name: business-card
description: Generate professional, print-ready business card PDFs with 300 DPI, CMYK colors, proper bleed, trim marks, and safe zones. Use when the user wants to create, design, or generate a business card.
---

# Business Card Generator

Generate professional, print-ready business cards as PDF files. All output meets professional print shop specifications: 300 DPI, CMYK color, proper bleed, trim marks, and safe zones.

## Workflow

### Step 1: Collect Information
Ask the user for the following details. Only **Name** is required; all others are optional.

| Field       | Required | Example                    |
|-------------|----------|----------------------------|
| Name        | Yes      | Jane Smith                 |
| Title       | No       | Senior Software Engineer   |
| Company     | No       | Acme Corp                  |
| Phone       | No       | (555) 123-4567             |
| Email       | No       | jane@acme.com              |
| Website     | No       | www.acme.com               |
| Logo path   | No       | /path/to/logo.png          |

### Step 2: Generate the Card
Run the Python generator script with the collected information:

```bash
python scripts/card_generator.py \
  --name "Jane Smith" \
  --title "Senior Software Engineer" \
  --company "Acme Corp" \
  --phone "(555) 123-4567" \
  --email "jane@acme.com" \
  --website "www.acme.com"
```

Optional flags:
- `--logo /path/to/logo.png` — place a company logo in the top-right corner
- `--output /custom/path.pdf` — override default output location
- `--style [classic|modern|minimal]` — choose a design style (default: classic)

The script must be run from the `business-card-generator/` directory, or use the full path to the script.

### Step 3: Validate Output
After generation, confirm the following:
1. PDF file was created in the `output/` directory
2. File size is reasonable (typically 10KB–2MB, under 5MB)
3. Report the file path to the user

### Step 4: Deliver
Provide the user with:
- The full path to the generated PDF
- A summary of the card contents
- Reminder that the PDF is print-ready at 300 DPI with CMYK colors and 0.125" bleed

## Print Specifications Reference

| Property         | Value                              |
|------------------|------------------------------------|
| Final card size  | 3.5" × 2" (88.9mm × 50.8mm)      |
| With bleed       | 3.75" × 2.25" (95.25mm × 57.15mm)|
| Bleed            | 0.125" (3.175mm) all sides        |
| Safe zone        | 3.25" × 1.75" (content area)      |
| Resolution       | 300 DPI                           |
| Color mode       | CMYK                              |
| Trim marks       | Yes, at all four corners           |
| Color bars       | CMYK verification bars included    |

## Error Handling
- If Python or ReportLab is not installed, instruct the user to run: `pip install reportlab pillow`
- If the logo file path is invalid, warn the user and generate the card without a logo
- If the output directory does not exist, create it automatically
