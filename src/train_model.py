import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load features
df = pd.read_csv("data/file_features.csv")

# Features and label
X = df[["commit_count", "unique_authors", "last_modified_days_ago", "bug_fix_count"]]
y = df["is_buggy"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print("📊 Classification Report:")
print(classification_report(y_test, preds))

# Save model
joblib.dump(model, "models/bug_predictor.pkl")
print("✅ Model saved to models/bug_predictor.pkl")