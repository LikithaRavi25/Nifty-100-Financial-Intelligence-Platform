from pathlib import Path

LOG_FILE = Path("output/ratio_edge_cases.log")


def reset_log():
    """
    Clear the log file before every run.
    """
    LOG_FILE.parent.mkdir(exist_ok=True)

    with open(LOG_FILE, "w") as f:
        f.write("RATIO EDGE CASE LOG\n")
        f.write("=" * 60 + "\n")


def log_case(
    company,
    year,
    ratio,
    calculated,
    source,
    category
):
    """
    Append one anomaly to the log file.
    """

    with open(LOG_FILE, "a") as f:

        f.write(
            f"{company} | "
            f"{year} | "
            f"{ratio} | "
            f"Calculated={calculated} | "
            f"Source={source} | "
            f"{category}\n"
        )