"""
Utility class for DNA sequence operations.
"""
from __future__ import annotations
from pyfaidx import Faidx, Fasta
import dna_utils.mapper as mapper
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pathlib import Path


class DNAUtils:
    @staticmethod
    def reverse(seq: str) -> str:
        """
        Method to reverse DNA sequence.

        Args:
            seq (str): DNA sequence string.

        Returns:
            str: Reversed DNA sequence string.
        """
        return str(seq).upper()[::-1]

    @staticmethod
    def complement(seq: str) -> str:
        """
        Method to compute complement of a DNA sequence.

        Args:
            seq (str): DNA sequence string to complement.

        Returns:
            str: Complement DNA sequence string.
        """
        trans_tab = str.maketrans("ATCG", "TAGC")
        return str(seq).upper().translate(trans_tab)

    @staticmethod
    def reverse_complement(seq: str) -> str:
        """
        Method to reverse complement DNA sequence.

        Args:
            seq (str): DNA sequence string.

        Returns:
            str: Reverse complement DNA sequence string.
        """
        return DNAUtils.reverse(DNAUtils.complement(seq))

    @staticmethod
    def get_reference_sequence(fasta: Path, chrom: str, start: int, end: int) -> str:
        """
        Method to retrieve a DNA sequence by genomic location from an indexed genome Fasta file.

        Args:
            fasta (Path): Fasta file
            chrom (str): chromosome name as define in chromosome source Fata file (ex: chr1).
            start (long): start location on chromosome.
            end (long): end location on chromosome.

        Return:
            DNA sequence for given coordinates.
        """
        with Fasta(fasta, split_char=".", duplicate_action="first", sequence_always_upper=True, rebuild=False) as fasta:
            return fasta.get_seq(chrom, start, end)

    @staticmethod
    def get_reference_chromosomes(fasta: Path) -> List[List[str, int]]:
        """
        List reference genome chromosome and chromosome length.

        Args:
            fasta (Path): Fasta file

        Return:
            List of chromosome with length: [['chr1', 249250621], ['chr2', 243199373],...]
        """
        with Faidx(fasta, rebuild=False) as indexed_fasta:
            return [[k, indexed_fasta.index[k].rlen] for k in indexed_fasta.index.keys()]

    @staticmethod
    def translate(seq: str, long_notation=False) -> str:
        """
        Convert DNA sequence in protein sequence.

        Args:
            seq (str): DNA sequence string to translate.
            long_notation (bool): Whether return aa long notation or not.

        Returns:
            str: Protein sequence string
        """

        aa_seq = ""
        for i in range(0, len(seq), 3):
            codon = seq[i: i + 3].upper()
            if len(codon) == 3:
                aa = mapper.nucl_to_small_aa.get(codon)
                if long_notation:
                    aa = DNAUtils.aa1to3(aa)
                aa_seq += aa
        return aa_seq

    @staticmethod
    def aa1to3(aa: str) -> str:
        """
        Convert small aa notation to long aa notation

        Args:
            aa (str): small aa notation (len 1)

        Returns:
            str: long aa notation (len 3)
        """
        if len(aa) != 1:
            raise ValueError("AA should be one character")
        return mapper.small_aa_to_long_aa.get(aa.upper())

    @staticmethod
    def aa3to1(aa: str):
        """
        Convert long aa notation to small aa notation

        Args:
            aa (str): long aa notation (len 3)

        Returns:
            str: small aa notation (len 1)
        """
        if len(aa) != 3:
            raise ValueError("AA should be 3 characters")
        return mapper.long_aa_to_small_aa.get(aa)

