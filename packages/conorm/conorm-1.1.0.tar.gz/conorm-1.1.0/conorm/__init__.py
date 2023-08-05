"""Count matrix normalization in Python."""


name = "cmnorm"
__version__ = "1.1.0"
__author__ = "Georgy Meshcheryakov"

from .normalize import tmm, tmm_norm_factors, getmm, percentile, quartile,\
                       rpk, rpkm, cpm, total_count