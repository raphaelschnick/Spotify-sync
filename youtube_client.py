import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl

class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class Song(object):
    def __init__(self, track):
        self.track = track

class YoutubeClient(object):
    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    def get_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "/secrets/client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id, snippet",
            maxResults=50,
            mine=True
        )
        response = request.execute()

        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

        return playlists

    def get_videos_from_playlist(self, playlist_id):
        songs = []
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id, snippet"
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            track = self.get_artist_and_track_from_video(video_id)
            if track:
                songs.append(Song(track))

        return songs

    def get_artist_and_track_from_video(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download=False
        )

        track = video['title']

        return track