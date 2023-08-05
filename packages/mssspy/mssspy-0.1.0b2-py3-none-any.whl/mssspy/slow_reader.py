"""Implements a slow but simple pure-Python reader."""


import os
from typing import cast, IO, List, Union

import numpy as np  # type: ignore

from .base_readers import FileReader
from .exceptions import ParseError
from .sample import Sample


def encode_str(s: Union[str, bytes]):
    """
    If passed `str`, encodes it as latin-1, ignoring non-ASCII characters.
    """

    if isinstance(s, str):
        return s.encode('latin-1')

    return s


class SlowReader(FileReader):
    """
    A relatively slow but simple and correct pure-Python reader for ms/msms
    files.

    It can be passed the path to a file, or an already open file-like object.
    If passed a file-like object it does not close it when used as a context
    manager, otherwise it does.
    """

    name = 'slow'
    priority = 90

    # TODO: For building an index without parsing the samples, it would be
    # faster to refactor this into an iterator that just finds each //
    # separator and adds their offsets to the index.  Then, for actually
    # reading the samples, call _parse_sample while iterating.
    #
    # Otherwise, currently there is no way to simply build the index without
    # calling read_sample() repeatedly, which does unnecessary seeks/tells,
    # etc.
    def read_sample(self, idx: int = 0, index_only: bool = False) -> Sample:
        offset = 0
        cur_idx = 0

        if self.index:
            if idx < len(self.index):
                offset = self.index[idx]
                cur_idx = idx
            elif idx >= len(self.index):
                if self.index.complete:
                    # We already know there are no more samples to parse in
                    # this file
                    raise IndexError(idx)

                # Start from the last known sample's offset
                offset = self.index[-1]
                cur_idx = len(self.index) - 1

        sample = None

        with self:
            fd = cast(IO, self._fd)
            # When self.__enter__ is invoked self._fd will be non-None but
            # the type checker isn't clever enough to figure that out.
            fd.seek(offset, os.SEEK_SET)

            # Usually infinite loop, but we can set it to a small int to stop
            # reading after a specific number of lines
            remaining_lines = float('inf')

            while remaining_lines:
                offset = fd.tell()
                line = encode_str(fd.readline())

                # The rest of this code works on bytes

                remaining_lines -= 1

                if not line:
                    # EOF reached
                    if self.index is not None:
                        self.index.complete = True
                    if cur_idx <= idx:
                        raise IndexError(idx)
                    break
                elif line.startswith(b'//'):
                    if self.index is not None and len(self.index) - 1 < cur_idx:
                        self.index.append(offset)

                    if cur_idx == idx:
                        if not index_only:
                            sample = self._parse_sample(idx)

                        if self.index is not None and len(self.index) - 1 == cur_idx:
                            # Even if we successfully found the next sample,
                            # stay in the loop for a couple more lines, since
                            # the next sample should begin soon, or the end of
                            # the file will be reached
                            remaining_lines = min(remaining_lines, 2)
                        else:
                            remaining_lines = 0
                    elif cur_idx > idx:
                        remaining_lines = 0

                    cur_idx += 1

        if sample is None:
            raise IndexError(idx)

        return sample

    def _parse_sample(self, idx: int) -> Sample:
        segsites = None
        positions = None
        snps: List[List[int]] = []

        def validate_segsites():
            if (segsites is not None and positions is not None and
                    len(positions) != segsites):
                raise ParseError(
                    f'number of positions ({len(positions)}) does not '
                    f'equal segsites ({segsites}) in sample {idx}')

        # This method should only be called from within read_sample and within
        # use of this class as a context manager
        assert self._fd is not None

        while True:
            line = encode_str(self._fd.readline().rstrip())

            if not line:
                # A blank line should indicate the end of the sample; if there
                # are some badly formatted files out there containing spurious
                # blank lines, we could add extra logic to handle that
                break
            elif not snps:
                if segsites is None and line.startswith(b'segsites:'):
                    segsites = int(line.split(maxsplit=1)[1])
                    validate_segsites()
                elif positions is None and line.startswith(b'positions:'):
                    positions = np.fromstring(line.split(maxsplit=1)[1], sep=' ')
                    validate_segsites()
                elif line and line[:1] in (b'0', b'1'):
                    if segsites is None:
                        raise ParseError(f'missing segsites from sample {idx}')
                    elif positions is None:
                        raise ParseError(f'missing positions from sample {idx}')

                    # Should maybe do further validation that the line is all 0's
                    # and 1's
                    snps.append([int(s) - ord(b'0') for s in line])
            elif line and line[:1] in (b'0', b'1'):
                snps.append([int(s) - ord(b'0') for s in line])
            elif snps:
                # The first line that does not look like a haplotype line
                # should be ignored
                break
            else:
                # All unrecognized lines are ignored for now
                pass

        if positions is None:
            # Some samples, if nsamps is low, can have segsites: 0 and no
            # positions section
            positions = np.array([], dtype=float)

        return Sample(np.array(snps, dtype=np.uint8), positions)
