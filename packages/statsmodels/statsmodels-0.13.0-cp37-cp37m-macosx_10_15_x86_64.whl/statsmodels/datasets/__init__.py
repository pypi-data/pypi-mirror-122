"""
Datasets module
"""
from statsmodels.tools._testing import PytestTester

from . import (
    anes96,
    cancer,
    ccard,
    china_smoking,
    co2,
    committee,
    copper,
    cpunish,
    danish_data,
    elnino,
    engel,
    fair,
    fertility,
    grunfeld,
    heart,
    interest_inflation,
    longley,
    macrodata,
    modechoice,
    nile,
    randhie,
    scotland,
    spector,
    stackloss,
    star98,
    statecrime,
    strikes,
    sunspots,
)
from .utils import (
    check_internet,
    clear_data_home,
    get_data_home,
    get_rdataset,
    webuse,
)

__all__ = [
    "anes96",
    "cancer",
    "committee",
    "ccard",
    "copper",
    "cpunish",
    "elnino",
    "engel",
    "grunfeld",
    "interest_inflation",
    "longley",
    "macrodata",
    "modechoice",
    "nile",
    "randhie",
    "scotland",
    "spector",
    "stackloss",
    "star98",
    "strikes",
    "sunspots",
    "fair",
    "heart",
    "statecrime",
    "co2",
    "fertility",
    "china_smoking",
    "get_rdataset",
    "get_data_home",
    "clear_data_home",
    "webuse",
    "check_internet",
    "test",
    "danish_data",
]

test = PytestTester()
