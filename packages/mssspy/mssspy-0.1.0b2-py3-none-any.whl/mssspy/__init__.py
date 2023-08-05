"""mssspy -- A Python reader for ms/msms files"""


from types import TracebackType
from typing import Any, List, Optional, Tuple, Type, Union, cast
from warnings import warn

from .base_readers import FileReader, MSReader
from .exceptions import MssspyWarning
from .index import Index
from .sample import Sample
from .utils import LRUDict

# Import and register the built-in readers
from .faster_reader import FasterReader  # noqa: E402, F401
from .slow_reader import SlowReader  # noqa: E402


# Typing aliases
ReaderArg = Union[str, Type[MSReader]]


class MSFile:
    """
    High-level interface for ms files.

    When a file is opened, individual samples in the file can be accessed by
    indexing the `MSFile` instance.

    Actual reading of the file is delegated to the chosen reader.

    This class also implements caching of "indices" for files in the most
    common cases (e.g. files on disk), which allow rapid access to individual
    samples within a file without having to fully re-parse them.

    Currently the "faster" reader is used by default, though it falls back on
    the "slow" reader if the input is a type not supported by "faster" reader
    (e.g. an `io.StringIO` object or other non-mmap-able file), if parsing
    the file otherwise fails with the "faster" reader, which is less
    fault-tolerant, or if the reader is otherwise explicitly specified.
    """

    _index_cache: LRUDict = LRUDict(maxsize=None)
    """Global index cache."""

    reader: MSReader
    fallback_reader: Optional[MSReader]

    def __init__(self, path_or_obj: Any,
                 reader: Optional[ReaderArg] = None,
                 disable_index_cache: bool = False,
                 fallback_reader: Optional[ReaderArg] = None) -> None:
        self.path_or_obj = path_or_obj

        if reader is None:
            reader = self.guess_reader(path_or_obj)
        elif isinstance(reader, str):
            reader = MSReader.get(reader)

        if isinstance(fallback_reader, str):
            fallback_reader = MSReader.get(fallback_reader)

        # Reader should now be an MSReader subclass
        reader = cast(Type[MSReader], reader)
        fallback_reader = cast(Optional[Type[MSReader]], fallback_reader)

        if not disable_index_cache:
            index = self._cached_index(reader, path_or_obj)
        else:
            index = None

        self.reader = reader(path_or_obj, index=index)

        # If using a FileReader other than SlowReader, construct a SlowReader
        # as the default fallback
        if (fallback_reader is None and issubclass(reader, FileReader) and
                reader is not SlowReader):
            fallback_reader = SlowReader

        if fallback_reader is not None:
            self.fallback_reader = fallback_reader(path_or_obj, index=index)
        else:
            self.fallback_reader = None

    def __enter__(self) -> 'MSFile':
        # Delegate to the underlying reader's __enter__
        self.reader.__enter__()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        # Delegate to the underlying reader's __exit__
        self.reader.__exit__(exc_type, exc_val, exc_tb)

    def __getitem__(self, idx: int) -> Sample:
        try:
            return self.reader.read_sample(idx)
        except IndexError:
            raise
        except Exception as exc:
            if self.fallback_reader is not None:
                warn(
                    f'{self.reader.name} reader failed on sample {idx} of '
                    f'{self.path_or_obj} ({exc}); '
                    f'trying {self.fallback_reader.name} reader as a fallback',
                    MssspyWarning)
                return self.fallback_reader.read_sample(idx)
            else:
                raise

    @classmethod
    def resize_index_cache(cls, size: Optional[int]) -> None:
        """
        Set the maximum size (in number of files) of the cache of file indices.

        By default the size of the cache is unbounded.  Setting a smaller size
        will cause the cached indices of less recently used files to be
        dropped.
        """

        cls._index_cache.maxsize = size

    @classmethod
    def guess_reader(cls, path_or_obj: Any) -> Type[MSReader]:
        """
        Try to guess the most appropriate reader to use based on the input
        type.
        """

        tried: List[Tuple[Type[MSReader], str]] = []

        for reader_cls in sorted(MSReader.registry.values(),
                                 key=lambda cls: cls.priority, reverse=True):
            try:
                matches = reader_cls.match_data_source(path_or_obj)
                reason = 'not supported'
                if isinstance(matches, tuple) and len(matches) == 2:
                    matches, reason = matches

                if matches:
                    return reader_cls
                else:
                    tried.append((reader_cls, reason))
            except Exception as exc:
                tried.append((reader_cls, str(exc)))
        else:
            tried_msg = '\n'.join(f'* {c.__name__}: {r}' for c, r in tried)

            raise ValueError(
                f'reading from {path_or_obj} failed; tried:\n{tried_msg}')

    @classmethod
    def _cached_index(cls, reader: Type[MSReader],
                      path_or_obj: Any) -> Optional[Index]:
        try:
            cache_key = reader.cache_key(path_or_obj)
        except NotImplementedError:
            cache_key = None

        if cache_key is not None:
            try:
                index = cls._index_cache[cache_key]
            except KeyError:
                # No index cache available for this file
                index = Index()
                cls._index_cache[cache_key] = index
        else:
            index = None

        return index
