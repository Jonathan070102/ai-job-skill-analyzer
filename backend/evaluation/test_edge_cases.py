from matching.gap_analyzer import analyze_skill_gap
from nlp.skill_extractor import extract_skills
from parsers.text_cleaner import clean_text


def test_empty_text():
    result = extract_skills("")

    assert result == []

    print("✓ Empty text handled")


def test_whitespace_text():
    result = extract_skills("   \n   ")

    assert result == []

    print("✓ Whitespace-only text handled")


def test_cleaner_empty_text():
    result = clean_text("   \n\n   ")

    assert result == ""

    print("✓ Empty text cleaning handled")


def test_empty_gap_analysis():
    result = analyze_skill_gap([])

    assert result["coverage_score"] == 0.0
    assert result["total_requirements"] == 0
    assert result["matched_count"] == 0
    assert result["partial_count"] == 0
    assert result["missing_count"] == 0

    print("✓ Empty gap analysis handled")


def test_duplicate_text():
    text = """
    Python Python Python
    Git Git
    """

    result = extract_skills(text)

    skill_names = [
        item["skill"]
        for item in result
    ]

    assert "Python" in skill_names
    assert "Git" in skill_names

    print("✓ Repeated skills handled")


def test_unrelated_text():
    text = """
    This document contains no known technical
    skills or technologies.
    """

    result = extract_skills(text)

    assert result == []

    print("✓ No-skill text handled")


def main():
    print("\nEDGE CASE TESTS")
    print("=" * 60)

    test_empty_text()
    test_whitespace_text()
    test_cleaner_empty_text()
    test_empty_gap_analysis()
    test_duplicate_text()
    test_unrelated_text()

    print("=" * 60)
    print("All edge-case tests passed.")


if __name__ == "__main__":
    main()