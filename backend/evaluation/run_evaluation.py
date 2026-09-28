from evaluation.test_dataset import TEST_CASES
from matching.skill_matcher import match_skills

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


def main():
    y_true = []
    y_pred = []

    print("\nPRODUCTION MATCHING EVALUATION")
    print("=" * 60)

    for index, case in enumerate(TEST_CASES, start=1):

        candidate_skill = case["candidate_skill"]
        job_skill = case["job_skill"]

        results = match_skills(
            candidate_skills=[
                candidate_skill
            ],
            job_skills=[
                job_skill
            ],
        )

        predicted = results[0]["status"]
        expected = case["expected"]

        y_true.append(expected)
        y_pred.append(predicted)

        print(f"\nTest {index}")
        print(
            f"Candidate: "
            f"{candidate_skill['skill']}"
        )
        print(
            f"Job: "
            f"{job_skill['skill']}"
        )
        print(
            f"Expected: {expected}"
        )
        print(
            f"Predicted: {predicted}"
        )
        print(
            f"Similarity: "
            f"{results[0]['similarity_score']}"
        )
        print(
            f"Correct: "
            f"{'YES' if expected == predicted else 'NO'}"
        )

    # =====================================================
    # OVERALL ACCURACY
    # =====================================================

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    print("\n" + "=" * 60)

    print(
        f"Accuracy: {accuracy * 100:.2f}%"
    )

    # =====================================================
    # CLASSIFICATION REPORT
    # =====================================================

    print("\nCLASSIFICATION REPORT")
    print("=" * 60)

    print(
        classification_report(
            y_true,
            y_pred,
            labels=[
                "matched",
                "partial",
                "missing",
            ],
            target_names=[
                "Matched",
                "Partial",
                "Missing",
            ],
            zero_division=0,
        )
    )

    # =====================================================
    # CONFUSION MATRIX
    # =====================================================

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=[
            "matched",
            "partial",
            "missing",
        ],
    )

    print("CONFUSION MATRIX")
    print("=" * 60)

    print(
        "Rows    = Actual"
        "\nColumns = Predicted"
    )

    print(
        "\n             Matched  Partial  Missing"
    )

    print(
        f"Matched    {matrix[0][0]:8d}"
        f" {matrix[0][1]:8d}"
        f" {matrix[0][2]:8d}"
    )

    print(
        f"Partial    {matrix[1][0]:8d}"
        f" {matrix[1][1]:8d}"
        f" {matrix[1][2]:8d}"
    )

    print(
        f"Missing    {matrix[2][0]:8d}"
        f" {matrix[2][1]:8d}"
        f" {matrix[2][2]:8d}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()