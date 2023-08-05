import inspect
import io
import os
import mmap
from abc import ABCMeta, abstractmethod
from pathlib import Path
from types import TracebackType
from typing import (cast, Any, AnyStr, Dict, Hashable, IO, Optional, Tuple,
                    Type, Union)
from warnings import warn

from .exceptions import MssspyWarning
from .index import Index
from .sample import Sample


ReaderMatch = Union[bool, Tuple[bool, str]]


class MSReader(metaclass=ABCMeta):
    """
    Base class for lower-level ``ms`` file readers.

    This can have multiple implementations with different advantages or
    optimizations depending on your needs.  This also allows extending `mssspy`
    with custom readers.
    """

    registry: Dict[str, Type['MSReader']] = {}
    name: str
    priority = 0
    """
    Priority order in which to try a reader.  Setting a high priority on a
    subclass can give greater priority to that reader when `MSFile` guesses
    which reader to use.
    """

    def __init__(self, data_source: Any,
                 index: Optional[Union[Index, bool]] = None) -> None:
        """
        Initialize the reader with a data source which may be any arbitrary
        object, though typically it will be an open file-like object.

        Typically this will be a file-like object or something similar.
        """

        self.data_source = data_source

        if index in (None, True):
            index = Index()
        elif index is False:
            index = None

        self.index = cast(Optional[Index], index)

    def __init_subclass__(cls: Type['MSReader']) -> None:
        """Add this reader to the registry of available readers."""

        try:
            cls.name
        except AttributeError:
            # This is necessary since "abstract class attributes" are not
            # really supported by the abc module or by mypy
            if not inspect.isabstract(cls):
                raise RuntimeError(
                    'concrete implementations of MSReader require a name '
                    'attribute')
        else:
            if cls.name in cls.registry:
                warn(f'an MSReader named {cls.name} already exists in '
                     f'{cls.registry[cls.name].__module__} and will be '
                     f'replaced by {cls.__module__}.{cls.__qualname__}',
                     MssspyWarning)

            cls.registry[cls.name] = cls

    def __enter__(self) -> 'MSReader':
        """
        Dummy ``__enter__`` method so the reader can be used as a context
        manager.  Implement this and/or ``__exit__`` to manage resources
        (e.g. when the ``data_source`` is a file to be opened/closed).

        It should return ``self``.
        """

        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        """
        Dummy ``__exit__`` method so the reader can be used as a context
        manager.  Implement this and or ``__enter__`` to manage resources
        (e.g. when the ``data_source`` is a file to be opened/closed).
        """

    @abstractmethod
    def read_sample(self, idx: int = 0, index_only: bool = False) -> Sample:
        """
        Read the N-th sample in the file.

        By default the first (0th) sample is read, in the case of single-sample
        files.
        """

    @classmethod
    def match_data_source(cls, data_source: Any) -> ReaderMatch:
        """
        Return `True` if the given ``data_source`` object can be read by this
        reader.

        Otherwise, if it returns `False` or raises an exception, the object
        cannot be read.  In the case of `False`, an optional reason string can
        be given.

        The high-level interface will try known readers until it finds one that
        matches.
        """

        return False

    @classmethod
    def cache_key(cls, data_source: Any) -> Hashable:
        """
        For a given instance of the ``data_source`` accepted by this reader,
        return a hashable key used to cache the data source's index.

        For example, given a filename, this might return the pair ``(filename,
        mtime)`` for the file.

        If it cannot generate a cache key for the given ``data_source``, this
        should raise `NotImplementedError`, and the data source's index cannot
        be cached.
        """

        raise NotImplementedError(
            f'the data source {data_source} does not have a cacheable index')

    @classmethod
    def get(cls, name: str) -> Type['MSReader']:
        """Get an `MSReader` subclass by name."""

        try:
            return cls.registry[name]
        except KeyError:
            raise ValueError(
                f'unknown reader: {name}; available readers are: '
                f'{list(cls.registry)}')


FileLikeSource = Union[str, Path, IO[AnyStr], io.IOBase, mmap.mmap]


class FileReader(MSReader):
    """
    Base class for readers that read from a filesystem path or file-like
    object.

    This base class handles details such as opening/closing files, as well as
    generating the cache key.  Index caching is currently only possible for
    files with filesystem paths.

    The details of actually reading and parsing the file are left to individual
    implementations.
    """

    def __init__(self, data_source: FileLikeSource,
                 index: Optional[Index] = None) -> None:
        super().__init__(data_source, index)
        self._fd: Optional[Union[IO, mmap.mmap]] = None
        self._closefd = False
        self._opencount = 0

        if self.index is not None and isinstance(data_source, (str, Path)):
            self.index.path = str(data_source)

    def __enter__(self) -> 'FileReader':
        if self._opencount == 0:
            self._open()

        # Allows enter/exit to be re-entrant
        self._opencount += 1
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self._opencount -= 1
        if self._opencount == 0:
            self._close()

    @classmethod
    def match_data_source(cls, data_source: Any) -> ReaderMatch:
        # By default all file paths are supported, and strings are assumed to
        # be file paths (it doesn't matter if the file does not exist; that
        # will result in a FileNotFoundError later)
        if isinstance(data_source, (str, Path)):
            return True

        if not isinstance(data_source, io.IOBase):
            return False
        elif not data_source.seekable():
            return False, 'non-seekable files are not supported yet'

        return True

    @classmethod
    def cache_key(cls, data_source: Union[str, Path, IO[AnyStr]]) -> Tuple[str, float]:
        if isinstance(data_source, io.FileIO):
            # typing: here data_source.name could also be an int, but we use
            # the cast to ignore that case, do an explicit isinstance check
            # below
            name = cast(Union[str, Path], data_source.name)
        else:
            name = cast(Union[str, Path], data_source)

        if isinstance(name, (str, Path)):
            mtime = os.stat(name).st_mtime
            return (str(name), mtime)

        return super().cache_key(data_source)

    def _open(self) -> None:
        if isinstance(self.data_source, (str, Path)):
            self._fd = open(self.data_source, 'rb')
            self._closefd = True
        else:
            self._fd = self.data_source

    def _close(self) -> None:
        if self._closefd and self._fd is not None:
            self._fd.close()
