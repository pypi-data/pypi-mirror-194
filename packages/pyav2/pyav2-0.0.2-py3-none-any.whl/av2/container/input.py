from typing import Dict, Any
from av.container.input import InputContainer as AvInputContainer
from av2.container.core import Container
from av2.container.streams import StreamContainer
from av2.container.schemas import InputContainerMetadata
import av


class InputContainer(Container):
    auto_bsf: bool
    bit_rate: int
    bit_exact: bool
    duration: int
    # flags: str # TODO
    metadata: InputContainerMetadata
    streams: StreamContainer
    sort_dts: bool
    shortest: bool
    size: int
    start_time: int
    writeable: bool

    def __init__(self, *args, **kwargs) -> None:
        self.av1_input_container = av.open(*args, **kwargs)

    def dict(self, fraction: bool = False, only_container: bool = False) -> Dict[str, Any]:
        """
        fraction: Whether to keep the fraction, if True then Fraction, if False then float
        """
        _d = {
            'auto_bsf': self.auto_bsf,
            'bit_rate': self.bit_rate,
            'bit_exact': self.bit_exact,
            'duration': self.duration,
            # 'flags': self.flags,
            'metadata': self.metadata.dict(),
            'sort_dts': self.sort_dts,
            'shortest': self.shortest,
            'size': self.size,
            'start_time': self.start_time,
            'writeable': self.writeable
        }
        if only_container:
            return _d
        else:
            _f = {
                'container': _d,
                'steams': {
                    'video': [v.dict() for v in self.streams.video]
                }
            }
            return _f

    @property
    def metadata(self) -> InputContainerMetadata:
        _metadata: Dict[str, str] = self.av1_input_container.metadata
        return InputContainerMetadata(**_metadata)

    @property
    def streams(self) -> StreamContainer:
        _streams = self.av1_input_container.streams
        return StreamContainer(self.av1_input_container)

    @property
    def size(self) -> int:
        _size = self.av1_input_container.size
        return _size

    @property
    def writeable(self) -> bool:
        return self.av1_input_container.writeable

    @property
    def sort_dts(self) -> bool:
        return self.av1_input_container.sort_dts

    @property
    def shortest(self) -> bool:
        return self.av1_input_container.shortest

    # @property
    # def flags(self) -> str:
    #     return self.av1_input_container.flags

    @property
    def duration(self) -> int:
        return self.av1_input_container.duration

    @property
    def bit_rate(self) -> int:
        return self.av1_input_container.bit_rate

    @property
    def bit_exact(self) -> bool:
        return self.av1_input_container.bit_exact

    @property
    def auto_bsf(self) -> bool:
        return self.av1_input_container.auto_bsf

    @property
    def start_time(self) -> int:
        return self.av1_input_container.start_time
