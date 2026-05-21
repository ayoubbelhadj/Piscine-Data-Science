import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score


def main():
    if len(sys.argv) != 3:
        print("Usage: ./democracy.py Train_knight.csv Test_knight.csv")
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

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=11)
    lr = LogisticRegression(max_iter=1000, random_state=42)

    voting = VotingClassifier(
        estimators=[('rf', rf), ('knn', knn), ('lr', lr)],
        voting='soft'
    )

    print(f"{'Model':<22}{'f1':>8}{'accuracy':>12}")
    for name, model in [
        ('Random Forest', rf),
        ('KNN', knn),
        ('Logistic Regression', lr),
        ('Voting Classifier', voting),
    ]:
        model.fit(X_train_scaled, y_train)
        pred = model.predict(X_val_scaled)
        f1 = f1_score(y_val, pred, average='weighted')
        acc = accuracy_score(y_val, pred)
        print(f"{name:<22}{f1:>8.4f}{acc:>12.4f}")

    X_full_scaled = scaler.fit_transform(X)
    X_test_scaled = scaler.transform(test_df)
    voting.fit(X_full_scaled, y)

    test_pred = voting.predict(X_test_scaled)
    labels = ['Jedi' if p == 0 else 'Sith' for p in test_pred]
    with open('Voting.txt', 'w') as f:
        for label in labels:
            f.write(label + '\n')
    print(f"\nWrote {len(labels)} predictions to Voting.txt")


if __name__ == "__main__":
    main()
