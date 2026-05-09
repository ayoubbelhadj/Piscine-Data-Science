import pandas as pd


def load(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    df = load("../Train_knight.csv")
    df["knight"] = df["knight"].map({"Sith": 0, "Jedi": 1})
    correlations = df.corr()["knight"].abs().sort_values(ascending=False)
    print(correlations.to_string())
