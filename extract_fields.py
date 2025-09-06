import re

def extract_fields(text):
    """
    Extracts Student_ID, Name, and Marks from PDF text.
    Supports both simple and slightly messy formats:
    - ID: 1001
    - Name: Alice Smith
    - Marks: 85
    - Marks Obtained: 85/100
    - Score - 78
    - Total Marks: 92
    """
    # Student ID
    student_id = re.search(r'\bID[:\s]+(\d+)', text, re.IGNORECASE)

    # Name (letters + spaces only)
    name = re.search(r'\bName[:\s]+([A-Za-z ]+)', text, re.IGNORECASE)

    # Marks (handles multiple formats)
    marks_patterns = [
        r'Marks[:\s]+(\d+)',             # Marks: 85
        r'Marks Obtained[:\s]+(\d+)',    # Marks Obtained: 85
        r'Marks Obtained[:\s]+(\d+)/\d+',# Marks Obtained: 85/100
        r'Score[:\s-]+(\d+)',            # Score - 78
        r'Total Marks[:\s]+(\d+)'        # Total Marks: 92
    ]

    marks_val = None
    for pattern in marks_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            marks_val = int(m.group(1))
            break

    return {
        "Student_ID": student_id.group(1) if student_id else None,
        "Name": name.group(1).strip() if name else None,
        "Marks": marks_val
    }
