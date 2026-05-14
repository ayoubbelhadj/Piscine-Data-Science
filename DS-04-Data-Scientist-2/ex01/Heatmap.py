import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    df = load("../Train_knight.csv")
    if df is None:
        sys.exit(1)
    df['knight'] = df['knight'].map({'Jedi': 0, 'Sith': 1})

    corr = df.corr()

    plt.figure(figsize=(14, 12))
    sns.heatmap(corr)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("Heatmap.png")


if __name__ == "__main__":
    main()
