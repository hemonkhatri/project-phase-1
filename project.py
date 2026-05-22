import argparse
import os

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def summarize_text(text):

    prompt = f"""
    Summarize the following text:

    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text


def translate_text(text, language):

    prompt = f"""
    Translate the following text into {language}:

    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text


def analyze_sentiment(text):

    prompt = f"""
    Analyze the sentiment of this text.

    Return:
    - Positive
    - Negative
    - Neutral

    Also provide a short explanation.

    Text:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text


def main():

    parser = argparse.ArgumentParser(
        description="Gemini AI CLI Tool"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Summarize command
    summarize_parser = subparsers.add_parser(
        "summarize",
        help="Summarize text"
    )

    summarize_parser.add_argument(
        "text",
        type=str,
        help="Text to summarize"
    )

    # Translate command
    translate_parser = subparsers.add_parser(
        "translate",
        help="Translate text"
    )

    translate_parser.add_argument(
        "text",
        type=str,
        help="Text to translate"
    )

    translate_parser.add_argument(
        "--to",
        required=True,
        help="Target language"
    )

    # Sentiment command
    sentiment_parser = subparsers.add_parser(
        "sentiment",
        help="Analyze sentiment"
    )

    sentiment_parser.add_argument(
        "text",
        type=str,
        help="Text for sentiment analysis"
    )

    args = parser.parse_args()

    try:

        if args.command == "summarize":

            result = summarize_text(args.text)

        elif args.command == "translate":

            result = translate_text(
                args.text,
                args.to
            )

        elif args.command == "sentiment":

            result = analyze_sentiment(args.text)

        else:
            result = "Invalid command"

        print("\n=== RESULT ===")
        print(result)

    except Exception as e:
        print(f"\nERROR: {e}")


if __name__ == "__main__":
    main()