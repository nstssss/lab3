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


@pytest.fixture
def sample_sleep():
    """Фикстура для создания тестовой записи сна"""
    return Sleep(date=date(2024, 1, 15), duration=7.5, quality=8)


def test_valid_sleep_record(sample_record):
    assert sample_record.date == date(2024, 1, 11)  # Должен быть date объект
    assert sample_record.duration == 7.5
    assert sample_record.quality == 8


def test_sleep_creation(sample_sleep):
    """Тест создания объекта Sleep"""
    assert sample_sleep.date == date(2024, 1, 15)
    assert sample_sleep.duration == 7.5
    assert sample_sleep.quality == 8


def test_sleep_properties(sample_sleep):
    """Тест свойств (property) класса Sleep"""
    # Тест свойства date
    sample_sleep.date = date(2024, 1, 20)
    assert sample_sleep.date == date(2024, 1, 20)

    # Тест свойства duration
    sample_sleep.duration = 8.0
    assert sample_sleep.duration == 8.0

    # Тест свойства quality
    sample_sleep.quality = 9
    assert sample_sleep.quality == 9


def test_sleep_string_representation(sample_sleep):
    """Тест строкового представления объекта Sleep"""
    expected_str = "Дата: 2024-01-15, Продолжительность сна: 8, Качество сна: 7.5"
    assert str(sample_sleep) == expected_str


def test_sleep_invalid_date(sample_sleep):
    """Тест установки невалидной даты"""
    # Должно игнорировать не-date объекты
    original_date = sample_sleep.date
    sample_sleep.date = "invalid_date"
    assert sample_sleep.date == original_date