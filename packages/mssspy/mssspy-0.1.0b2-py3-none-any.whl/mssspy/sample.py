from dataclasses import dataclass

import numpy as np  # type: ignore


@dataclass
class Sample:
    """
    Class representing data read from a single sample in an ms file.

    It consists of two arrays, ``snps`` which contain the hapoltype/SNP data
    as an array of shape ``(n, m)`` where ``n`` is the number of individuals
    in the array, and ``m`` is the number of SNPs.

    The other array is the array of ``positions`` of the SNPs as read from the
    sample.  The number of positions is equivalently `Sample.segsites`.
    """

    snps: np.ndarray
    positions: np.ndarray

    @property
    def segsites(self) -> int:
        """Number of polymorphic sites in the sample."""

        return len(self.positions)

    def __eq__(self, other):
        """
        Samples are equal if their haplotypes and positions arrays are equal.
        """

        if self is other:
            return True

        if isinstance(other, Sample):
            # Comparing positions first is faster for the negative case
            return ((self.positions == other.positions).all() and
                    (self.snps == other.snps).all())

        return NotImplemented
