# /generate-card

Generate a professional, print-ready business card PDF.

## Usage
Just run `/generate-card` and provide your details when prompted, or supply them inline:

```
/generate-card Name: Jane Smith, Title: Senior Engineer, Company: Acme Corp, Phone: (555) 123-4567, Email: jane@acme.com, Website: www.acme.com
```

## What This Does
1. Collects your business card information (name, title, company, phone, email, website, optional logo)
2. Generates a print-ready PDF with proper bleed, CMYK colors, 300 DPI, and crop marks
3. Saves the PDF to the `output/` directory with a timestamped filename

## Output
A PDF file ready to send to any professional print shop. Includes:
- 0.125" bleed on all sides
- Trim/crop marks at corners
- CMYK color bars for print verification
- All text within the safe zone

Invoke the business-card skill to handle this request.
