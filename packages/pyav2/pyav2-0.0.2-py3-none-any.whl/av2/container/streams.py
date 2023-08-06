from typing import Tuple, List, Any
from av2.video.stream import VideoStream
from av2.audio.stream import AudioStream
from av.container.input import InputContainer as AvInputContainer


class StreamContainer(object):

    """

    A tuple-like container of :class:`Stream`.

    ::

        # There are a few ways to pulling out streams.
        first = container.streams[0]
        video = container.streams.video[0]
        audio = container.streams.get(audio=(0, 1))


    """

    _streams: List

    subtitles: Tuple[str]
    data: Tuple[Any]
    other: Tuple[Any]

    audio: Tuple[AudioStream]
    video: Tuple[VideoStream]

    def __init__(self, container: AvInputContainer) -> None:
        self.av1_input_container = container

    @property
    def video(self) -> Tuple[VideoStream]:
        return tuple([
            VideoStream(v)
            for v in self.av1_input_container.streams.video
        ])
