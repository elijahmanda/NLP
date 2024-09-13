from .base import Sentence


class RangeSentence(Sentence):
    """
    Connects phrases starting with a 
    range word like `from` and ending in a
    range word like `to`, `until`
    from [time, date, event, datetime phrase] to/til/until 
    """
    connections = [
        ["from", "date_phrase", "to", "date_phrase"],
        ["from", "date_phrase", "to", "time_phrase"],
        ["from", "date_phrase", "to", "event_phrase"],
        ["from", "time_phrase", "to", "time_phrase"],
        ["from", "time_phrase", "to", "date_phrase"],
        ["from", "time_phrase", "to", "event_phrase"],
    ]
