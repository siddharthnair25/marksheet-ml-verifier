import streamlit as st
import pandas as pd
import os
from fuzzywuzzy import fuzz
import joblib
from scripts.extract_pdf_text import extract_text_from_pdf
from scripts.extract_fields import extract_fields

# -------------------------------
# Load trained model
# -------------------------------
model_path = "models/mismatch_classifier/model.pkl"
if not os.path.exists(model_path):
    st.error("Model not found. Please train the model first by running train_mismatch_classifier.py")
    st.stop()

model = joblib.load(model_path)

# -------------------------------
# Feature generation
# -------------------------------
def generate_features(extracted, gt_row):
    features = {}
    # Ensure ID is string for comparison
    features['ID_match'] = int(str(extracted.get('Student_ID')) == str(gt_row['Student_ID']))
    
    # Name similarity (ignore case and strip spaces)
    features['Name_similarity'] = fuzz.ratio(
        (extracted.get('Name') or "").lower().strip(),
        (gt_row['Name'] or "").lower().strip()
    ) / 100
    
    # Marks difference
    features['Marks_difference'] = abs((extracted.get('Marks') or 0) - gt_row['Marks'])
    
    # Count missing fields
    features['Total_missing_fields'] = sum(x is None for x in extracted.values())
    
    return features

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Marksheet ML Verifier")

uploaded_excel = st.file_uploader("Upload Ground Truth Excel", type=["xlsx"])
uploaded_pdfs = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])

if uploaded_excel and uploaded_pdfs:
    ground_truth_df = pd.read_excel(uploaded_excel)
    mismatches = []

    for pdf_file in uploaded_pdfs:
        text = extract_text_from_pdf(pdf_file)
        extracted = extract_fields(text)

        # Match student in Excel
        gt_match = ground_truth_df[ground_truth_df['Student_ID'].astype(str) == str(extracted['Student_ID'])]
        if gt_match.empty:
            mismatches.append({
                "Student_ID": extracted.get('Student_ID', 'N/A'),
                "Reason": "Student ID not found in Excel"
            })
            continue

        gt_row = gt_match.iloc[0]
        # ✅ Generate features FIRST
        features = generate_features(extracted, gt_row)

        # --- RULE-BASED MISMATCH DETECTION ---
        name_mismatch = features['Name_similarity'] < 0.95  # Name similarity < 95%
        marks_mismatch = features['Marks_difference'] > 0   # Any marks difference

        if name_mismatch or marks_mismatch:
            mismatches.append({
                "Student_ID": extracted.get('Student_ID', 'N/A'),
                "Name_PDF": extracted.get('Name', 'N/A'),
                "Name_Excel": gt_row['Name'],
                "Marks_PDF": extracted.get('Marks', 'N/A'),
                "Marks_Excel": gt_row['Marks'],
                "Reason": f"Name mismatch: {name_mismatch}, Marks mismatch: {marks_mismatch}"
            })

    if mismatches:
        st.subheader("Mismatches Found:")
        st.write(pd.DataFrame(mismatches))
        st.download_button(
            label="Download Mismatch Report",
            data=pd.DataFrame(mismatches).to_excel(index=False),
            file_name="mismatch_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.success("No mismatches found!")


