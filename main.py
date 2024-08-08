import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor, QPalette, QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QMenu, QSystemTrayIcon


class FramelessWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)

        self.init_ui()
        self.old_pos = None

        # 设置窗口透明度
        self.setWindowOpacity(0.8)

        # 创建系统托盘图标和菜单
        self.create_tray_icon()

        # 添加页面内容
        self.pages = ["This is page 1. Drag me around!", "This is page 2. Drag me around!", "This is page 3. Drag me around!"]
        self.current_page = 0
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

        # 设置标签字体颜色为白色
        self.label.setStyleSheet("color: white;")

        self.layout.addWidget(self.label)

    def update_label(self):
        self.label.setText(self.pages[self.current_page])

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

    def wheelEvent(self, event):
        print(event.angleDelta().y())
        # 处理鼠标滚轮事件进行翻页
        if event.angleDelta().y() > 50:  # 向上滚动
            self.current_page = (self.current_page - 1) % len(self.pages)
        else:  # 向下滚动
            self.current_page = (self.current_page + 1) % len(self.pages)
        self.update_label()

    def create_tray_icon(self):
        tray_icon = QSystemTrayIcon(self)
        tray_icon.setIcon(QIcon("aquarium.png"))  # 设置托盘图标，这里需要有一个 icon.png 图标文件

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)

        tray_menu = QMenu(self)
        tray_menu.addAction(quit_action)

        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 防止所有窗口关闭时退出应用程序

    window = FramelessWindow()
    window.show()

    sys.exit(app.exec())
