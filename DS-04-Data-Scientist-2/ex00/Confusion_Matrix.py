import sys
import numpy as np
import matplotlib.pyplot as plt


def load_labels(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def compute_metrics(tp, fn, fp, tn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) \
        if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def main():
    if len(sys.argv) != 3:
        print("Usage: ./Confusion_Matrix.py predictions.txt truth.txt")
        sys.exit(1)

    predictions = load_labels(sys.argv[1])
    truth = load_labels(sys.argv[2])

    if len(predictions) != len(truth):
        print(f"Error: files have different lengths "
              f"({len(predictions)} vs {len(truth)})")
        sys.exit(1)

    # Count the 4 outcomes with Jedi as the positive class
    TP = FN = FP = TN = 0
    for i in range(len(predictions)):
        if truth[i] == "Jedi" and predictions[i] == "Jedi":
            TP += 1
        elif truth[i] == "Jedi" and predictions[i] == "Sith":
            FN += 1
        elif truth[i] == "Sith" and predictions[i] == "Sith":
            TN += 1
        elif truth[i] == "Sith" and predictions[i] == "Jedi":
            FP += 1

    # Metrics for Jedi
    p_jedi, r_jedi, f1_jedi = compute_metrics(TP, FN, FP, TN)
    # Metrics for Sith
    p_sith, r_sith, f1_sith = compute_metrics(TN, FP, FN, TP)

    total = TP + FN + FP + TN
    total_jedi = TP + FN
    total_sith = FP + TN
    accuracy = (TP + TN) / total if total > 0 else 0.0

    # Print the classification report
    print(
        f"{'':>8}{'precision':>10}{'recall':>10}{'f1-score':>10}{'total':>10}"
    )
    print(
        f"{'Jedi':<8}"
        f"{p_jedi:>10.2f}{r_jedi:>10.2f}{f1_jedi:>10.2f}{total_jedi:>10}"
    )
    print(
        f"{'Sith':<8}"
        f"{p_sith:>10.2f}{r_sith:>10.2f}{f1_sith:>10.2f}{total_sith:>10}"
    )
    print()
    print(f"{'accuracy':<8}{'':>10}{'':>10}{accuracy:>10.2f}{total:>10}")
    print()

    matrix = np.array([[TP, FN], [FP, TN]])
    print(matrix)

    # Display heatmap
    fig, ax = plt.subplots()
    im = ax.imshow(matrix)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Jedi', 'Sith'])
    ax.set_yticklabels(['Jedi', 'Sith'])
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    # Write the count inside each cell
    for i in range(2):
        for j in range(2):
            ax.text(j, i, matrix[i, j], ha='center', va='center',
                    color='white', fontsize=20)
    fig.colorbar(im)
    plt.title('Confusion Matrix')
    plt.savefig("Confusion_Matrix.png")


if __name__ == "__main__":
    main()
