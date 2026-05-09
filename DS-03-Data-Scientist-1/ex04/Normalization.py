import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


def load(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    df_train = load("../Train_knight.csv")
    df_test = load("../Test_knight.csv")

    scaler = MinMaxScaler()
    Y_train = df_train["knight"]
    X_train = df_train.drop(columns=["knight"])
    X_test = df_test

    X_train_norm = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        )

    X_test_norm = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        )
    print("BEFORE:")
    print(X_train.head())
    print("\nAFTER:")
    print(X_train_norm.head())

    jedi = (Y_train == "Jedi")
    sith = (Y_train == "Sith")
    plt.scatter(X_train_norm.loc[jedi, 'Push'],
                X_train_norm.loc[jedi, 'Midi-chlorien'],
                alpha=0.5, c='blue', label="Jedi")
    plt.scatter(X_train_norm.loc[sith, 'Push'],
                X_train_norm.loc[sith, 'Midi-chlorien'],
                alpha=0.5, c='red', label="Sith")
    plt.xlabel("Push")
    plt.ylabel("Midi-chlorien")
    plt.legend()
    plt.savefig("Normalization.png")

