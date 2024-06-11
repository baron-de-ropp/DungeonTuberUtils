from flask import Flask, request, render_template, jsonify
import requests
import isodate

app = Flask(__name__)

API_KEY = 'AIzaSyAfb1RDnrusAp2uI19FHj-FEdPevf2KadM'


def convert_duration_to_seconds(duration):
    parsed_duration = isodate.parse_duration(duration)
    return int(parsed_duration.total_seconds())

def fetch_youtube_data(channel_id):
    video_ids = []
    next_page_token = ''
    
    while True:
        url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=50&type=video&pageToken={next_page_token}'
        response = requests.get(url).json()
        
        if 'items' not in response:
            print('Error fetching data:', response)
            return []

        video_ids.extend([item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video'])
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    video_data = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        stats_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={",".join(batch)}&key={API_KEY}'
        stats_response = requests.get(stats_url).json()
        
        if 'items' not in stats_response:
            print('Error fetching video stats:', stats_response)
            continue
        
        for video in stats_response['items']:
            duration_seconds = convert_duration_to_seconds(video['contentDetails']['duration'])
            
            # Exclude shorts (duration <= 60 seconds)
            if duration_seconds > 60:
                video_data.append(video)

    # Sort videos by published date and return the last twelve
    video_data.sort(key=lambda x: x['snippet']['publishedAt'], reverse=True)
    recent_videos = video_data[:12]
    
    return recent_videos




def calculate_sponsorship_rates(videos):
    cpms = [15, 20, 25, 30, 35, 40, 45]  # List of CPM values

    # Get the view counts of the last 12 videos
    view_counts = [int(video['statistics']['viewCount']) for video in videos]
    total_views = sum(view_counts)
    average_views = total_views / len(view_counts) if view_counts else 0

    # Calculate sponsorship rates for different CPM values
    rates = {}
    for cpm in cpms:
        rate = (average_views / 1000) * cpm
        rates[f'${cpm} CPM'] = rate

    return rates



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    channel_id = request.form['channel_id']
    videos = fetch_youtube_data(channel_id)

    
    if not videos:
        return jsonify({'error': 'No videos found or error fetching data.'}), 400

    rates = calculate_sponsorship_rates(videos)
    return jsonify({
        'videos': videos,
        'sponsorship_rates': rates
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


# UC5l5MjE1H1NP7Gh6VOZNfsQ
