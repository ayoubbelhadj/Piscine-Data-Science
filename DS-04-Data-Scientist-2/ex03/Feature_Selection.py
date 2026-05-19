import sys
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor


def load(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


def compute_vif(df):
    vif = pd.DataFrame(index=df.columns)
    vif['VIF'] = [
        variance_inflation_factor(df.values, i)
        for i in range(df.shape[1])
    ]
    vif['Tolerance'] = 1 / vif['VIF']
    return vif


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "Train_knight.csv"

    df = load(path)
    if df is None:
        sys.exit(1)
    if 'knight' in df.columns:
        df = df.drop(columns=['knight'])

    print("Initial VIF table:")
    print(compute_vif(df))
    print()

    while True:
        vif = compute_vif(df)
        max_vif = vif['VIF'].max()
        if max_vif < 5:
            break
        worst_feature = vif['VIF'].idxmax()
        print(f"Dropping '{worst_feature}' (VIF = {max_vif:.2f})")
        df = df.drop(columns=[worst_feature])

    print()
    print("Final VIF table (all VIFs < 5):")
    print(compute_vif(df))
    print()
    print(f"Kept features ({len(df.columns)}):")
    print(list(df.columns))


if __name__ == "__main__":
    main()
