from av2.stream import Stream
from typing import Tuple, Dict, Any
from av.video.stream import VideoStream as AvVideoStream
from fractions import Fraction


class VideoStream:
    id: int
    index: int
    language: str
    average_rate: Fraction
    base_rate: Fraction
    duration: int
    frames: int
    guessed_rate: Fraction
    metadata: Dict[str, str]
    profile: str
    start_time: int
    time_base: Fraction
    type: str

    def __init__(self, av1_video_stream: AvVideoStream) -> None:
        self.av1_video_stream = av1_video_stream

    def dict(self, fraction: bool = False) -> Dict[str, Any]:
        """
        fraction: Whether to keep the fraction, if True then Fraction, if False then float
        """
        _d = {
            'id': self.id,
            'index': self.index,
            'language': self.language,
            'average_rate': self.average_rate,
            'base_rate': self.base_rate,
            'duration': self.duration,
            'frames': self.frames,
            'guessed_rate': self.guessed_rate,
            'metadata': self.metadata,
            'profile': self.profile,
            'start_time': self.start_time,
            'time_base': self.time_base,
            'type': self.type,
        }

        if fraction:
            return _d
        else:
            for k in _d.keys():
                if isinstance(_d[k], Fraction):
                    _d[k] = float(_d[k])

            return _d

    def decode(self):
        pass

    def encode(self):
        pass

    @property
    def id(self) -> int:
        return self.av1_video_stream.id

    @property
    def index(self) -> int:
        return self.av1_video_stream.index

    @property
    def language(self) -> str:
        return self.av1_video_stream.language

    @property
    def average_rate(self) -> Fraction:
        return self.av1_video_stream.average_rate

    @property
    def base_rate(self) -> Fraction:
        return self.av1_video_stream.base_rate

    @property
    def duration(self) -> int:
        return self.av1_video_stream.duration

    @property
    def frames(self) -> int:
        return self.av1_video_stream.frames

    @property
    def guessed_rate(self) -> Fraction:
        return self.av1_video_stream.guessed_rate

    @property
    def profile(self) -> str:
        return self.av1_video_stream.profile

    @property
    def start_time(self) -> int:
        return self.av1_video_stream.start_time

    @property
    def time_base(self) -> Fraction:
        return self.av1_video_stream.time_base

    @property
    def type(self) -> str:
        return self.av1_video_stream.type

    @property
    def metadata(self) -> Dict[str, str]:
        return self.av1_video_stream.metadata
