import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def load(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "Train_knight.csv"

    df = load(path)
    if df is None:
        sys.exit(1)

    if 'knight' in df.columns:
        df = df.drop(columns=['knight'])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)

    pca = PCA()
    pca.fit(X_scaled)

    variances = pca.explained_variance_ratio_ * 100

    cumulative = np.cumsum(variances)

    print("Variances (Percentage):")
    print(variances)
    print()
    print("Cumulative Variances (Percentage):")
    print(cumulative)

    plt.figure(figsize=(12, 7))
    plt.plot(range(1, len(cumulative) + 1), cumulative)
    plt.xlabel("Number of components")
    plt.ylabel("Explained variance (%)")
    plt.savefig("variances.png")


if __name__ == "__main__":
    main()
