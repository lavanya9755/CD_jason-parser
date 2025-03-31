# from JsonParser import JSONParser
# 
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QTreeWidget, QTreeWidgetItem, QSplitter, QFileDialog, QLabel, QHBoxLayout
)
# from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QMessageBox

import json


import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from JSONParser import *

class JSONParserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced JSON Parser")
        self.resize(800, 600)
        self.initUI()

    def initUI(self):
        # Main Layout
        layout = QVBoxLayout(self)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # JSON Input Area
        self.json_input = QTextEdit(self)
        self.json_input.setPlaceholderText("Enter JSON data here...")

        # Tree View for Parsed JSON
        self.tree_view = QTreeWidget(self)
        self.tree_view.setHeaderLabels(["Key", "Value"])

        # Error Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")

        # Buttons
        self.parse_button = QPushButton("Parse JSON")
        self.expand_button = QPushButton("Expand All")
        self.collapse_button = QPushButton("Collapse All")
        self.load_button = QPushButton("Load JSON")
        self.save_button = QPushButton("Save JSON")

        # Add buttons to button layout
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.parse_button)
        button_layout.addWidget(self.expand_button)
        button_layout.addWidget(self.collapse_button)

        # Splitter for resizable sections
        splitter = QSplitter()
        splitter.addWidget(self.json_input)
        splitter.addWidget(self.tree_view)
        splitter.setSizes([300, 500])

        # Add widgets to the main layout
        layout.addLayout(button_layout)
        layout.addWidget(splitter)
        layout.addWidget(self.error_label)

        # Connect Buttons to Functions
        self.parse_button.clicked.connect(self.parse_json)
        self.expand_button.clicked.connect(self.expand_all)
        self.collapse_button.clicked.connect(self.collapse_all)
        self.load_button.clicked.connect(self.load_json)
        self.save_button.clicked.connect(self.save_json)

                # Apply custom styles
        self.setStyleSheet("""
        QWidget {
        background-color: #f4f4f4; 
        color: #333333; 
    }
    QTextEdit {
         color: #000000;
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 8px;
        font-size: 14px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        border: 1px solid #45a049;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #90EE90;
       
    }
    QTreeWidget {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
        """)

    def parse_json(self):
        json_text = self.json_input.toPlainText().strip()
        try:
            parser = JSONParser(json_text)
            json_data = parser.parse()
            self.error_label.setText("")
            self.tree_view.clear()
            self.populate_tree(json_data, self.tree_view.invisibleRootItem())
        except Exception as e:
            self.error_label.setText(f"Error: {str(e)}")
            self.tree_view.clear()

    def populate_tree(self, data, parent):
        """Populate tree with parsed JSON data."""
        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem([str(key), ""])
                parent.addChild(item)
                self.populate_tree(value, item)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                item = QTreeWidgetItem([f"[{index}]", ""])
                parent.addChild(item)
                self.populate_tree(value, item)
        else:
            parent.setText(1, str(data))

    def expand_all(self):
        """Expand all tree nodes."""
        self.tree_view.expandAll()

    def collapse_all(self):
        """Collapse all tree nodes."""
        self.tree_view.collapseAll()

    def load_json(self):
        """Load JSON from a file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            with open(file_name, "r") as file:
                data = file.read()
                self.json_input.setText(data)

    def save_json(self):
        json_text = self.json_input.toPlainText()

        file_name, _ = QFileDialog.getSaveFileName(self, "Save JSON File","", "JSON Files (*.json);;All Files (*)")

        if file_name:
            try:
                parsed_data = json.loads(json_text)  
                with open(file_name, 'w') as file:
                    json.dump(parsed_data, file, indent=4)
                self.show_message("Success", f"JSON saved successfully to:\n{file_name}")
            except Exception as e:
                self.show_message("Error", f"Failed to save JSON:\n{str(e)}", QMessageBox.Icon.Critical)

    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JSONParserApp()
    window.show()
    sys.exit(app.exec())
