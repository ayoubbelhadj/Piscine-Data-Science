import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score


def main():
    if len(sys.argv) != 3:
        print("Usage: ./Tree.py Train_knight.csv Test_knight.csv")
        sys.exit(1)

    train_df = pd.read_csv(sys.argv[1])
    test_df = pd.read_csv(sys.argv[2])

    X = train_df.drop(columns=['knight'])
    y = train_df['knight'].map({'Jedi': 0, 'Sith': 1})

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred_val = model.predict(X_val)

    f1 = f1_score(y_val, y_pred_val, average='weighted')
    print(f"Validation f1-score: {f1 * 100:.2f}%")

    model.fit(X, y)

    test_pred = model.predict(test_df)
    labels = ['Jedi' if p == 0 else 'Sith' for p in test_pred]

    with open('Tree.txt', 'w') as f:
        for label in labels:
            f.write(label + '\n')
    print(f"Wrote {len(labels)} predictions to Tree.txt")

    plt.figure(figsize=(20, 15))
    plot_tree(
        model.estimators_[0],
        feature_names=X.columns,
        class_names=['Jedi', 'Sith'],
        filled=True,
        rounded=True,
        fontsize=11
    )
    plt.title("One tree from the Random Forest")
    plt.savefig("Tree.png")


if __name__ == "__main__":
    main()
