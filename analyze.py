import pandas as pd
import ast
from collections import Counter

def analyze_dataset(file_path="dataset.csv"):
    # Load dataset
    df = pd.read_csv(file_path)

    print("\n=== Dataset Overview ===")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"Columns: {list(df.columns)}\n")

    # Check missing values
    print("=== Missing Values ===")
    print(df.isnull().sum(), "\n")

    # Basic stats
    print("=== Basic Statistics ===")
    print(df.describe(include="all").transpose(), "\n")

    # Leaning distribution
    print("=== Leaning Distribution ===")
    lean_sums = {
        "Left": df["leaning_left"].sum(),
        "Center": df["center"].sum(),
        "Right": df["leaning_right"].sum(),
        "Total": df["total_source"].sum()
    }
    for k, v in lean_sums.items():
        print(f"{k:<7}: {v}")
    print()

    # Balance check
    print("=== Balance Check (Proportion %) ===")
    total = lean_sums["Total"]
    for k in ["Left", "Center", "Right"]:
        pct = (lean_sums[k] / total) * 100 if total else 0
        print(f"{k:<7}: {pct:.2f}%")
    print()

    # Parse list-like columns safely
    def parse_list(cell):
        try:
            return ast.literal_eval(cell) if isinstance(cell, str) else []
        except:
            return []

    df["left_points"] = df["left_points"].apply(parse_list)
    df["center_points"] = df["center_points"].apply(parse_list)
    df["right_points"] = df["right_points"].apply(parse_list)
    df["sources"] = df["sources"].apply(parse_list)

    # Average sources per event
    print("=== Source Statistics ===")
    print(f"Average total sources per event: {df['total_source'].mean():.2f}")
    print(f"Max sources in an event: {df['total_source'].max()}")
    print(f"Min sources in an event: {df['total_source'].min()}\n")

    # Top mentioned sources
    # print("=== Top Sources (across dataset) ===")
    # all_sources = [s for sublist in df["sources"] for s in sublist]
    # counter = Counter(all_sources)
    # for source, count in counter.most_common(10):
    #     print(f"{source:<25} {count}")
    # print()

    # # Event-wise leaning diversity
    # print("=== Leaning Diversity (per event) ===")
    # df["diversity_score"] = (df[["leaning_left","center","leaning_right"]] > 0).sum(axis="columns")
    # diversity_counts = df["diversity_score"].value_counts().sort_index()
    # for score, count in diversity_counts.items():
    #     print(f"Events with {score} different leanings: {count}")
    # print()

    # Longest & shortest titles (for fun)
    print("=== Title Lengths ===")
    df["title_len"] = df["title"].astype(str).apply(len)
    print(f"Average title length: {df['title_len'].mean():.1f} chars")
    print("Shortest title:", df.loc[df["title_len"].idxmin(), "title"])
    print("Longest title :", df.loc[df["title_len"].idxmax(), "title"])

if __name__ == "__main__":
    analyze_dataset()
