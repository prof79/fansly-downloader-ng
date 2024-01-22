"""MPEG-4 Binary File Manipulation"""


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


class MP4Box(object):
    """Represents an MPEG-4 binary box/atom object.
    """
    def __init__(self, size_bytes: bytes, fourcc_bytes: bytes, position: int) -> None:
        self.position = position
        self.size = int.from_bytes(size_bytes, byteorder='big')
        self.fourcc = str(fourcc_bytes, encoding='ascii')


    def __str__(self) -> str:
        return f'MP4Box ( Position: {self.position}, FourCC: {self.fourcc}, Size: {self.size} )'



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
            raise RuntimeError(f'Not an MP4 file.')
        
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
        raise RuntimeError('File is too small.')

    if print is not None:
        print(f'File: {file_name}')
        print()

    with open(file_name, 'rb') as mp4file:
        
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
