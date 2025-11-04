import sqlite3
from sleep import  Sleep

class Database:
    def __init__(self, path: str = "sleep_tracker.db"):
        self.path = path
        self.conn = None


    def connect(self) -> bool:
        try:
            self.conn = sqlite3.connect(self.path)
            return True
        except sqlite3.OperationalError:
            print("Ошибка соединения")
            return False

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def load_table(self) -> list:
        sql = "SELECT * FROM sleep_records"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        return records

    def get_record(self, id : int) -> list:
        cursor = self.conn.cursor()
        sql = f"SELECT * FROM sleep_records WHERE id = {id}"
        cursor.execute(sql)
        record = cursor.fetchone()
        return record

    def add_record(self, record : Sleep) -> None:
        cursor = self.conn.cursor()
        sql = "INSERT INTO sleep_records (date, sleep_duration, sleep_quality) VALUES (?, ?, ?)"
        cursor.execute(sql, (str(record.date), record.duration, record.quality))
        self.conn.commit()
        return

    def remove_last_record(self) -> None:
        cursor = self.conn.cursor()
        index = len(self.load_table())
        sql = f"DELETE FROM sleep_records WHERE id = {index}"
        sql2 = f"UPDATE sqlite_sequence SET seq = {index-1} WHERE name='sleep_records'"
        cursor.execute(sql)
        cursor.execute(sql2)
        self.conn.commit()

    def clear(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM sleep_records")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='sleep_records'")

db = Database()
db.connect()
s = Sleep( '2025-11-04',7, 6)
# db.add_record(s)
# db.remove_last_record()
# db.add_record(s)
records = db.load_table()
for record in records:
    r = Sleep(record[1], record[2], record[3])
    print(r)

        