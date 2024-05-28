import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QLabel,
    QMessageBox,
)
from converter import Converter


class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.converter = Converter()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.input_label = QLabel("Input File: None")
        self.layout.addWidget(self.input_label)

        self.input_button = QPushButton("Select Input File")
        self.input_button.clicked.connect(self.select_input_file)
        self.layout.addWidget(self.input_button)

        self.output_label = QLabel("Output File: ")
        self.layout.addWidget(self.output_label)

        self.output_edit = QLineEdit()
        self.layout.addWidget(self.output_edit)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)
        self.layout.addWidget(self.convert_button)

        self.setLayout(self.layout)
        self.setWindowTitle("Data Converter")
        self.input_path = None

    def select_input_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Input File",
            "",
            "All Files (*);;JSON Files (*.json);;YAML Files (*.yml *.yaml);;XML Files (*.xml)",
            options=options,
        )
        if file_path:
            self.input_path = file_path
            self.input_label.setText(f"Input File: {file_path}")

    def convert(self):
        if self.input_path:
            output_path = self.output_edit.text()
            try:
                self.converter.convert(self.input_path, output_path)
                QMessageBox.information(self, "Success", "File converted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to convert file: {e}")
        else:
            QMessageBox.warning(self, "Warning", "Please select input file.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConverterApp()
    ex.show()
    sys.exit(app.exec_())
