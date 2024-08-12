# main.py
import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor, QPalette, QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QMenu, QSystemTrayIcon
from settings import SettingsWindow  # 导入 SettingsWindow
from qt_material import apply_stylesheet

class FramelessWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(200, 40)

        self.init_ui()
        self.old_pos = None

        # 设置窗口透明度
        self.setWindowOpacity(0.8)

        # 默认值
        self.time_to_leave = "07:08:23"
        self.work_percentage = "20.68%"
        self.earnings = "¥204.65"

        # 创建系统托盘图标和菜单
        self.create_tray_icon()

        self.update_label()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 设置背景颜色和透明度
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 150))  # 黑色背景，150为透明度
        central_widget.setAutoFillBackground(True)
        central_widget.setPalette(palette)

        self.layout = QVBoxLayout(central_widget)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white;")  # 设置标签字体颜色为白色
        self.layout.addWidget(self.label)

    def update_label(self):
        self.label.setText(f"{self.time_to_leave} | {self.work_percentage} | {self.earnings}")

    def update_values(self, time_to_leave, work_percentage, earnings):
        self.time_to_leave = time_to_leave
        self.work_percentage = work_percentage
        self.earnings = earnings
        self.update_label()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()

    def create_tray_icon(self):
        tray_icon = QSystemTrayIcon(self)
        tray_icon.setIcon(QIcon("assets/aquarium.png"))  # 确保图标路径正确

        # 创建托盘菜单
        tray_menu = QMenu(self)

        # 添加设置选项
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        tray_menu.addAction(settings_action)

        # 添加退出选项
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 防止所有窗口关闭时退出应用程序
    # 应用 qt-material 主题
    apply_stylesheet(app, theme='dark_amber.xml')

    window = FramelessWindow()
    window.show()

    sys.exit(app.exec())
