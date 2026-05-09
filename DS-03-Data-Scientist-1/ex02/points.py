import matplotlib.pyplot as plt
import pandas as pd


def load(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


def plot_scatter(ax, df, x_col, y_col, target_col=None):
    if target_col is not None:
        jedi = df[df[target_col] == 'Jedi']
        sith = df[df[target_col] == 'Sith']
        ax.scatter(sith[x_col], sith[y_col], c='red', alpha=0.4, label='Sith')
        ax.scatter(jedi[x_col], jedi[y_col], c='blue', alpha=0.4, label='Jedi')
    else:
        ax.scatter(df[x_col], df[y_col], c='green', alpha=0.5, label='Knight')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend()


if __name__ == "__main__":
    df_train = load("../Train_knight.csv")
    df_test = load("../Test_knight.csv")

    pair_clean = ('Empowered', 'Prescience')
    pair_mixed = ('Push', 'Midi-chlorien')

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    plot_scatter(axes[0, 0], df_train, *pair_clean, target_col='knight')
    plot_scatter(axes[0, 1], df_train, *pair_mixed, target_col='knight')
    plot_scatter(axes[1, 0], df_test, *pair_clean)
    plot_scatter(axes[1, 1], df_test, *pair_mixed)
    plt.tight_layout()
    plt.savefig('points.png')
    plt.show()
