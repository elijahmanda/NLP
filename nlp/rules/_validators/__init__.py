
def register():
    from . import number
    from . import datetime

    number.register()
    datetime.register()
