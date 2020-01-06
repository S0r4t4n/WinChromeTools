import os
import re
import sqlite3


def round_str(size):
    return str(round(size, 1))


def file_size_convert(byte_size):
    if byte_size < 1024:
        return str(byte_size) + ' Bytes'
    elif byte_size < 1024 ** 2:
        return round_str(byte_size / 1024.0) + ' KBytes'
    elif byte_size < 1024 ** 3:
        return round_str(byte_size / (1024.0 ** 2)) + ' MBytes'
    elif byte_size < 1024 ** 4:
        return round_str(byte_size / (1024.0 ** 3)) + ' GBytes'
    elif byte_size < 1024 ** 5:
        return round_str(byte_size / (1024.0 ** 4)) + ' TBytes'
    else:
        return str(byte_size) + ' Bytes'


class DownloadsData(object):
    class NotFoundHistoryException(Exception):
        pass

    def __init__(self):
        HISTORY_PATH = os.getenv("TMP").strip("Temp") + r"Google\Chrome\User Data\Default\History"
        if not os.path.exists(HISTORY_PATH):
            raise DownloadsData.NotFoundHistoryException("Not found 'History'\n"
                                                                "Add path 'TMP' or 'Temp' to "
                                                                "'%USERPROFILE%\AppData\Local\Temp'")
        conn = sqlite3.connect(HISTORY_PATH)

        c = conn.cursor()
        c.execute("select * from downloads")
        self.data_table = c.fetchall()
        conn.close()

    def get_all_data(self):
        file_name, file_size, url, exist = [], [], [], []
        for raw in self.data_table:
            file_name.append(re.search(r"([^\\]+?)?$", raw[2]).group())
            file_size.append(file_size_convert(int(raw[5])))
            url.append(raw[17])
            if os.path.exists(raw[2]):
                exist.append(True)
            else:
                exist.append(False)
        return file_name, file_size, url, exist

    def show_all_data(self):
        file_name, file_size, url, exist = self.get_all_data()
        for i in range(len(file_name)):
            fn = "* " + file_name[i] + " *"
            boundary = "".ljust(len(fn), "*")
            print(boundary)
            print(fn)
            print(boundary)
            print("file size : "+file_size[i])
            print("url       : "+url[i])
            if exist[i]:
                print("exist     : True")
            else:
                print("exist     : False")
            print()