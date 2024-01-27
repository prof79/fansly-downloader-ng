"""MPEG-4 Selective Hashing Tool"""


import argparse
import hashlib

from pathlib import Path
from rich import print

from fileio.mp4 import hash_mp4file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Hashes an MPEG-4 except the "moov" and "mdat" portions using MD5.',
    )

    parser.add_argument(
        dest='file',
        metavar='FILE',
        help='MPEG4 file',
    )

    parser.add_argument(
        '-d', '--debug',
        required=False,
        action='store_true',
        default=False,
        help='Debug output',
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    file_name = Path(args.file)

    md5 = hashlib.md5()

    hash = hash_mp4file(md5, file_name, print=print if args.debug else None)

    print(f'{hash}\t*{file_name.name}')


if __name__ == '__main__':
    try:
        main()
    
    except KeyboardInterrupt:
        pass

    except Exception as ex:
        print()
        print(f"Unexpected error: {ex}")
        print()
        print()
