import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor, QPalette, QIcon, QAction
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMenu,
    QSystemTrayIcon,
)
from settings import SettingsWindow
from qt_material import apply_stylesheet
from PyQt6.QtCore import QTime, QTimer
import platform
from utils import resource_path

current_os = platform.system()


class FramelessWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if current_os == "Windows":
            self.setWindowFlags(
                Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(200, 40)

        self.init_ui()
        self.old_pos = None

        # 设置上班和下班时间
        self.start_work_time = QTime(9, 0)
        self.end_work_time = QTime(18, 0)
        self.salary = 100.00
        self.off_duty_reminder = "到点啦，🏃‍♂️下班啦！"

        # 设置窗口透明度
        self.setWindowOpacity(0.8)

        # 创建系统托盘图标和菜单
        self.create_tray_icon()
        self.update_label()
        # 使用计时器每分钟更新一次剩余时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)  # 每分钟更新一次

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 设置背景颜色和透明度
        palette = self.palette()
        palette.setColor(
            QPalette.ColorRole.Window, QColor(0, 0, 0, 150)
        )  # 黑色背景，150为透明度
        central_widget.setAutoFillBackground(True)
        central_widget.setPalette(palette)

        self.layout = QVBoxLayout(central_widget)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white;")  # 设置标签字体颜色为白色
        self.layout.addWidget(self.label)

    def update_label(self):
        current_time = QTime.currentTime()

        total_time = self.start_work_time.secsTo(self.end_work_time)
        elapsed_time = self.start_work_time.secsTo(current_time)

        if elapsed_time >= total_time:
            elapsed_time = total_time  # 防止超过 100%
            time_left = 0
        else:
            time_left = total_time - elapsed_time

        hours_left = time_left // 3600
        minutes_left = (time_left % 3600) // 60
        seconds_left = time_left % 60  # 计算剩余的秒数
        time_to_leave = f"{hours_left:02}:{minutes_left:02}:{seconds_left:02}"

        # 计算工作进度百分比
        work_percentage = f"{(elapsed_time / total_time) * 100:.2f}%"

        # 计算已挣的薪水
        earnings = (elapsed_time / total_time) * self.salary

        self.label.setText(f"{time_to_leave} | {work_percentage} | ¥{earnings:.2f}")

        # 检查是否达到 100%
        if work_percentage == "100.00%" and time_to_leave == "00:00:00":
            self.timer.stop()  # 停止计时器
            self.send_off_duty_notification()  # 发送下班通知

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
        if current_os == "Windows":
            tray_icon.setIcon(QIcon(resource_path("assets/aquarium_win.png")))
        else:
            tray_icon.setIcon(
                QIcon(resource_path("assets/aquarium.png"))
            )  # 确保图标路径正确

        # 创建托盘菜单
        tray_menu = QMenu(self)

        # 添加设置选项
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        tray_menu.addAction(settings_action)

        # 添加退出选项
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.instance().quit)  # 退出应用程序
        tray_menu.addAction(quit_action)

        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()

    def send_off_duty_notification(self):
        if current_os == "Darwin":
            try:
                from pync import Notifier

                # 发送下班通知
                Notifier.notify(f"{self.off_duty_reminder}", title="FishyClock")
            except ImportError:
                pass
        elif current_os == "Windows":
            try:
                from win11toast import toast

                toast(f"{self.off_duty_reminder}")
            except ImportError:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 防止所有窗口关闭时退出应用程序

    # from pyobjc import objc
    # from Cocoa import NSApplication, NSApplicationActivationPolicyAccessory
    # # 让应用程序不在 Dock 栏显示
    # NSApp = objc.objc_getClass("NSApplication").sharedApplication()
    # NSApp.setActivationPolicy_(NSApplicationActivationPolicyAccessory)

    # 应用 qt-material 主题
    apply_stylesheet(app, theme="dark_amber.xml")

    window = FramelessWindow()
    window.show()

    sys.exit(app.exec())
