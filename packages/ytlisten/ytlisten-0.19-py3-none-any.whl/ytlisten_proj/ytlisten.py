import argparse
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import vlc
import pytube

# Set up the YouTube Data API v3 client
API_KEY = os.environ["YT_API_KEY"]
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION, developerKey=API_KEY)


def get_video_url(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=API_KEY)
    request = youtube.search().list(
        part="id",
        q=query,
        type="video",
        videoDefinition="high",
        maxResults=1
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return f"https://www.youtube.com/watch?v={video_id}"


def download_audio(url):
    video = pytube.YouTube(url)
    audio_stream = video.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download()
    return audio_file


def play_audio(audio_file):
    player = vlc.MediaPlayer(audio_file)
    player.play()
    return player


def main():
    parser = argparse.ArgumentParser(
        description='Listen to audio of YouTube videos from the command line.')
    parser.add_argument('query', nargs='+', help='search query for YouTube')
    args = parser.parse_args()

    # Get the search query from the command line arguments
    query = ' '.join(args.query)

    try:
        url = get_video_url(query)
        audio_file = download_audio(url)
        player = play_audio(audio_file)

        input("Press enter to stop playback")

        player.stop()
        os.remove(audio_file)

    except HttpError as e:
        print(f'An error occurred: {e}')


if __name__ == "__main__":
    main()
