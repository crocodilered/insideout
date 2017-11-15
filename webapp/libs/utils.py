from datetime import timedelta


__all__ = ['DateUtils']


class DateUtils:
    @staticmethod
    def get_monday_sunday(dt):
        monday = dt if dt.isoweekday() == 1 else dt - timedelta(days=(dt.isoweekday() - 1))
        sunday = monday + timedelta(days=6)
        return monday, sunday

    @staticmethod
    def get_prev_monday_sunday(dt):
        monday, sunday = DateUtils.get_monday_sunday(dt)
        return monday - timedelta(days=7), sunday - timedelta(days=7)

    @staticmethod
    def get_next_monday_sunday(dt):
        monday, sunday = DateUtils.get_monday_sunday(dt)
        return monday + timedelta(days=7), sunday + timedelta(days=7)

    @staticmethod
    def format_dm(dt):
        months = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня", 7: "июля", 8: "августа",
                  9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}
        return "%s %s" % (dt.day, months[dt.month])
