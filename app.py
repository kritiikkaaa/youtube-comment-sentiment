from flask import Flask, render_template, request
from sentiment_utils import (
    get_youtube_comments,
    analyze_sentiment,
    get_video_details
)
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

API_KEY = "AIzaSyBJk_hrKiiA11qckKs2UUy_jVMsVRRlD18"


def extract_video_id(url):
    """
    Extract YouTube Video ID from different URL formats.
    """

    try:
        if "youtu.be/" in url:
            return url.split("/")[-1].split("?")[0]

        parsed = urlparse(url)

        if parsed.hostname in [
            "www.youtube.com",
            "youtube.com"
        ]:

            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [None])[0]

            elif parsed.path.startswith("/shorts/"):
                return parsed.path.split("/")[2]

            elif parsed.path.startswith("/embed/"):
                return parsed.path.split("/")[2]

        return None

    except:
        return None


@app.route("/", methods=["GET", "POST"])
def home():

    results = []

    positive = 0
    neutral = 0
    negative = 0

    total = 0

    video = None

    video_url = ""

    error = None

    if request.method == "POST":

        video_url = request.form.get("video_id", "").strip()

        video_id = extract_video_id(video_url)

        if not video_id:

            error = "Please enter a valid YouTube URL."

        else:

            try:

                video = get_video_details(video_id, API_KEY)

                comments = get_youtube_comments(
                    video_id,
                    API_KEY,
                    50
                )

                if len(comments) == 0:

                    error = "No comments found."

                else:

                    for comment in comments:

                        sentiment = analyze_sentiment(comment)

                        if sentiment == "Positive":

                            positive += 1

                        elif sentiment == "Negative":

                            negative += 1

                        else:

                            neutral += 1

                        results.append(
                            (comment, sentiment)
                        )

                    total = len(results)

            except Exception:

                error = "Unable to fetch comments. Please try another video."

    return render_template(

        "index.html",

        video=video,

        results=results,

        positive=positive,

        neutral=neutral,

        negative=negative,

        total=total,

        error=error,

        video_url=video_url

    )


if __name__ == "__main__":
    app.run(debug=True)