import sys
from PyQt6.QtWidgets import QApplication
from ui.player_ui import PlayerUI
from core import yaml_loader, db

class Controller:
    def __init__(self):
        db.init_db()
        self.session = 'default'

    def handle_yaml_import(self, file_path):
        urls = yaml_loader.load_yaml_file(file_path)
        db.add_to_playlist(urls, self.session)
        self.refresh_ui()

    def refresh_ui(self):
        items = db.get_playlist(self.session)
        self.ui.update_playlist(items)

    def start(self):
        self.ui = PlayerUI(controller=self)
        self.ui.show()
        self.refresh_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.start()
    sys.exit(app.exec())
