"""MPEG-4 Binary File Manipulation

Kudos to Alfred Gutierrez' (alfg) and Sanjeev Pandey's well-summarizing articles:

https://dev.to/alfg/a-quick-dive-into-mp4-57fo
https://sanjeev-pandey.medium.com/understanding-the-mpeg-4-moov-atom-pseudo-streaming-in-mp4-93935e1b9e9a
"""


__all__ = [
    'MP4Box',
    'hash_mp4file',
    'get_boxes',
    'hash_mp4box',
]


import os

from io import BufferedReader
from pathlib import Path
from typing import Iterable, Optional, Callable

from errors.mp4 import InvalidMP4Error


class MP4Box(object):
    """Represents an MPEG-4 binary box/atom object.
    """
    def __init__(self, size_bytes: bytes, fourcc_bytes: bytes, position: int) -> None:
        self.position = position
        self.size = int.from_bytes(size_bytes, byteorder='big')
        self.fourcc = MP4Box.convert_to_fourcc(fourcc_bytes)


    def __str__(self) -> str:
        return f'MP4Box ( Position: {self.position}, FourCC: {self.fourcc}, Size: {self.size} )'


    @staticmethod
    def convert_to_fourcc(fourcc_bytes: bytes) -> str:
        fourcc: str = ''

        try:
            fourcc = str(fourcc_bytes, encoding='ascii')
        
        except UnicodeDecodeError:
            for by in fourcc_bytes:
                # See: http://facweb.cs.depaul.edu/sjost/it212/documents/ascii-pr.htm
                # 32-126 inclusive
                by_str: str = ''

                if (by < 32 or by > 126):
                    by_str = f'[{by}]'
                
                else:
                    by_str = chr(by)

                fourcc += by_str

        return fourcc



def get_boxes(reader: BufferedReader) -> Iterable[MP4Box]:
    position = 0
    first = True

    while reader.peek():
        box = MP4Box(
            size_bytes=reader.read(4),
            fourcc_bytes=reader.read(4),
            position=position,
        )

        if first and box.fourcc != 'ftyp':
            raise InvalidMP4Error(f'File header missing, not an MPEG-4 file.')
        
        first = False

        position += box.size

        reader.seek(position, os.SEEK_SET)

        yield box


def hash_mp4box(algorithm, reader: BufferedReader, box: MP4Box):
    """Hashes an MPEG-4 box atom.
    
    `algorithm` must be a `hashlib` algorithm.
    """
    CHUNK_SIZE = 1_048_576

    reader.seek(box.position, os.SEEK_SET)

    chunks = box.size // CHUNK_SIZE
    remainder = box.size - chunks*CHUNK_SIZE

    for _ in range(chunks):
        algorithm.update(reader.read(CHUNK_SIZE))
    
    algorithm.update(reader.read(remainder))


def hash_mp4file(
            algorithm,
            file_name: Path,
            print: Optional[Callable]=None
        ) -> str:

    if not file_name.exists():
        raise RuntimeError(f'{file_name} does not exist.')

    file_size = file_name.stat().st_size

    if file_size < 8:
        raise InvalidMP4Error(f'{file_name} is too small to be an MPEG-4 file.')

    if print is not None:
        print(f'File: {file_name}')
        print()

    with open(file_name, 'rb') as mp4file:
        
        try:
            boxes = get_boxes(mp4file)

            for box in boxes:
                if print is not None:
                    print(box)

                if box.fourcc != 'moov' and box.fourcc != 'mdat':
                    hash_mp4box(algorithm, mp4file, box)
            
            if print is not None:
                print()
                print(f'Hash: {algorithm.hexdigest()}')
                print()

            return algorithm.hexdigest()

        except InvalidMP4Error as ex:
            raise InvalidMP4Error(f'{file_name}: {ex}')
