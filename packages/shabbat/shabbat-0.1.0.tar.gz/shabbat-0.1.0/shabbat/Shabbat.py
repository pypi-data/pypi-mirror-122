from datetime import datetime
import httpx


# geotags for israel city's
# 281184 ירושלים
# 294801 חיפה
# 293397 תל אביב
# באר שבע 295530

class Shabbat:

    def __init__(self, geotag=281184, shabbat_min=36):
        self.geotag = geotag
        self.shabbat_min = shabbat_min

    def get_sabbat(self):
        """
        :param shabbat_min: minute before shabbat.
        """
        times = httpx.get(f"https://www.hebcal.com/shabbat/?cfg=json&geonameid={self.geotag}&m={self.shabbat_min}").json()
        data = [i for i in eval(str(times))['items'] if i["category"] == "havdalah" or i["category"] == "candles"]
        return [data[0]['title'], data[-1]['title']]

    def get_in(self) -> str:
        return self.get_sabbat()[0][self.get_sabbat()[0].find(r":") + 2:]

    def get_out(self) -> str:
        return self.get_sabbat()[-1][self.get_sabbat()[-1].find(r":") + 2:]

    def exact_time(self, method):
        """
        :param method: the method to get the exact time of shabbat: "in" Shabbat entry, "out" end of shabbat.
        :return: tuple with the times.
        for example: if get_out() return 18:50 this func will return (18, 50).
        """
        if method == "in":
            hour_in, min_in = self.get_in().split(':')
            return int(hour_in), int(min_in)
        elif method == "out":
            hour_out, min_out = self.get_out().split(':')
            return int(hour_out), int(min_out)
        else:
            raise ValueError(f"{method} Isn't an available method. the available methods are 'in' and 'out'")

    def shabbat(self, m_in, hr_in, m_out, hr_out):
        """If Friday and shabbat came in returns True, if shabbat has not yet come out, returns True!"""
        day = datetime.today()
        now = datetime.now()
        if day.weekday() == 4:
            if now.hour > hr_in:
                if now.minute > m_in:
                    return True
        elif day.weekday() == 5:
            if now.hour < hr_out:
                if now.minute < m_out:
                    return True
        return False

    def is_shabbat(self):
        hour_in, min_in = self.exact_time("in")
        hour_out, min_out = self.exact_time("out")
        if self.shabbat(min_in, hour_in, min_out, hour_out):
            return True
        return False


