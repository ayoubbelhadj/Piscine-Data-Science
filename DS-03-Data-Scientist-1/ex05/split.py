import sys
import pandas as pd
from sklearn.model_selection import train_test_split


def load(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <Train_knight.csv>")
        sys.exit(1)
    df = load(sys.argv[1])
    if df is None:
        sys.exit(1)

    train_df, val_df = train_test_split(
        df,
        test_size=0.20,
        stratify=df['knight'],
        random_state=42
    )
    val_df.to_csv("Validation_knight.csv", index=False)
    train_df.to_csv("Training_knight.csv", index=False)


if __name__ == "__main__":
    main()