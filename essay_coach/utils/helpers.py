"""
Helper functions for Essay Coach
"""


def read_essay_from_file(filepath: str) -> str:
    """
    Read essay content from a file

    Args:
        filepath: Path to the essay file

    Returns:
        Essay content as string
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Essay file not found: {filepath}")


def save_feedback_to_file(feedback: dict, output_path: str) -> None:
    """
    Save coaching feedback to a file

    Args:
        feedback: Feedback dictionary
        output_path: Path to save the feedback
    """
    import json

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(feedback, f, ensure_ascii=False, indent=2)


def format_feedback_for_display(feedback: dict) -> str:
    """
    Format feedback for console display

    Args:
        feedback: Feedback dictionary

    Returns:
        Formatted feedback string
    """
    # TODO: Implement formatting logic
    pass
