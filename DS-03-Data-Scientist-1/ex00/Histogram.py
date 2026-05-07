import pandas as pd
import matplotlib.pyplot as plt


def load(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_histogram(df: pd.DataFrame, output_path: str):
    features = df.columns
    n_feature = len(features)
    n_cols = 5
    n_rows = (n_feature + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 3 * n_rows))
    axes = axes.flatten()
    for idx, col in enumerate(features):
        axes[idx].hist(df[col], bins=40,
                       color="green", alpha=0.5, label="knight")
        axes[idx].set_title(col, fontsize=12)
        axes[idx].legend()

    # Hide any leftover empty subplots
    for idx in range(n_feature, n_rows * n_cols):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved {output_path}")


def train_histogram(df: pd.DataFrame, output_path: str):

    features = df.columns.drop("knight")
    jedi = df[df['knight'] == 'Jedi']
    sith = df[df['knight'] == 'Sith']
    n_feature = len(features)
    n_cols = 5
    n_rows = (n_feature + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 3 * n_rows))
    axes = axes.flatten()

    for idx, col in enumerate(features):
        axes[idx].hist(jedi[col], bins=40,
                       color="blue", alpha=0.5, label="Jedi")
        axes[idx].hist(sith[col], bins=40,
                       color="red", alpha=0.5, label="Sith")
        axes[idx].set_title(col, fontsize=12)
        axes[idx].legend()

    # Hide any leftover empty subplots
    for idx in range(n_feature, n_rows * n_cols):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved {output_path}")


if __name__ == "__main__":
    df_test = load("../Test_knight.csv")
    test_histogram(df_test, "Histogram_Test.png")

    df_train = load("../Train_knight.csv")
    train_histogram(df_train, "Histogram_Train.png")
