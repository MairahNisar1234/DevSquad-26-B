def evaluate_agent(df, report):

    score = 100

    # Missing values improvement
    if report["missing_before"] > 0:
        improvement = (
            report["missing_before"] -
            report["missing_after"]
        )
        score += min(improvement, 20)

    # Duplicate handling
    score += min(report["duplicates_before"], 15)

    # Outlier detection contribution
    score += min(report["outliers_detected"], 15)

    return max(min(score, 100), 0)