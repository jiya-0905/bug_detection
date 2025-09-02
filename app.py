import streamlit as st
import pandas as pd
import joblib
import altair as alt

# Load model and data
model = joblib.load("models/bug_predictor.pkl")
df = pd.read_csv("data/file_features.csv")

# Predict bug risk
features = df[["commit_count", "unique_authors", "last_modified_days_ago", "bug_fix_count"]]
df["predicted_buggy"] = model.predict(features)

# Risk level coloring
def risk_level(row):
    if row["predicted_buggy"] == 1 and row["bug_fix_count"] >= 3:
        return "🔴 High"
    elif row["predicted_buggy"] == 1:
        return "🟠 Medium"
    else:
        return "🟢 Low"

df["risk_level"] = df.apply(risk_level, axis=1)

# Streamlit UI
st.set_page_config(page_title="Bug Prediction Engine", layout="wide")
st.title("🐞 Bug Prediction Engine")
st.markdown("""
This tool analyzes GitHub commit history and code metrics to predict which files are most likely to contain bugs.  
Use it to prioritize code reviews, improve software quality, and reduce QA overhead.
""")
uploaded_file = st.file_uploader("📤 Upload your commit_info.json", type="json")

if uploaded_file:
    import json
    commits = json.load(uploaded_file)
    from src.feature_engineering import extract_features
    df = extract_features(commits)
    features = df[["commit_count", "unique_authors", "last_modified_days_ago", "bug_fix_count"]]
    df["predicted_buggy"] = model.predict(features)
    df["risk_level"] = df.apply(risk_level, axis=1)

# Sidebar filters
repo_url = st.sidebar.text_input("🔗 GitHub Repo URL")

if repo_url:
    try:
        owner, repo = repo_url.strip().split("/")[-2:]
        from src.fetch_data import get_commits, extract_commit_info
        commits = get_commits(owner, repo, max_pages=3)
        commit_info = extract_commit_info(commits, owner, repo)
        df = extract_features(commit_info)
        features = df[["commit_count", "unique_authors", "last_modified_days_ago", "bug_fix_count"]]
        df["predicted_buggy"] = model.predict(features)
        df["risk_level"] = df.apply(risk_level, axis=1)
    except Exception as e:
        st.error(f"❌ Failed to fetch data: {e}")
st.sidebar.header("🔍 Filters")
min_commits = st.sidebar.slider("Minimum commit count", 0, int(df["commit_count"].max()), 1)
show_only_buggy = st.sidebar.checkbox("Show only predicted buggy files")

filtered_df = df[df["commit_count"] >= min_commits]
if show_only_buggy:
    filtered_df = filtered_df[filtered_df["predicted_buggy"] == 1]

# Summary metrics
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Files", len(df))
col2.metric("Buggy Files", df["predicted_buggy"].sum())
col3.metric("High Risk Files", (df["risk_level"] == "🔴 High").sum())

# Bar chart: Top 10 risky files
st.subheader("🔥 Top 10 Risky Files")
top_risky = df[df["predicted_buggy"] == 1].sort_values(by="bug_fix_count", ascending=False).head(10)
chart = alt.Chart(top_risky).mark_bar().encode(
    x="bug_fix_count:Q",
    y=alt.Y("file:N", sort="-x"),
    color=alt.Color("risk_level:N", scale=alt.Scale(domain=["🔴 High", "🟠 Medium", "🟢 Low"],
                                                    range=["#FF4B4B", "#FFA500", "#4CAF50"])),
    tooltip=["file", "commit_count", "bug_fix_count", "risk_level"]
).properties(height=400)
st.altair_chart(chart, use_container_width=True)

# Data table
st.subheader("📁 File-Level Predictions")
st.dataframe(filtered_df[["file", "commit_count", "unique_authors", "last_modified_days_ago", "bug_fix_count", "risk_level"]])

# Download button
st.download_button("📥 Download Results as CSV", filtered_df.to_csv(index=False), file_name="bug_predictions.csv")