"""Implements the slightly faster (but still pure-Python `FasterReader`)."""


import gzip
import io
import mmap
from typing import Any, Optional

import numpy as np  # type: ignore

from .base_readers import ReaderMatch, FileLikeSource
from .index import Index
from .sample import Sample
from .slow_reader import SlowReader


class FasterReader(SlowReader):
    """
    Similar to `SlowReader` (and still pure-Python) but a bit faster (about
    2x).

    This reader makes many concessions in terms of checking correctness of the
    input file, and assumes correctly-formatted ms files.  It may crash in
    unexpected ways when encountering a malformatted file, or a malformatted
    sample within an otherwise correct file.

    This reader should be preferred by default over `SlowReader`, though
    `SlowReader` can be fallen back on in order to better handle problems in
    poorly-formatted inupt files.
    """

    name = 'faster'
    priority = 100

    def __init__(self, data_source: FileLikeSource,
                 index: Optional[Index] = None) -> None:
        super().__init__(data_source, index)
        self._close_mmap = False

    @classmethod
    def match_data_source(cls, data_source: Any) -> ReaderMatch:
        if isinstance(data_source, io.IOBase):
            if hasattr(data_source, 'fileno'):
                try:
                    data_source.fileno()
                except io.UnsupportedOperation:
                    return False, 'fileno() not supported'
            else:
                return False, 'file objects must have a fileno() method'

        if isinstance(data_source, gzip.GzipFile):
            # TODO: Detect other compressed file types
            return False, 'gzip files not supported'

        # Try using SlowReader.match_data_source first since it will apply for
        # most other cases
        return super().match_data_source(data_source)

    # Replace the basic file object with an mmap, which is used exclusively by
    # this reader (it assumes self._fd is an mmap object)
    def _open(self) -> None:
        super()._open()
        # mypy is not clever enough to realize that self._fd cannot be None
        # after a call to super()._open()
        assert self._fd is not None

        # If not already an mmap
        if not isinstance(self._fd, mmap.mmap):
            self._orig_fd = self._fd
            self._fd = mmap.mmap(self._fd.fileno(), 0, flags=mmap.MAP_PRIVATE)
            self._close_mmap = True

    def _close(self) -> None:
        assert self._fd is not None

        if self._close_mmap:
            self._fd.close()
            self._fd = self._orig_fd
            del self._orig_fd
        super()._close()

    def _parse_sample(self, idx: int) -> Sample:
        assert isinstance(self._fd, mmap.mmap)

        positions = None
        snps = None

        # For the fast reader actually we ignore the segsites line entirely
        # since we can infer it from the positions list (I don't think there's
        # ever a time they won't be the same, based on the original ms.c
        # source)

        while True:
            start = self._fd.tell()
            line = self._fd.readline()

            if not line:
                break

            first_char = line[:1]

            if first_char == b'p':  # for positions:
                positions = np.fromstring(line[11:-1], sep=' ')
            elif first_char in (b'0', b'1'):
                # We can infer the number of positions from the length of the
                # line
                n_pos = len(line) - 1
                # In the haplotypes block; find the end of it by finding the
                # next double-newline or EOF
                end = self._fd.find(b'\n\n', start) + 1
                end = end if end > start else self._fd.size()
                # We can infer the number of haplotypes by the size of the
                # block
                n_hap = (end - start) // (n_pos + 1)
                shape = (n_hap, n_pos)
                snps = np.ndarray(shape, buffer=self._fd[start:end],
                                  strides=(n_pos + 1, 1),
                                  dtype=np.uint8) - ord(b'0')
                break
            elif first_char == b'\n':
                # We reached a blank line, so this should be the end of the
                # sample
                break

        if positions is None:
            # Some samples, if nsamps is low, can have segsites: 0 and no
            # positions section
            positions = np.array([], dtype=float)

        if snps is None:
            # Something else unrecognized or start of another sample
            snps = np.array([], dtype=np.uint8)

        return Sample(snps, positions)
