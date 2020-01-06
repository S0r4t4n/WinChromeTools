import datetime
import os
import re
import sqlite3


class HistoryData(object):
    class NotFoundHistoryException(Exception):
        pass

    def __init__(self):
        HISTORY_PATH = os.getenv("TMP").strip("Temp") + r"Google\Chrome\User Data\Default\History"
        if not os.path.exists(HISTORY_PATH):
            raise HistoryData.NotFoundHistoryException("Not found 'History'\n"
                                                              "Add path 'TMP' or 'Temp' to "
                                                              "'%USERPROFILE%\AppData\Local\Temp'")
        conn = sqlite3.connect(HISTORY_PATH)

        c = conn.cursor()
        c.execute("select * from urls")
        self.data_table = c.fetchall()
        conn.close()

    def get_all_data(self):
        time_string, url, title, visit_count = [], [], [], []
        for raw in self.data_table:
            start_time = datetime.datetime(1601, 1, 1)
            time_diff = raw[5] / 1000000
            time_string.append(re.sub(r".[0-9]{6}", "",
                                      str(start_time + datetime.timedelta(seconds=time_diff))))
            url.append(raw[1])
            title.append(raw[2])
            visit_count.append(str(raw[3]))
        return time_string, url, title, visit_count

    def show_all_data(self):
        time_string, url, title, visit_count = self.get_all_data()
        for i in range(len(time_string)):
            time_string[i] = "* " + time_string[i] + " *"
            boundary = "".ljust(len(time_string[i]), "*")
            print(boundary)
            print(time_string[i])
            print(boundary)
            print("title        : "+title[i])
            print("url          : "+url[i])
            print("visit count  : "+visit_count[i])
            print()