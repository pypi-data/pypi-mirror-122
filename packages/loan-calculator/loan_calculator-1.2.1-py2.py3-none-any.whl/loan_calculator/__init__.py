# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2019, Mateus Yano
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Loan Calculator"""

from loan_calculator.loan import Loan
from loan_calculator.utils import display_summary
from loan_calculator.grossup.iof import IofGrossup
from loan_calculator.projection import Projection
from loan_calculator.schedule.base import AmortizationScheduleType
from loan_calculator.grossup.base import GrossupType
from loan_calculator.interest_rate import (
    convert_to_daily_interest_rate, InterestRateType, YearSizeType
)

__all__ = [
    'Loan',
    'IofGrossup',
    'Projection',
    'AmortizationScheduleType',
    'GrossupType',
    'convert_to_daily_interest_rate',
    'InterestRateType',
    'display_summary',
    'YearSizeType',
]

__author__ = """Mateus Yano"""
__email__ = 'yano.mateus@gmail.com'
__version__ = '1.2.1'
