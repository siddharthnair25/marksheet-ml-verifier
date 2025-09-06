import streamlit as st
import pandas as pd
import os
import glob
from scripts.extract_pdf_text import extract_text_from_pdf
from scripts.extract_fields import extract_fields
from fuzzywuzzy import fuzz
import joblib
from io import BytesIO

# Load trained model
model_path = "models/mismatch_classifier/model.pkl"
if not os.path.exists(model_path):
    st.error("Model not found. Please train the model first by running train_mismatch_classifier.py")
    st.stop()
model = joblib.load(model_path)

def generate_features(extracted, gt_row):
    features = {}
    features['ID_match'] = int(extracted['Student_ID'] == str(gt_row['Student_ID']))
    features['Name_similarity'] = fuzz.ratio(extracted['Name'] or "", gt_row['Name'] or "") / 100
    features['Marks_difference'] = abs((extracted['Marks'] or 0) - gt_row['Marks'])
    features['Total_missing_fields'] = sum(x is None for x in extracted.values())
    return features

# ---------------- STREAMLIT APP ----------------
st.title("📄 Marksheet ML Verifier")

uploaded_excel = st.file_uploader("Upload Ground Truth Excel", type=["xlsx"])

pdf_input_mode = st.radio(
    "Choose how to load PDFs:",
    ("Upload PDFs manually", "Load all PDFs from a folder")
)

pdf_files = []

if pdf_input_mode == "Upload PDFs manually":
    pdf_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])

elif pdf_input_mode == "Load all PDFs from a folder":
    folder_path = st.text_input("Enter folder path (e.g., sample_pdfs/)", "sample_pdfs/")
    if st.button("Load PDFs"):
        if os.path.isdir(folder_path):
            pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
            st.success(f"Found {len(pdf_files)} PDFs in {folder_path}")
        else:
            st.error("Folder does not exist!")

# ---------------- PROCESSING ----------------
if uploaded_excel and pdf_files:
    ground_truth_df = pd.read_excel(uploaded_excel)
    mismatches = []

    # Handle both uploaded files and file paths
    for pdf_file in pdf_files:
        if isinstance(pdf_file, str):  # From folder
            text = extract_text_from_pdf(pdf_file)
        else:  # Uploaded via UI
            text = extract_text_from_pdf(pdf_file)

        extracted = extract_fields(text)

        gt_match = ground_truth_df[ground_truth_df['Student_ID'].astype(str) == extracted['Student_ID']]
        if gt_match.empty:
            mismatches.append({
                "Student_ID": extracted.get('Student_ID', 'N/A'),
                "Reason": "Student ID not found in Excel"
            })
            continue

        gt_row = gt_match.iloc[0]
        features = generate_features(extracted, gt_row)
        feature_vector = [[
            features['ID_match'],
            features['Name_similarity'],
            features['Marks_difference'],
            features['Total_missing_fields']
        ]]
        pred = model.predict(feature_vector)[0]

        if pred == 1:
            mismatches.append({
                "Student_ID": extracted.get('Student_ID', 'N/A'),
                "Name_PDF": extracted.get('Name', 'N/A'),
                "Name_Excel": gt_row['Name'],
                "Marks_PDF": extracted.get('Marks', 'N/A'),
                "Marks_Excel": gt_row['Marks'],
                "Reason": "Mismatch detected"
            })

    # ---------------- RESULTS ----------------
    if mismatches:
        st.subheader("⚠️ Mismatches Found:")
        mismatches_df = pd.DataFrame(mismatches)
        st.write(mismatches_df)

        # Export Excel in memory
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            mismatches_df.to_excel(writer, index=False)
        buffer.seek(0)

        st.download_button(
            label="📥 Download Mismatch Report",
            data=buffer,
            file_name="mismatch_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.success("✅ No mismatches found!")
