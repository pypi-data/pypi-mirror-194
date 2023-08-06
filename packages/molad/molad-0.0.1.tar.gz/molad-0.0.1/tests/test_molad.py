from molad.molad import MoladHelper
from molad.molad import MoladDetails
from molad.molad import Molad
from molad.molad import RoshChodesh
import datetime
import pytest

molads = [
    (
        'Regular Year',
        datetime.datetime(2023, 2, 15),
        MoladDetails(
            molad=Molad(
                friendly="Monday, 12:40 pm and 11 chalakim",
                day="Monday",
                hours=12,
                minutes=40,
                chalakim=11,
                am_or_pm="pm"
            ),
            is_shabbos_mevorchim=False,
            rosh_chodesh=RoshChodesh(
                month="Adar",
                days=["Tuesday", "Wednesday"],
                text="Tuesday & Wednesday",
            )
        )
    ),
    (
        'Leap Year Before Adar',
        datetime.datetime(2023, 11, 11),
        MoladDetails(
            molad=Molad(
                friendly="Monday, 7:17 am and 2 chalakim",
                day="Monday",
                hours=7,
                minutes=17,
                chalakim=2,
                am_or_pm="am"
            ),
            is_shabbos_mevorchim=True,
            rosh_chodesh=RoshChodesh(
                month="Kislev",
                days=["Tuesday"],
                text="Tuesday",
            )
        )
    ),
    (
        'Leap Year After Adar',
        datetime.datetime(2024, 5, 6),
        MoladDetails(
            molad=Molad(
                friendly="Wednesday, 11:41 am and 8 chalakim",
                day="Wednesday",
                hours=11,
                minutes=41,
                chalakim=8,
                am_or_pm="am"
            ),
            is_shabbos_mevorchim=False,
            rosh_chodesh=RoshChodesh(
                month="Iyyar",
                days=["Wednesday", "Thursday"],
                text="Wednesday & Thursday",
            )
        )
    ),
    (
        'Far Past Year',
        datetime.datetime(1823, 3, 7),
        MoladDetails(
            molad=Molad(
                friendly="Wednesday, 8:51 am and 4 chalakim",
                day="Wednesday",
                hours=8,
                minutes=51,
                chalakim=4,
                am_or_pm="am"
            ),
            is_shabbos_mevorchim=False,
            rosh_chodesh=RoshChodesh(
                month="Nisan",
                days=["Thursday"],
                text="Thursday",
            )
        )
    ),
    (
        'Far Future Year',
        datetime.datetime(2122, 12, 26),
        MoladDetails(
            molad=Molad(
                friendly="Monday, 7:29 pm and 4 chalakim",
                day="Monday",
                hours=7,
                minutes=29,
                chalakim=4,
                am_or_pm="pm"
            ),
            is_shabbos_mevorchim=True,
            rosh_chodesh=RoshChodesh(
                month="Tevet",
                days=["Tuesday", "Wednesday"],
                text="Tuesday & Wednesday",
            )
        )
    )
]

@pytest.mark.parametrize('name,date,expected', molads)
def test_molad(name, date, expected):
    calculated = get_molad(date)

    assert calculated.molad.friendly == expected.molad.friendly
    assert calculated.molad.day == expected.molad.day
    assert calculated.molad.hours == expected.molad.hours
    assert calculated.molad.minutes == expected.molad.minutes
    assert calculated.molad.chalakim == expected.molad.chalakim
    assert calculated.molad.am_or_pm == expected.molad.am_or_pm
    assert calculated.is_shabbos_mevorchim == expected.is_shabbos_mevorchim
    assert calculated.rosh_chodesh.month == expected.rosh_chodesh.month
    assert calculated.rosh_chodesh.days == expected.rosh_chodesh.days
    assert calculated.rosh_chodesh.text == expected.rosh_chodesh.text

class Config:
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.time_zone = 'Asia/Jerusalem'

def get_molad(d) -> MoladDetails:
    config = Config()
    mh = MoladHelper(config)   
    return mh.get_molad(d)
