from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QListWidget, QFileDialog, QLabel
)

class PlayerUI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Video Bookmark Player")

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Playlist atual:")
        self.layout.addWidget(self.label)

        self.playlist_widget = QListWidget()
        self.layout.addWidget(self.playlist_widget)

        self.import_button = QPushButton("Importar YAML")
        self.import_button.clicked.connect(self.load_yaml)
        self.layout.addWidget(self.import_button)

    def load_yaml(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo YAML", "", "YAML Files (*.yaml *.yml)")
        if file_path:
            self.controller.handle_yaml_import(file_path)

    def update_playlist(self, items):
        self.playlist_widget.clear()
        for _, url in items:
            self.playlist_widget.addItem(url)
