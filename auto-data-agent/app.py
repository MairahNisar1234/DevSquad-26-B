import streamlit as st
import pandas as pd
import plotly.express as px

from data_utils import clean_data, classify_columns
from analyzer import generate_insights

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Power BI Agent", layout="wide")
st.title("📊 AI Power BI Style Data Agent")


# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:

    df_raw = pd.read_csv(uploaded_file)

    st.subheader("📄 Raw Data")
    st.dataframe(df_raw.head())

    df, report = clean_data(df_raw.copy())

    st.subheader("🧹 Cleaned Data")
    st.dataframe(df.head())

    # ---------------- COLUMN CLASSIFICATION ----------------
    continuous, categorical, ids = classify_columns(df)

    # remove IDs completely
    categorical = [c for c in categorical if c not in ids]
    continuous = [c for c in continuous if c not in ids]

    all_cols = categorical + continuous

    # ---------------- SIDEBAR ----------------
    st.sidebar.title("🎛️ Controls")

    chart = st.sidebar.selectbox(
        "Chart Type",
        ["Auto", "Bar", "Line", "Scatter", "Histogram", "Box Plot", "Distribution Grid", "Pie Chart"]
    )

    st.sidebar.markdown("### 📌 Column Summary")
    st.sidebar.write("Continuous:", continuous)
    st.sidebar.write("Categorical:", categorical)
    st.sidebar.write("Excluded IDs:", ids)

    st.subheader("📊 Visualization")

    # ---------------- AUTO MODE ----------------
    if chart == "Auto":

        if len(categorical) > 0 and len(continuous) > 0:
            c = st.selectbox("Category Column", categorical)
            v = st.selectbox("Value Column", continuous)
            st.bar_chart(df.groupby(c)[v].mean())

        elif len(continuous) >= 2:
            x = st.selectbox("X Axis", continuous)
            y = st.selectbox("Y Axis", [c for c in continuous if c != x])
            st.scatter_chart(df[[x, y]])

        elif len(categorical) >= 1:
            c = st.selectbox("Column", categorical)
            st.bar_chart(df[c].value_counts().head(15))

        elif len(continuous) == 1:
            col = continuous[0]
            binned = pd.cut(df[col].dropna(), bins=10).value_counts().sort_index()
            binned.index = binned.index.astype(str)
            st.bar_chart(binned)

        else:
            st.warning("No graphable columns found")

    # ---------------- BAR ----------------
    elif chart == "Bar":

        c = st.selectbox("Column", all_cols)

        if c in categorical:
            st.bar_chart(df[c].value_counts().head(15))

        else:
            if len(categorical) > 0:
                v = st.selectbox("Value Column", continuous)
                st.bar_chart(df.groupby(c)[v].mean())
            else:
                st.bar_chart(df[c].value_counts())

    # ---------------- LINE ----------------
    elif chart == "Line":

        col = st.selectbox("Column", all_cols)

        if pd.api.types.is_numeric_dtype(df[col]):
            st.line_chart(df[col])
        else:
            st.bar_chart(df[col].value_counts().head(15))

    # ---------------- SCATTER ----------------
    elif chart == "Scatter":

        if len(continuous) >= 2:

            x = st.selectbox("X", continuous)
            y = st.selectbox("Y", [c for c in continuous if c != x])

            st.scatter_chart(df[[x, y]])

        else:
            st.warning("Need at least 2 numeric columns")

    # ---------------- HISTOGRAM ----------------
    elif chart == "Histogram":

        col = st.selectbox("Column", all_cols)
        bins = st.slider("Bins", 5, 50, 10)

        if pd.api.types.is_numeric_dtype(df[col]):
            binned = pd.cut(df[col].dropna(), bins=bins).value_counts().sort_index()
            binned.index = binned.index.astype(str)
        else:
            binned = df[col].value_counts().head(15)

        st.bar_chart(binned)

    # ---------------- BOX PLOT ----------------
    elif chart == "Box Plot":

        if len(continuous) > 0:
            col = st.selectbox("Column", continuous)
            fig = px.box(df, y=col, points="all")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric columns found")

    # ---------------- DISTRIBUTION GRID ----------------
    elif chart == "Distribution Grid":

        if len(continuous) > 0:

            selected = st.multiselect(
                "Select Columns",
                continuous,
                default=continuous[:2]
            )

            for col in selected:
                fig = px.box(df, y=col, title=f"Distribution of {col}")
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns found")

    # ---------------- PIE CHART ----------------
    elif chart == "Pie Chart":

        st.subheader("🥧 Pie Chart Distribution")

        pie_cols = [
            c for c in categorical
            if df[c].nunique() <= 15 and "id" not in c.lower()
        ]

        if len(pie_cols) == 0:
            st.warning("No suitable categorical columns for pie chart")
        else:

            col = st.selectbox("Select Column", pie_cols)

            data = df[col].value_counts().head(10)

            fig = px.pie(
                names=data.index,
                values=data.values,
                title=f"Distribution of {col}"
            )

            st.plotly_chart(fig, use_container_width=True)

    # ---------------- INSIGHTS ----------------
    st.subheader("🧠 Insights")
    for i in generate_insights(df):
        st.write("•", i)

    # ---------------- REPORT ----------------
    st.subheader("📈 Data Quality Report")
    st.write(report)