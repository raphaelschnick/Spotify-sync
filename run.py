from /secrets/secrets import spotify_token, spotify_user_id

from youtube_client import YoutubeClient
from spotify_client import SpotifyClient

def run():
    youtube_client = YoutubeClient()
    spotify_client = SpotifyClient(spotify_token)
    playlists = youtube_client.get_playlists()

    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter your Playlist choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")

    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(songs)}")

    for song in songs:
        spotify_song_id = spotify_client.search_song(song.track)
        if spotify_song_id:
            added_song = spotify_client.add_song_to_spotify(spotify_song_id)
            if added_song:
                print(f"Added {song.track}")

if __name__ == '__main__':
    run()