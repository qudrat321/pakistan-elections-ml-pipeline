# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Single entrypoint to reproduce the entire Part A + Part B pipeline end to end."""

from src.pipeline_part_a import run_part_a
from src.train_part_b import train_and_evaluate


def main() -> None:
    """Run Part A data pipeline followed by Part B ML training and evaluation."""
    print(
        "=== Step 1/2: Running Part A (Data Cleaning, Validation, SQLite & Charts) ==="
    )
    run_part_a()

    print(
        "\n=== Step 2/2: Running Part B (ML Pipeline, Model Comparison & Error Analysis) ==="
    )
    train_and_evaluate()

    print("\nAll Part A and Part B deliverables generated successfully!")


if __name__ == "__main__":
    main()
