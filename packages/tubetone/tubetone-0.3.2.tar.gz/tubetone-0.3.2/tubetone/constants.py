import os
# DB
DB_URL = os.getenv("TUBETONE_DB_URL",
                   "mongodb+srv://aragorn:#aragorn#@cluster0.dlx9j.mongodb.net/tubetune?retryWrites=true&w=majority")
COLLECTION_VIDEOS = "video"
COLLECTION_PLAYLISTS = "playlists"
DB_NAME = "tubetune"

# youtube
YOUTUBE_PLAYLIST_PRE_URL = os.getenv('TUBETONE_YOUTUBE_PLAYLIST_PRE_URL', 'https://www.youtube.com/playlist?list=')
