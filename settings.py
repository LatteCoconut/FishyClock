from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QTimeEdit,
)
from PyQt6.QtGui import QDoubleValidator, QIcon
from utils import resource_path


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(resource_path("assets/aquarium_win_sM8_icon.ico")))
        self.setFixedSize(350, 500)

        self.parent = parent

        # 创建主网格布局
        main_layout = QVBoxLayout()

        # 设置固定宽度
        input_width = 100

        qss = """
               QTimeEdit, QLineEdit {
                   color: white;  /* 未选中时的文本颜色 */
               }
               """

        # 上班时间
        start_time_layout = QHBoxLayout()  # 创建一个水平布局
        start_time_label = QLabel("上班时间:")
        self.start_time_edit = QTimeEdit(self)
        self.start_time_edit.setFixedWidth(input_width)  # 设置固定宽度
        self.start_time_edit.setTime(self.parent.start_work_time)  # 设置默认时间为 9:00
        self.start_time_edit.setStyleSheet(qss)  # 应用 QSS 样式
        start_time_layout.addWidget(start_time_label)
        start_time_layout.addWidget(self.start_time_edit)
        main_layout.addLayout(start_time_layout)  # 将水平布局添加到垂直布局中

        # 下班时间
        end_time_layout = QHBoxLayout()  # 创建一个水平布局
        end_time_label = QLabel("下班时间:")
        self.end_time_edit = QTimeEdit(self)
        self.end_time_edit.setFixedWidth(input_width)  # 设置固定宽度
        self.end_time_edit.setTime(self.parent.end_work_time)
        self.end_time_edit.setStyleSheet(qss)
        end_time_layout.addWidget(end_time_label)
        end_time_layout.addWidget(self.end_time_edit)
        main_layout.addLayout(end_time_layout)  # 将水平布局添加到垂直布局中

        # 日薪
        salary_layout = QHBoxLayout()
        self.salary_edit = QLineEdit(self)
        self.salary_edit.setFixedWidth(input_width)  # 设置固定宽度
        self.salary_edit.setStyleSheet(qss)
        # 设置 QDoubleValidator 限制输入为数字
        validator = QDoubleValidator(
            0.0, 1000000.0, 2, self
        )  # 最小值0.0，最大值1000000.0，小数点后两位
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.salary_edit.setValidator(validator)
        self.salary_edit.setText(f"{self.parent.salary:.2f}")
        salary_layout.addWidget(QLabel("日薪 (¥):"))
        salary_layout.addWidget(self.salary_edit)
        main_layout.addLayout(salary_layout)

        # 下班提示词
        word_layout = QHBoxLayout()
        self.word_edit = QLineEdit(self)
        self.word_edit.setFixedWidth(200)  # 设置固定宽度
        self.word_edit.setStyleSheet(qss)
        self.word_edit.setText(f"{self.parent.off_duty_reminder}")
        word_layout.addWidget(QLabel("下班提示词:"))
        word_layout.addWidget(self.word_edit)
        main_layout.addLayout(word_layout)

        # 添加确认和取消按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Cancel", self)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        # 设置主布局为窗口的布局
        self.setLayout(main_layout)

        # 连接按钮事件
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

    def on_ok_clicked(self):
        self.parent.start_work_time = self.start_time_edit.time()
        self.parent.end_work_time = self.end_time_edit.time()
        self.parent.salary = float(self.salary_edit.text())
        self.parent.off_duty_reminder = self.word_edit.text()
        if not self.parent.timer.isActive():
            self.parent.timer.start(1000)
        self.accept()

    def on_cancel_clicked(self):
        self.reject()
