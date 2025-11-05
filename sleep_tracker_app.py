import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLabel, QGroupBox, QMessageBox, QHeaderView,
    QFormLayout, QSpinBox, QDoubleSpinBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from database import Database
from sleep import Sleep
from datetime import date


class SleepTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Sleep Tracker - Отслеживание сна")
        self.setGeometry(100, 100, 1400, 900)
        self.current_edit_id = None
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Левая панель
        left_panel = QVBoxLayout()

        # Форма ввода данных
        input_group = QGroupBox("Добавить/Изменить запись о сне")
        input_layout = QFormLayout(input_group)

        # Поле даты
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        input_layout.addRow("Дата:", self.date_edit)

        # Поле продолжительности сна
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0, 24)
        self.duration_spin.setDecimals(1)
        self.duration_spin.setSuffix(" часов")
        self.duration_spin.setValue(7.0)
        input_layout.addRow("Продолжительность сна:", self.duration_spin)

        # Поле качества сна
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 10)
        self.quality_spin.setSuffix("/10")
        self.quality_spin.setValue(7)
        input_layout.addRow("Качество сна:", self.quality_spin)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить запись")
        self.add_button.clicked.connect(self.add_record)
        self.add_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")

        self.update_button = QPushButton("Изменить выбранную")
        self.update_button.clicked.connect(self.update_selected_record)
        self.update_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")

        self.delete_last_button = QPushButton("Удалить последнюю")
        self.delete_last_button.clicked.connect(self.delete_last_record)
        self.delete_last_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")

        self.clear_button = QPushButton("Очистить поля")
        self.clear_button.clicked.connect(self.clear_fields)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_last_button)
        button_layout.addWidget(self.clear_button)
        input_layout.addRow(button_layout)

        left_panel.addWidget(input_group)

        # Таблица с записями
        table_group = QGroupBox("История сна")
        table_layout = QVBoxLayout(table_group)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Дата", "Продолжительность", "Качество", "Время создания"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)
        table_layout.addWidget(self.table)

        left_panel.addWidget(table_group)

        # Правая панель
        right_panel = QVBoxLayout()

        # График
        chart_group = QGroupBox("График сна")
        chart_layout = QVBoxLayout(chart_group)

        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas)

        # Статистика под графиком
        stats_group = QGroupBox("Статистика")
        stats_layout = QFormLayout(stats_group)

        self.avg_duration_label = QLabel("0 часов")
        self.avg_quality_label = QLabel("0/10")
        self.total_records_label = QLabel("0")

        stats_layout.addRow("Средняя продолжительность:", self.avg_duration_label)
        stats_layout.addRow("Среднее качество:", self.avg_quality_label)
        stats_layout.addRow("Всего записей:", self.total_records_label)

        chart_layout.addWidget(stats_group)
        right_panel.addWidget(chart_group)

        main_layout.addLayout(left_panel, 2)
        main_layout.addLayout(right_panel, 1)

    def on_table_selection_changed(self):
        """Обработчик изменения выбора в таблице"""
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.load_record_to_form(row)
            self.update_button.setEnabled(True)
        else:
            self.update_button.setEnabled(False)
            self.clear_fields()

    """загружает выбранную запись в форму для редактирования"""
    def load_record_to_form(self, row):
        try:
            record_id = int(self.table.item(row, 0).text())
            self.current_edit_id = record_id
            # Загружаем полные данные записи из БД
            record_data = self.db.get_record(record_id)

            if not record_data:
                return

            # Получаем данные из записи БД
            record_date = record_data[1]  # date
            duration = record_data[2]  # sleep_duration
            quality = record_data[3]  # sleep_quality

            # Устанавливаем значения в форму
            date_parts = list(map(int, record_date.split('-')))
            self.date_edit.setDate(QDate(date_parts[0], date_parts[1], date_parts[2]))
            self.duration_spin.setValue(float(duration))
            self.quality_spin.setValue(int(quality))

            # Сохраняем ID для обновления
            self.current_edit_id = record_id

        except Exception as e:
            print(f"Ошибка загрузки записи в форму: {e}")

    """обновление выбранной записи"""
    def update_selected_record(self):
        if (self.current_edit_id == None):
            QMessageBox.warning(self, "Внимание", "Не выбрана запись для редактирования")
            return
        try:
            # Получение данных из формы
            qt_date = self.date_edit.date()
            sleep_date = date(qt_date.year(), qt_date.month(), qt_date.day())
            duration = self.duration_spin.value()
            quality = self.quality_spin.value()

            # Создание нового объекта Sleep
            updated_record = Sleep(sleep_date, duration, quality)

            self.db.update_record(self.current_edit_id, updated_record)

            self.load_data()
            self.clear_fields()
            QMessageBox.information(self, "Успех", "Запись успешно обновлена")

        except Exception as e:
            error_msg = str(e)
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить запись:\n{error_msg}")

    """загрузка данных в таблицу"""
    def load_data(self):
        try:
            records = self.db.load_table()

            # Очистка таблицы
            self.table.setRowCount(0)

            # Заполнение таблицы
            for row_idx, record in enumerate(records):
                self.table.insertRow(row_idx)
                for col_idx, value in enumerate(record):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.update_statistics()
            self.update_chart()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    """обновление статистики"""
    def update_statistics(self):
        try:
            records = self.db.load_table()
            if not records:
                self.avg_duration_label.setText("0 часов")
                self.avg_quality_label.setText("0/10")
                self.total_records_label.setText("0")
                return

            total_duration = sum(record[2] for record in records)
            total_quality = sum(record[3] for record in records)

            avg_duration = total_duration / len(records)
            avg_quality = total_quality / len(records)

            self.avg_duration_label.setText(f"{avg_duration:.1f} часов")
            self.avg_quality_label.setText(f"{avg_quality:.1f}/10")
            self.total_records_label.setText(str(len(records)))

        except Exception as e:
            print(f"Ошибка обновления статистики: {e}")

    """обеовление графика"""
    def update_chart(self):
        try:
            records = self.db.load_table()
            if not records:
                self.ax.clear()
                self.ax.text(0.5, 0.5, 'Нет данных для отображения',
                             ha='center', va='center', transform=self.ax.transAxes)
                self.canvas.draw()
                return

            recent_records = records[-10:]
            dates = [record[1] for record in recent_records]
            durations = [record[2] for record in recent_records]
            qualities = [record[3] for record in recent_records]

            self.ax.clear()

            color1 = 'tab:blue'
            self.ax.set_xlabel('Дата')
            self.ax.set_ylabel('Продолжительность (часы)', color=color1)
            line1 = self.ax.plot(dates, durations, 'o-', color=color1, label='Продолжительность')[0]
            self.ax.tick_params(axis='y', labelcolor=color1)

            ax2 = self.ax.twinx()
            color2 = 'tab:red'
            ax2.set_ylabel('Качество сна', color=color2)
            line2 = ax2.plot(dates, qualities, 's-', color=color2, label='Качество')[0]
            ax2.tick_params(axis='y', labelcolor=color2)

            lines = [line1, line2]
            labels = [line.get_label() for line in lines]
            self.ax.legend(lines, labels, loc='upper left')

            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            print(f"Ошибка обновления графика: {e}")

    """добавление новой записи"""
    def add_record(self):
        try:
            qt_date = self.date_edit.date()
            sleep_date = date(qt_date.year(), qt_date.month(), qt_date.day())
            duration = self.duration_spin.value()
            quality = self.quality_spin.value()

            sleep_record = Sleep(sleep_date, duration, quality)
            self.db.add_record(sleep_record)

            self.load_data()
            self.clear_fields()
            QMessageBox.information(self, "Успех", "Запись успешно добавлена")

        except Exception as e:
            error_msg = str(e)
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись:\n{error_msg}")

    """удаление последней записи"""
    def delete_last_record(self):
        try:
            records = self.db.load_table()
            if not records:
                QMessageBox.warning(self, "Внимание", "Таблица пуста, нечего удалять")
                return

            last_record = records[-1]
            record_id = last_record[0]
            record_date = last_record[1]

            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить запись от {record_date}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db.remove_last_record()
                self.load_data()
                QMessageBox.information(self, "Успех", "Запись успешно удалена")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить запись: {e}")

    """очистка полей ввода"""
    def clear_fields(self):
        self.date_edit.setDate(QDate.currentDate())
        self.duration_spin.setValue(7.5)
        self.quality_spin.setValue(7)
        self.current_edit_id = None
        self.update_button.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = SleepTrackerGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()