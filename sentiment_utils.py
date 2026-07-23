from googleapiclient.discovery import build
from textblob import TextBlob


def get_youtube_comments(video_id, api_key, max_results=50):
    youtube = build("youtube", "v3", developerKey=api_key)

    comments = []

    try:

        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_results, 100),
            textFormat="plainText"
        ).execute()

        for item in response.get("items", []):

            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

            comments.append(comment)

    except Exception:

        return []

    return comments


def get_video_details(video_id, api_key):

    youtube = build("youtube", "v3", developerKey=api_key)

    try:

        response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        items = response.get("items", [])

        if not items:
            return None

        snippet = items[0]["snippet"]

        return {
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["high"]["url"]
        }

    except Exception:

        return None


def analyze_sentiment(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.1:
        return "Positive"

    elif polarity < -0.1:
        return "Negative"

    else:
        return "Neutral"