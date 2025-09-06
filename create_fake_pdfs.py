from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Ensure sample_pdfs folder exists
os.makedirs("sample_pdfs", exist_ok=True)

# Define sample PDF data
pdf_data = {
    "1001.pdf": "ID: 1001\nName: Alice Smith\nMarks: 85",   # correct
    "1002.pdf": "ID: 1002\nName: Bob Jonson\nMarks: 90",    # typo in name
    "1003.pdf": "ID: 1003\nName: Charlie Lee\nMarks: 80",   # marks mismatch
    "1004.pdf": "ID: 1004\nName: Diana Prince\nMarks: 92",  # correct
    "1005.pdf": "ID: 1005\nName: Evan Wright\nMarks: 70",   # marks mismatch
}

# Generate PDFs
for filename, content in pdf_data.items():
    path = os.path.join("sample_pdfs", filename)
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Write each line
    for i, line in enumerate(content.split("\n")):
        c.drawString(100, 750 - (i * 20), line)

    c.save()
    print(f"Created {path}")
