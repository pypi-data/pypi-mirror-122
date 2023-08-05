# __main__.py

from tubetone.db import save_video_data
from tubetone.loader import tone_playlist


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--type', metavar='type', required=False,
                        help='playlist or video', default='playlist')
    parser.add_argument('--id', metavar='id', required=True,
                        help='playlist id')
    parser.add_argument('--amount', metavar='amount', required=False,
                        help='how many of the latest video to parse', default=5)

    parser.add_argument('--db_url', metavar='db_url', required=False,
                        help='db url: will save here if provided', default=None)
    args = parser.parse_args()

    id = args.id
    if args.type == 'playlist':
        amount = args.amount
        toned_vides = tone_playlist(playlist_id=id, amount=amount)
        for toned_video in toned_vides:
            if args.db_url:
                save_video_data(toned_video)
            else:
                toned_video.view_main()
    elif type == 'video':
        raise Exception("Not processing videos yet")


if __name__ == "__main__":
    main()
