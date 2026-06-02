def suggest_graph(df):
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    text_cols = df.select_dtypes(include=['object']).columns

    # CASE 1: Time series
    for col in df.columns:
        if "date" in col.lower() or "year" in col.lower():
            return "line", col

    # CASE 2: Category + numeric → bar chart
    if len(text_cols) > 0 and len(numeric_cols) > 0:
        return "bar", text_cols[0]

    # CASE 3: 2 numeric columns → scatter
    if len(numeric_cols) >= 2:
        return "scatter", numeric_cols[:2]

    # CASE 4: Only numeric → histogram
    if len(numeric_cols) == 1:
        return "histogram", numeric_cols[0]

    return "none", None