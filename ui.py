import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import finance

class FinanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = None
        self.menu_visible = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Фінансовий проєкт")

        # головний горизонтальний layout
        self.main_layout = QHBoxLayout(self)

        # бокове меню (зліва)
        self.side_menu = QFrame()
        self.side_menu.setFixedWidth(200)
        menu_layout = QVBoxLayout()

        btn_balance = QPushButton("Баланс")
        btn_balance.clicked.connect(self.show_balance)
        menu_layout.addWidget(btn_balance)

        btn_top = QPushButton("Топ витрат")
        btn_top.clicked.connect(self.show_top_expenses)
        menu_layout.addWidget(btn_top)

        btn_chart = QPushButton("Графік")
        btn_chart.clicked.connect(self.toggle_chart)
        menu_layout.addWidget(btn_chart)

        self.side_menu.setLayout(menu_layout)
        self.side_menu.hide()  # приховане на старті

        # контентна область (справа)
        self.content_layout = QVBoxLayout()
        self.toggle_btn = QPushButton("≡ Меню")
        self.toggle_btn.clicked.connect(self.toggle_menu)
        self.content_layout.addWidget(self.toggle_btn)

        # додаємо меню зліва, контент справа
        self.main_layout.addWidget(self.side_menu)       # лівий край
        self.main_layout.addLayout(self.content_layout)  # решта простору

        self.resize(1024, 768)

    def toggle_menu(self):
        if self.menu_visible:
            self.side_menu.hide()
            self.menu_visible = False
        else:
            self.side_menu.show()
            self.menu_visible = True

    def show_balance(self):
        balance = finance.get_balance()
        QMessageBox.information(self, "Баланс", f"Баланс: {balance:.2f}")

    def show_top_expenses(self):
        top_expenses = finance.get_top_expenses()
        QMessageBox.information(self, "Топ витрат", str(top_expenses))

    def toggle_chart(self):
        if self.canvas is None:
            fig, ax = plt.subplots()
            finance.get_expenses_by_category().plot(kind='bar', ax=ax)
            ax.set_title("Витрати по категоріях")
            self.canvas = FigureCanvas(fig)
            self.content_layout.addWidget(self.canvas)
        else:
            self.content_layout.removeWidget(self.canvas)
            self.canvas.setParent(None)
            self.canvas = None

def run_app():
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())
