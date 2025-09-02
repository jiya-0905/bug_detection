# 🐞 Bug Prediction Engine for GitHub Repositories
## 🔍 Overview
This project predicts which files in a GitHub repository are most likely to contain bugs, using commit history and code metrics. It helps developers prioritize code reviews and testing efforts by identifying high-risk areas in large codebases.


<img width="1903" height="1025" alt="Screenshot 2025-09-02 210221" src="https://github.com/user-attachments/assets/b7cbedbf-4da1-4b94-a27f-092e10797bd4" />
<img width="1905" height="734" alt="Screenshot 2025-09-02 210437" src="https://github.com/user-attachments/assets/b13e20ba-7bed-4cca-848b-08a66da0ecd3" />


## 🚀 Features
- 🔎 Fetches commit data and file history from any public GitHub repo
- 📊 Extracts features like commit frequency, churn rate, and contributor count
- 🧠 Trains a machine learning model to classify files as bug-prone or safe
- 📈 Visualizes risk scores with an interactive dashboard

## 🧰 Tech Stack
- Python for data processing and ML
- GitHub API for repository mining
- scikit-learn for model training
- Streamlit for the web dashboard
- Radon (optional) for code complexity metrics
  
## 📂 How It Works
- Data Collection: Pulls commit history and file-level changes from a GitHub repo
- Feature Engineering: Calculates metrics like:
- Number of commits per file
- Lines added/deleted
- Number of unique contributors
- Time since last modification
- Labeling: Uses commit messages to label files (e.g., commits with “fix”, “bug”, “issue”)
- Model Training: Trains a classifier to predict bug-prone files
- Visualization: Displays risk scores in a clean dashboard
  
## 📌 Use Cases
- Prioritize code reviews for risky files
- Identify hotspots in legacy codebases
- Improve software quality with data-driven insights
  
## 🛠️ Setup Instructions

git clone https://github.com/jiya-0805/bug_detection.git

cd bug_detection

python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt

streamlit run app.py

  
## 👩‍💻 Author
Jiya, Final Year B.Tech Student @ TIET
Passionate about ML, software engineering, and building tools that solve real problems.
