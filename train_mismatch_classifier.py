import pandas as pd
import numpy as np
import re
from fuzzywuzzy import fuzz
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from scripts.extract_fields import extract_fields

# ---------------------------------------------------
# Load ground truth Excel
# ---------------------------------------------------
ground_truth_df = pd.read_excel("data/student_data.xlsx")

# ---------------------------------------------------
# Simulated extracted PDF texts (replace with real extraction later)
# ---------------------------------------------------
pdf_texts = {
    '1001': "ID: 1001\nName: Alice Smith\nMarks: 85",
    '1002': "ID: 1002\nName: Bob Jonson\nMarks: 90",   # <-- typo in last name
    '1003': "ID: 1003\nName: Charlie Lee\nMarks: 80",  # <-- wrong marks
    '1004': "ID: 1004\nName: Diana Prince\nMarks: 92",
    '1005': "ID: 1005\nName: Evan Wright\nMarks: 70"   # <-- wrong marks
}

# ---------------------------------------------------
# Feature generation function
# ---------------------------------------------------
def generate_features(extracted, ground_truth):
    features = {}
    features['ID_match'] = int(extracted['Student_ID'] == str(ground_truth['Student_ID']))
    features['Name_similarity'] = fuzz.ratio(extracted['Name'] or "", ground_truth['Name'] or "") / 100
    features['Marks_difference'] = abs((extracted['Marks'] or 0) - ground_truth['Marks'])
    features['Total_missing_fields'] = sum(x is None for x in extracted.values())
    return features

# ---------------------------------------------------
# Build dataset
# ---------------------------------------------------
feature_rows = []
labels = []

for sid, pdf_text in pdf_texts.items():
    extracted = extract_fields(pdf_text)
    gt_row = ground_truth_df[ground_truth_df['Student_ID'] == int(sid)].iloc[0]
    features = generate_features(extracted, gt_row)

    # Label = mismatch if marks difference > 5 OR name similarity < 0.8
    mismatch = int((features['Marks_difference'] > 5) or (features['Name_similarity'] < 0.8))

    feature_rows.append(features)
    labels.append(mismatch)

features_df = pd.DataFrame(feature_rows)
labels_series = pd.Series(labels)

# ---------------------------------------------------
# Train/test split
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    features_df, labels_series, test_size=0.4, random_state=42
)

# ---------------------------------------------------
# Train model
# ---------------------------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ---------------------------------------------------
# Evaluate
# ---------------------------------------------------
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ---------------------------------------------------
# Save model safely
# ---------------------------------------------------
os.makedirs("models/mismatch_classifier", exist_ok=True)
joblib.dump(model, "models/mismatch_classifier/model.pkl")
print("✅ Model saved at models/mismatch_classifier/model.pkl")
