import requests

def get_youtube_data(channel_id):
    # Example function to fetch YouTube channel data
    # Note: You need to replace 'YOUR_API_KEY' with your actual YouTube Data API key
    api_key = 'AIzaSyAfb1RDnrusAp2uI19FHj-FEdPevf2KadM'
    base_url = 'https://www.googleapis.com/youtube/v3'
    
    # Fetch channel details
    channel_url = f"{base_url}/channels?part=snippet,contentDetails,statistics&id={channel_id}&key={api_key}"
    channel_response = requests.get(channel_url)
    channel_data = channel_response.json()

    # Fetch recent videos
    uploads_playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos_url = f"{base_url}/playlistItems?part=snippet&playlistId={uploads_playlist_id}&maxResults=5&key={api_key}"
    videos_response = requests.get(videos_url)
    videos_data = videos_response.json()

    return {
        'channel_data': channel_data,
        'videos_data': videos_data
    }
