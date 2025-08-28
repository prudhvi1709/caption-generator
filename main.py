import argparse
from utils import upload_video_file, video_compressor
from gemini_client import generate_raw_subtitles
from openai_client import call_openai


def main():
    parser = argparse.ArgumentParser(description="Generate subtitles for a video file.")
    parser.add_argument("video", help="Path to the video file")
    parser.add_argument("-srt", "--subtitle", required=True, help="Path where the subtitles should be saved (.srt)")

    args = parser.parse_args()

    output_path = video_compressor(args.video)

    file_obj = upload_video_file(output_path)
    raw_subtitles = generate_raw_subtitles(file_obj)
    final_subtitles = call_openai(raw_subtitles)

    # Save to output file
    with open(args.subtitle, "w", encoding="utf-8") as f:
        f.write(final_subtitles)

    print(f"✅ Subtitles saved to {args.subtitle}")


if __name__ == "__main__":
    main()
