#!/usr/bin/env python3
import fire
from .fund import fund, fundalert
from .roundcorner import rc
from .app import asyncbenchmark
from ..network import LunarCalendar
import codefast as cf


def wnl():
    """Lunar calendar"""
    LunarCalendar.display()


def download(url: str, filename: str = None):
    """Download file from url. Usage: sli download url filename"""
    import codefast as cf
    cf.net.download(url, filename)


def excel2csv(filename: str):
    """Convert excel file to csv file. Usage: sli excel2csv filename"""

    import os
    os.system('mkdir -p /tmp/excel/')
    cf.reader.Excel(filename).to_csv('/tmp/excel/')


def ccard(bin_: str = '537630'):
    """Generate credit card number. Usage: sli ccard bin"""
    from dofast.toolkits.credit_card_generator import create_cc_numbers
    cf.info([bin_, 16])
    for n in create_cc_numbers(bin_, ccnumber_length=16):
        print(n)


def main():
    fire.Fire({
        'fund': fund,
        'fundalert': fundalert,
        'rc': rc,
        'asyncbenchmark': asyncbenchmark,
        'wnl': wnl,
        'download': download,
        'excel2csv': excel2csv,
        'ccard': ccard,
    })
