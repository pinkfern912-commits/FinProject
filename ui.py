# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QDate, QTimer
from db import add_expense, get_expenses, get_balance

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Фінансовий проєкт")

        # Поля вводу
        self.category_label = QLabel("Категорія:")
        self.category_input = QLineEdit()

        self.amount_label = QLabel("Сума:")
        self.amount_input = QLineEdit()

        self.date_label = QLabel("Дата (YYYY-MM-DD):")
        self.date_input = QLineEdit()
        self.date_input.setText(QDate.currentDate().toString("yyyy-MM-dd"))

        # Кнопка для додавання витрати
        self.save_button = QPushButton("Зберегти витрату")
        self.save_button.clicked.connect(self.save_expense)

        # Таблиця для витрат
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Категорія", "Сума", "Дата"])

        # Кнопка для показу балансу
        self.balance_button = QPushButton("Показати баланс")
        self.balance_button.clicked.connect(self.show_balance)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.balance_button)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.resize(500, 400)

        # Таймер для автооновлення таблиці
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_expenses)
        self.timer.start(2000)  # кожні 2 секунди

    def save_expense(self):
        try:
            category = self.category_input.text()
            amount = float(self.amount_input.text())
            date = self.date_input.text()
            add_expense(category, amount, date)
            QMessageBox.information(self, "Успіх", "Витрата збережена!")
            self.show_expenses()  # одразу оновлюємо таблицю
        except Exception as e:
            QMessageBox.critical(self, "Помилка", str(e))

    def show_expenses(self):
        data = get_expenses()
        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def show_balance(self):
        balance = get_balance()
        QMessageBox.information(self, "Баланс", f"Поточний баланс: {balance}")

def run_app():
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec_())
