# import sqlite3
#
# # Подключение к базе данных
# connection = sqlite3.connect('expenses.db')
#
# # Создание объекта курсора
# cursor = connection.cursor()
#
# # Пример выполнения SQL-запроса (можно заменить на свой запрос)
#
#
# cursor.execute("SELECT * FROM categories")
#
# results = cursor.fetchall()
#
# # Вывод результатов
# for row in results:
#     print(row)
#
# # Закрытие курсора и соединения с базой данных
# cursor.close()
# connection.close()

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QListWidget, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox
from datetime import *  # Импорт модуля datetime
import sqlite3

class ExpensesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Expenses Tracker")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Создание таблицы для отображения расходов
        self.expenses_table = QTableWidget()
        layout.addWidget(self.expenses_table)

        # Заголовки столбцов
        self.expenses_table.setColumnCount(3)  # Добавляем столбец для даты
        self.expenses_table.setHorizontalHeaderLabels(["Дата", "Сумма", "Категория"])

        # Создание списка категорий
        self.categories_list = QListWidget()
        layout.addWidget(self.categories_list)

        # Создание поля для ввода новой категории
        self.new_category_edit = QLineEdit()
        layout.addWidget(self.new_category_edit)

        # Кнопка для добавления новой категории
        self.add_category_button = QPushButton("Добавить категорию")
        self.add_category_button.clicked.connect(self.add_category)
        layout.addWidget(self.add_category_button)

        # Кнопка для удаления выбранной категории
        self.remove_category_button = QPushButton("Удалить категорию")
        self.remove_category_button.clicked.connect(self.remove_category)
        layout.addWidget(self.remove_category_button)

        # Поле для ввода суммы
        self.amount_edit = QLineEdit()
        layout.addWidget(self.amount_edit)

        # Выпадающий список для выбора категории
        self.category_combo = QComboBox()
        layout.addWidget(self.category_combo)

        # Кнопка для добавления расхода
        self.add_expense_button = QPushButton("Добавить расход")
        self.add_expense_button.clicked.connect(self.add_expense)
        layout.addWidget(self.add_expense_button)

        self.central_widget.setLayout(layout)

        self.populate_expenses()
        self.populate_categories()

        # Создание виджета для отображения расходов за день, неделю и месяц
        self.expenses_summary_widget = QWidget()
        self.expenses_summary_layout = QVBoxLayout(self.expenses_summary_widget)
        self.expenses_summary_layout.addWidget(QLabel("Расходы за:"))
        self.expenses_summary_layout.addWidget(QLabel("Сегодня:"))
        self.expenses_summary_layout.addWidget(QLabel("Неделя:"))
        self.expenses_summary_layout.addWidget(QLabel("Месяц:"))
        layout.addWidget(self.expenses_summary_widget)

        self.central_widget.setLayout(layout)

        self.update_expenses_summary()
        self.add_expense_button.clicked.connect(self.add_expense_clicked)
    def populate_expenses(self):
        # Подключение к базе данных
        connection = sqlite3.connect('expenses.db')
        cursor = connection.cursor()

        # Выполнение запроса для получения расходов
        cursor.execute("SELECT * FROM expenses")
        results = cursor.fetchall()

        # Установка размеров таблицы
        self.expenses_table.setRowCount(len(results))

        # Заполнение таблицы данными
        for i, row in enumerate(results):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))  # Преобразование значения в строку
                self.expenses_table.setItem(i, j, item)

        # Закрытие курсора и соединения с базой данных
        cursor.close()
        connection.close()

    def populate_categories(self):
        # Подключение к базе данных
        connection = sqlite3.connect('expenses.db')
        cursor = connection.cursor()

        # Выполнение запроса для получения категорий
        cursor.execute("SELECT * FROM categories")
        results = cursor.fetchall()

        # Очистка списка категорий перед заполнением
        self.categories_list.clear()
        self.category_combo.clear()

        # Заполнение списка категорий
        for row in results:
            self.categories_list.addItem(row[1])  # добавляем только название категории
            self.category_combo.addItem(row[1])   # добавляем категорию в выпадающий список

        # Закрытие курсора и соединения с базой данных
        cursor.close()
        connection.close()

    def add_category(self):
        # Получение текста из поля ввода
        category_name = self.new_category_edit.text()

        # Проверка на пустое поле
        if not category_name:
            QMessageBox.warning(self, "Ошибка", "Введите название категории")
            return

        # Подключение к базе данных
        connection = sqlite3.connect('expenses.db')
        cursor = connection.cursor()

        # Выполнение запроса для добавления категории
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
        connection.commit()

        # Закрытие курсора и соединения с базой данных
        cursor.close()
        connection.close()

        # Очистка поля ввода
        self.new_category_edit.clear()

        # Обновление списка категорий
        self.populate_categories()

    def remove_category(self):
        # Получение выбранной категории
        selected_category = self.categories_list.currentItem()

        if selected_category is None:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления")
            return

        # Подтверждение удаления категории
        reply = QMessageBox.question(self, "Удаление категории", f"Вы уверены, что хотите удалить категорию '{selected_category.text()}'?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Подключение к базе данных
            connection = sqlite3.connect('expenses.db')
            cursor = connection.cursor()

            # Выполнение запроса для удаления категории
            cursor.execute("DELETE FROM categories WHERE name=?", (selected_category.text(),))
            connection.commit()

            # Закрытие курсора и соединения с базой данных
            cursor.close()
            connection.close()

            # Обновление списка категорий
            self.populate_categories()

    def add_expense(self):
        # Получение текста из поля ввода суммы и выбранной категории
        amount = self.amount_edit.text()
        category = self.category_combo.currentText()

        # Получение текущей даты и времени
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Проверка на пустое поле
        if not amount:
            QMessageBox.warning(self, "Ошибка", "Введите сумму расхода")
            return

        # Подключение к базе данных
        connection = sqlite3.connect('expenses.db')
        cursor = connection.cursor()

        # Выполнение запроса для добавления расхода
        cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)", (amount, category, current_date))
        connection.commit()

        # Закрытие курсора и соединения с базой данных
        cursor.close()
        connection.close()

        # Очистка поля ввода суммы
        self.amount_edit.clear()

        # Обновление списка расходов
        self.populate_expenses()

    def add_expense_clicked(self):
        # В этом методе вы должны добавить новый расход в базу данных
        # После добавления нового расхода вызовите метод update_expenses_summary для обновления данных
        self.update_expenses_summary()

    def update_expenses_summary(self):
        # Получение текущей даты
        today = datetime.now().strftime('%Y-%m-%d')

        # Получение даты начала недели (понедельник)
        start_of_week = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')

        # Получение даты конца недели (воскресенье)
        end_of_week = (datetime.now() + timedelta(days=6 - datetime.now().weekday())).strftime('%Y-%m-%d')

        # Подключение к базе данных
        connection = sqlite3.connect('expenses.db')
        cursor = connection.cursor()

        # Выполнение запросов для получения суммы расходов за день, неделю и месяц
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (f"{today}%",))
        today_expenses = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (start_of_week, end_of_week))
        week_expenses = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')")
        month_expenses = cursor.fetchone()[0] or 0

        # Обновление меток на виджете
        self.expenses_summary_layout.itemAt(1).widget().setText(f"Сегодня: {today_expenses} руб. (Бюджет: 1000 руб.)")
        self.expenses_summary_layout.itemAt(2).widget().setText(f"Неделя: {week_expenses} руб. (Бюджет: 7000 руб.)")
        self.expenses_summary_layout.itemAt(3).widget().setText(f"Месяц: {month_expenses} руб. (Бюджет: 30000 руб.)")

        # Закрытие курсора и соединения с базой данных
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpensesApp()
    window.show()
    sys.exit(app.exec())



