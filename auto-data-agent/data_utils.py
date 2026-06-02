import pandas as pd


def clean_data(df):

    report = {}

    report["rows_before"] = len(df)
    report["missing_before"] = int(df.isnull().sum().sum())
    report["duplicates_before"] = int(df.duplicated().sum())

    df = df.drop_duplicates()

    missing_filled = 0

    for col in df.columns:
        if df[col].isnull().sum() > 0:
            missing_filled += df[col].isnull().sum()
            mode = df[col].mode()
            if len(mode) > 0:
                df[col] = df[col].fillna(mode[0])
            else:
                df[col] = df[col].fillna("Unknown")

    report["missing_filled"] = int(missing_filled)
    report["rows_after"] = len(df)
    report["missing_after"] = int(df.isnull().sum().sum())
    report["duplicates_after"] = int(df.duplicated().sum())

    return df, report


def classify_columns(df):
    continuous = []
    categorical = []
    identifiers = []

    n = len(df)

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            nunique = df[col].nunique(dropna=True)
            unique_ratio = nunique / n if n > 0 else 0
            if unique_ratio > 0.95 and nunique > 20:
                identifiers.append(col)
            elif nunique > 15:
                continuous.append(col)
            else:
                categorical.append(col)
        else:
            categorical.append(col)

    return continuous, categorical, identifiers