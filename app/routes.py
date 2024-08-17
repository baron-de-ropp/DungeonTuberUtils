from flask import render_template, request, Blueprint
from youtube_utils import get_youtube_data

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/tool')
def tool():
    return render_template('tool.html')

@main.route('/youtube', methods=['GET', 'POST'])
def youtube():
    if request.method == 'POST':
        channel_id = request.form['channel_id']
        data = get_youtube_data(channel_id)
        return render_template('youtube.html', channel_data=data['channel_data'], videos_data=data['videos_data'])
    return render_template('youtube.html', channel_data=None, videos_data=None)
