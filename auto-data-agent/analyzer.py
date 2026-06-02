import pandas as pd


# ---------------- INSIGHTS ENGINE ----------------
def generate_insights(df):

    insights = []

    insights.append(f"Rows: {df.shape[0]}")
    insights.append(f"Columns: {df.shape[1]}")

    # numeric columns
    num = df.select_dtypes(include=["number"])

    if not num.empty:
        insights.append(f"Highest mean column: {num.mean().idxmax()}")
        insights.append(f"Lowest mean column: {num.mean().idxmin()}")

    # categorical insights
    for col in df.select_dtypes(include=["object"]).columns:

        if df[col].dropna().empty:
            continue

        top_val = df[col].value_counts().idxmax()
        top_count = df[col].value_counts().max()

        insights.append(
            f"Most common {col}: '{top_val}' ({top_count} times)"
        )

    return insights

