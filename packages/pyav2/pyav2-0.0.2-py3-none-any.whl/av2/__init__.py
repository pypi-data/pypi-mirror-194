from av2.container.input import InputContainer
from av2.container.output import OutputContainer
from typing import overload, Literal, Union


__version__ = '0.0.2'
VERSION = __version__


READ_MODE = Literal['r']
WRITE_MODE = Literal['w']


@overload
def open(file: str, mode: READ_MODE = READ_MODE, format=None, options=None,
         container_options=None, stream_options=None,
         metadata_encoding='utf-8', metadata_errors='strict',
         buffer_size=32768, timeout=None, io_open=None) -> InputContainer:
    pass


@overload
def open(file: str, mode: WRITE_MODE = READ_MODE, format=None, options=None,
         container_options=None, stream_options=None,
         metadata_encoding='utf-8', metadata_errors='strict',
         buffer_size=32768, timeout=None, io_open=None) -> OutputContainer:
    pass


def open(file: str, mode='r', format=None, options=None,
         container_options=None, stream_options=None,
         metadata_encoding='utf-8', metadata_errors='strict',
         buffer_size=32768, timeout=None, io_open=None) -> Union[InputContainer, OutputContainer]:
    """open(file, mode='r', **kwargs)

    Main entrypoint to opening files/streams.

    :param str file: The file to open, which can be either a string or a file-like object.
    :param str mode: ``"r"`` for reading and ``"w"`` for writing.
    :param str format: Specific format to use. Defaults to autodect.
    :param dict options: Options to pass to the container and all streams.
    :param dict container_options: Options to pass to the container.
    :param list stream_options: Options to pass to each stream.
    :param str metadata_encoding: Encoding to use when reading or writing file metadata.
        Defaults to ``"utf-8"``.
    :param str metadata_errors: Specifies how to handle encoding errors; behaves like
        ``str.encode`` parameter. Defaults to ``"strict"``.
    :param int buffer_size: Size of buffer for Python input/output operations in bytes.
        Honored only when ``file`` is a file-like object. Defaults to 32768 (32k).
    :param timeout: How many seconds to wait for data before giving up, as a float, or a
        :ref:`(open timeout, read timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param callable io_open: Custom I/O callable for opening files/streams.
        This option is intended for formats that need to open additional
        file-like objects to ``file`` using custom I/O.
        The callable signature is ``io_open(url: str, flags: int, options: dict)``, where
        ``url`` is the url to open, ``flags`` is a combination of AVIO_FLAG_* and
        ``options`` is a dictionary of additional options. The callable should return a
        file-like object.

    For devices (via ``libavdevice``), pass the name of the device to ``format``,
    e.g.::

        >>> # Open webcam on OS X.
        >>> av.open(format='avfoundation', file='0') # doctest: +SKIP

    For DASH and custom I/O using ``io_open``, add a protocol prefix to the ``file`` to
    prevent the DASH encoder defaulting to the file protocol and using temporary files.
    The custom I/O callable can be used to remove the protocol prefix to reveal the actual
    name for creating the file-like object. E.g.::

        >>> av.open("customprotocol://manifest.mpd", "w", io_open=custom_io) # doctest: +SKIP

    .. seealso:: :ref:`garbage_collection`

    More information on using input and output devices is available on the
    `FFmpeg website <https://www.ffmpeg.org/ffmpeg-devices.html>`_.
    """

    # if isinstance(timeout, tuple):
    #     open_timeout = timeout[0]
    #     read_timeout = timeout[1]
    # else:
    #     open_timeout = timeout
    #     read_timeout = timeout

    if mode.startswith('r'):
        return InputContainer(file, mode, format, options,
                              container_options, stream_options,
                              metadata_encoding, metadata_errors,
                              buffer_size, timeout, io_open
                              )
    if mode.startswith('w'):
        if stream_options:
            raise ValueError(
                "Provide stream options via Container.add_stream(..., options={}).")
        return OutputContainer(file, mode, format, options,
                               container_options, stream_options,
                               metadata_encoding, metadata_errors,
                               buffer_size, timeout, io_open
                               )

    # import av
    # return av.open(file, mode, format, options,
    #                container_options, stream_options,
    #                metadata_encoding, metadata_errors,
    #                buffer_size, timeout, io_open)
