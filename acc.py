import datetime
import os
import re
import sqlite3
import win32crypt


class AccountData(object):

    class NotFoundLoginDataException(Exception):
        pass

    def __init__(self):
        LOGIN_DATA_PATH = os.getenv("TMP").strip("Temp") + r"Google\Chrome\User Data\Default\Login Data"
        if not os.path.exists(LOGIN_DATA_PATH):
            raise AccountData.NotFoundLoginDataException("Not found 'Login Data'\n"
                                                                "Add path 'TMP' or 'Temp' to "
                                                                "'%USERPROFILE%\AppData\Local\Temp'")

        conn = sqlite3.connect(LOGIN_DATA_PATH)

        self.columns = {
            "origin_url": 0,
            "action_url": 1,
            "username_element": 2,
            "username_value": 3,
            "password_element": 4,
            "password_value": 5,
            "submit_element": 6,
            "signon_realm": 7,
            "preferred": 8,
            "date_created": 9,
            "blacklisted_by_user": 10,
            "scheme": 11,
            "password_type": 12,
            "times_used": 13,
            "form_data": 14,
            "date_synced": 15,
            "display_name": 16,
            "icon_url": 17,
            "federation_url": 18,
            "skip_zero_click": 19,
            "generation_upload_status": 20,
            "possible_username_pairs": 21,
            "id": 22,
            "date_last_used": 23
        }
        c = conn.cursor()
        c.execute("select * from logins")
        self.data_table = c.fetchall()
        conn.close()

    def get_all_information(self):
        time_string, url, username, password = [], [], [], []
        for raw in self.data_table:
            start_time = datetime.datetime(1601, 1, 1)
            time_diff = raw[self.columns["date_created"]] / 1000000
            time_string.append(re.sub(r".[0-9]{6}", "",
                                      str(start_time + datetime.timedelta(seconds=time_diff))))
            url.append(raw[self.columns["origin_url"]])
            username.append(raw[self.columns["username_value"]])
            password.append(win32crypt.CryptUnprotectData(
                bytes(raw[self.columns["password_value"]]), None, None, None, 0
            )[1].decode('utf8'))
        return time_string, url, username, password

    def show_all_information(self, password_visible: bool = True):
        time_string, url, username, password = self.get_all_information()
        for i in range(len(time_string)):
            time_string[i] = "* " + time_string[i] + " *"
            boundary = "".ljust(len(time_string[i]), "*")
            print(boundary)
            print(time_string[i])
            print(boundary)
            print("url:     ", url[i])
            print("username:", username[i])
            if password_visible:
                print("password:", password[i])
            print()

    def exist_columns(self):
        for k in self.columns.keys(): print(k)

    def get_select_columns(self, col):
        c = []
        print(f"-----{col}-----")
        for raw in self.data_table:
            c.append(raw[self.columns[col]])
            print(f"{raw[self.columns[col]]}")
        print()
        return c