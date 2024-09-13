from __future__ import annotations


from nlp.utils.sequences import combinations

from .base import Phrase


class DatePhrase(Phrase):
    """
    Connects words to make a date.
    A date component is complete with:
        - day, weekday, month, year
        - weekday, date
    eg:

        Thursday 20/10/2017
        June 16th
        Mon, Sep 18
        26th June
        Fri Sep 8th
    """
    connections = [
        *combinations(
            [
                "day", "year",
                "month", "weekday",
            ],
            min_n=1,
        ),
        *combinations(
            [
                "day", "year",
                "month_number", "weekday",
            ],
            min_n=1,
        ),
        *combinations(
            [
                "weekday", "date",
            ],
            min_n=1,
        )
    ]


class TimePhrase(Phrase):

    """
    Connects words to make time.
    A time component is complete with:
        - time, period, timezone
    eg:


    """

    connections = [
        ["time"],
        ["time", "period", "timezone"],
        ["time", "period"],
        ["time", "timezone"],
    ]


class DurationPhrase(Phrase):

    connections = [
        ["number", "timeunit"]
    ]
