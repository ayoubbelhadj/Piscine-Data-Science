import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score


def main():
    if len(sys.argv) != 3:
        print("Usage: ./KNN.py Train_knight.csv Test_knight.csv")
        sys.exit(1)

    train_df = pd.read_csv(sys.argv[1])
    test_df = pd.read_csv(sys.argv[2])

    X = train_df.drop(columns=['knight'])
    y = train_df['knight'].map({'Jedi': 0, 'Sith': 1})

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)

    k_values = range(1, 31)
    accuracies = []
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_scaled, y_train)
        pred = knn.predict(X_val_scaled)
        accuracies.append(accuracy_score(y_val, pred))

    best_k = k_values[int(np.argmax(accuracies))]
    best_acc = max(accuracies)
    print(f"Best K = {best_k}  (accuracy = {best_acc:.4f})")

    knn = KNeighborsClassifier(n_neighbors=best_k)
    knn.fit(X_train_scaled, y_train)
    pred = knn.predict(X_val_scaled)
    f1 = f1_score(y_val, pred, average='weighted')
    print(f"Validation f1-score: {f1 * 100:.2f}%")

    plt.figure(figsize=(8, 5))
    plt.plot(list(k_values), accuracies)
    plt.xlabel("k values")
    plt.ylabel("accuracy")
    plt.title("KNN accuracy vs k")
    plt.grid(True, alpha=0.3)
    plt.savefig("KNN.png")

    X_full_scaled = scaler.fit_transform(X)
    X_test_final = scaler.transform(test_df)
    knn_final = KNeighborsClassifier(n_neighbors=best_k)
    knn_final.fit(X_full_scaled, y)

    test_pred = knn_final.predict(X_test_final)
    labels = ['Jedi' if p == 0 else 'Sith' for p in test_pred]
    with open('KNN.txt', 'w') as f:
        for label in labels:
            f.write(label + '\n')
    print(f"Wrote {len(labels)} predictions to KNN.txt")


if __name__ == "__main__":
    main()
