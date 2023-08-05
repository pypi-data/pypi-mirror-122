from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


def get_video_transcript(video_id, langcode):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    for transcript in transcript_list:
        if langcode in transcript.language_code:
            our_transcript = transcript
            break
        print(transcript.language_code)

    transcript_json_array = our_transcript.fetch()
    return transcript_json_array


def get_video_info(movie: YouTube):
    movie_data = {
        'title': movie.title,
        'video_id': movie.video_id,
        'url': movie.watch_url,
        'rating': movie.rating,
        'views': movie.views,
        'description': movie.description.replace('\n', ''),
        'publish_date': movie.publish_date,
        'author': movie.author,
        'keywords': movie.keywords
    }
    return movie_data
