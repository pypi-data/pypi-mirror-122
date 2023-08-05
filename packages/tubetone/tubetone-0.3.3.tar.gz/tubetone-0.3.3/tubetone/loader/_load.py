import ssl

from pytube import Playlist, YouTube
from youtube_transcript_api import TranscriptsDisabled

from tubetone import constants
from tubetone.analysis import get_tone, frequency
from tubetone.models import ToneTube
from tubetone.utils import youtube
from tubetone.utils.operations import eyesore


def tone_playlist(playlist_id="PLY8fdk-3N0jC7JM_PCjHqZRTxr8KB41YA", lang='ru', amount=-1):
    """
    Loads loader videos and creates toned info for them

    :param amount: how many last videos to process, -1 means all
    :param playlist_id: youtube loader id
    :param lang: default loader language

    """
    print(f"loading playlist {playlist_id} data. will process {amount} videos.")
    _free_ssl()
    playlist = Playlist(f'{constants.YOUTUBE_PLAYLIST_PRE_URL}{playlist_id}')
    videos = playlist.videos

    if amount > 0:
        videos = videos[:amount]

    toned_videos = []
    for video in videos:
        toned_video = tone_video(playlist, video, lang=lang)
        if toned_video:
            toned_videos.append(toned_video)

    return toned_videos


def tone_video(playlist: Playlist, video: YouTube, lang: str = 'ru'):
    """
    Creates video object with additional info on it's tone and some default analysis.

    :param playlist: loader which the video belongs to (can be None)
    :param video: YouTube video
    :param lang: default lang
    :return: ToneTube or None if no transcript info
    """
    video_id = video.video_id
    captions = video.caption_tracks

    for cap in captions:
        print(cap)

    try:
        transcript = youtube.get_video_transcript(video_id, lang)

        meta = youtube.get_video_info(video)
        video_data = dict(meta)
        video_data['transcript'] = transcript
        video_data['lang'] = lang

        all_text = ""
        for text_chunk in transcript:
            if not eyesore(text_chunk['text']):
                all_text = all_text + " " + text_chunk['text']
        video_data['full_text'] = all_text
        tone_analysis = get_tone(video.title + all_text)
        morph_analysis = frequency(all_text).most_common(20)
        video_data['tone_analysis'] = tone_analysis
        video_data['morph_analysis'] = dict(morph_analysis)

        if playlist is not None:
            video_data['playlist_name'] = playlist.title
            video_data['playlist_id'] = playlist.playlist_id

        return ToneTube(**video_data)
    except TranscriptsDisabled as e:
        return None


def load_last_video(playlist_id, lang='ru'):
    arr = tone_playlist(playlist_id, lang=lang, amount=1)
    if len(arr):
        return arr[0]
    else:
        return None


def _free_ssl():
    """
    Ugly workaround for it to work on mac
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ssl._create_default_https_context = ssl._create_unverified_context
