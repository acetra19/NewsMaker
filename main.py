"""Entry point for Content-Farm bot."""
import argparse
from pathlib import Path

from pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Content-Farm: Reddit to Shorts pipeline")
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload the rendered video to YouTube",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for output video (default: output/)",
    )
    args = parser.parse_args()

    result = run_pipeline(upload_to_youtube=args.upload, output_dir=args.output_dir)
    if result:
        print(f"Done. Video: {result}")
    else:
        print("No candidate found or pipeline failed.")


if __name__ == "__main__":
    main()
