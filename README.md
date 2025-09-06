A Streamlit web application that extracts data from digital PDF marksheets and compares it with official student records using Machine Learning. The app highlights mismatches, provides insights, and ensures accurate academic record verification.

✨ Features

📂 Upload PDF marksheets – automatic text and field extraction (no OCR needed for digital PDFs).

🤖 Mismatch Detection – ML model detects discrepancies between extracted data and reference records.

📊 Analytics Dashboard – visualize mismatched fields and summary statistics.

🌐 Web App – simple, browser-based interface built with Streamlit.

🛠️ Tech Stack

Python – core logic & ML pipeline

Streamlit – interactive web UI

pdfplumber – PDF text extraction

pandas / scikit-learn – data handling & ML

openpyxl – Excel integration for student data

📂 Project Structure
marksheet_ml_verifier/
│
├── data/
│   └── student_data.xlsx       # Student records (for comparison)
├── models/
│   └── mismatch_classifier/    # Saved ML models
├── scripts/
│   ├── extract_pdf_text.py     # Extracts text from PDFs
│   ├── extract_fields.py       # Extracts structured fields
│   └── train_mismatch_classifier.py  # ML training script
├── app.py                      # Streamlit app entry point
├── requirements.txt            # Dependencies
├── .gitignore                  # Ignore unnecessary files
├── LICENSE                     # MIT License
└── README.md                   # Project documentation

⚡ Installation & Usage
1️⃣ Clone the Repository
git clone https://github.com/YourUsername/marksheet-ml-verifier.git
cd marksheet-ml-verifier

2️⃣ Create Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate   # on Mac/Linux
venv\Scripts\activate      # on Windows

pip install -r requirements.txt

3️⃣ Run the Streamlit App
streamlit run app.py

🚀 Deployment (Streamlit Cloud)

Push code to GitHub.

Go to Streamlit Community Cloud
.

Select your repo → branch → app.py.

Click Deploy 🚀.

📜 License

This project is licensed under the MIT License
.

👤 Author

Developed by [Siddharth Nair] ✨



