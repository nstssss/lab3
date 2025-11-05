from datetime import date

'''класс, представляющий информацию о сне'''
class Sleep:
    def __init__(self, date: date, duration: float, quality:int):
        self._date = date
        self._quality = quality
        self._duration = duration

    @property
    def date(self) -> date:
        return self._date
    @date.setter
    def date(self, value:date):
        if isinstance(value, date):
            self._date = value
    @property
    def duration(self) -> float:
        return self._duration
    @duration.setter
    def duration(self, value:int):
        self._duration = value
    @property
    def quality(self) -> int:
        return self._quality
    @quality.setter
    def quality(self, value:int):
        self._quality = value

    def __str__(self):
        return f"Дата: {self.date}, Продолжительность сна: {self.quality}, Качество сна: {self.duration}"