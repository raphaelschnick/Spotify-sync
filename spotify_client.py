import requests

class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token

    def search_song(self, track):
        url = f"https://api.spotify.com/v1/search?q={track}&type=track"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer{self.api_token}"
            }
        )
        response_json = response.json()
        results = response_json['tracks']['items']
        if results:
            return results[0]['id']
        else:
            raise Exception(f"No song found for {track}")


    def add_song_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={
                "ids": [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer{self.api_token}"
            }
        )

        return response.ok