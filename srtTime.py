import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QFileDialog, QVBoxLayout, QWidget

def convert_milliseconds_to_centiseconds(ms):
    return int(ms / 10)

def convert_timestamp(timestamp):
    time, milliseconds = timestamp.split(',')
    milliseconds = convert_milliseconds_to_centiseconds(int(milliseconds))
    return f"{time},{milliseconds:02d}"

def convert_srt_timecodes(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".srt"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    if '-->' in line:
                        start_timestamp, end_timestamp = line.split(' --> ')
                        start_timestamp = convert_timestamp(start_timestamp.strip())
                        end_timestamp = convert_timestamp(end_timestamp.strip())
                        outfile.write(f"{start_timestamp} --> {end_timestamp}\n")
                    else:
                        outfile.write(line)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SRT时码转换器')
        self.layout = QVBoxLayout()

        # 按钮：选择输入文件夹
        self.btn_input = QPushButton('选择SRT输入文件夹', self)
        self.btn_input.clicked.connect(self.open_folder_dialog)
        self.layout.addWidget(self.btn_input)

        # 按钮：选择输出文件夹
        self.btn_output = QPushButton('选择输出文件夹', self)
        self.btn_output.clicked.connect(self.save_folder_dialog)
        self.layout.addWidget(self.btn_output)

        # 标签：显示输入输出文件夹
        self.label_input = QLabel('输入文件夹: 未选择', self)
        self.layout.addWidget(self.label_input)
        self.label_output = QLabel('输出文件夹: 未选择', self)
        self.layout.addWidget(self.label_output)

        # 按钮：执行转换
        self.btn_convert = QPushButton('转换时码', self)
        self.btn_convert.clicked.connect(self.convert_files)
        self.layout.addWidget(self.btn_convert)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.resize(400, 200)  # 调整窗口大小

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if folder:
            self.input_folder = folder
            self.label_input.setText(f'输入文件夹: {folder}')

    def save_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if folder:
            self.output_folder = folder
            self.label_output.setText(f'输出文件夹: {folder}')

    def convert_files(self):
        if self.input_folder and self.output_folder:
            convert_srt_timecodes(self.input_folder, self.output_folder)
            # 弹出消息框通知用户转换完成
            msg = QMessageBox()
            msg.setWindowTitle("转换完成")
            msg.setText("SRT文件的时码已成功转换！")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            print(f"转换完成，文件已保存到: {self.output_folder}")
        else:
            print("请确保已选择输入文件夹和输出文件夹路径")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
