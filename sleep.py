from datetime import date

'''класс, представляющий информацию о сне'''
class Sleep:
    def __init__(self, date: date, duration: int, quality:str):
        self.date = date
        self.quality = quality
        self.duration = duration

    def __str__(self):
        return f"Дата: {self.date}, Продолжительность сна: {self.quality}, Качество сна: {self.duration}"