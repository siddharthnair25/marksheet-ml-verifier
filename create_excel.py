import pandas as pd
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Sample student data
data = {
    'Student_ID': [1001, 1002, 1003, 1004, 1005],
    'Name': ['Alice Smith', 'Bob Johnson', 'Charlie Lee', 'Diana Prince', 'Evan Wright'],
    'Marks': [85, 90, 78, 92, 88]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save Excel file
excel_path = "data/student_data.xlsx"
df.to_excel(excel_path, index=False)

print(f"Excel file created at {excel_path}")
