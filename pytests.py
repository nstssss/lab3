from dataclasses import *
from sleep import Sleep
from datetime import date
import pytest

@pytest.fixture
def sample_record():
    """Фикстура с date объектом"""
    return Sleep(
        date=date(2024, 1, 11),
        duration=7.5,
        quality=8
    )

# Тестовые функции без параметра self
def test_valid_sleep_record(sample_record):
    """Тест создания валидной записи о сне"""
    assert sample_record.date == date(2024, 1, 11)  # Должен быть date объект
    assert sample_record.duration == 7.5
    assert sample_record.quality == 8