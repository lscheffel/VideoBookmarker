import sys
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QInputDialog
)
from ui.player_ui import Ui_MainWindow
from core.db import Database
from core.yaml_loader import load_urls_from_file
from core.video_utils import download_video, get_video_info
from core.export import export_playlist_to_m3u

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Banco de dados
        self.db = Database("video_bookmarker.db")
        self.db.create_tables()

        # Estado
        self.playlist = []  # lista de dicts: {'url', 'title', 'valid', 'favorite'}
        self.current_session = None

        # Setup UI
        self.setup_connections()
        self.load_sessions()

    def setup_connections(self):
        self.ui.btnLoadYaml.clicked.connect(self.load_yaml)
        self.ui.btnAddUrl.clicked.connect(self.add_url_manually)
        self.ui.btnValidate.clicked.connect(self.validate_playlist)
        self.ui.btnDownload.clicked.connect(self.download_selected)
        self.ui.btnExport.clicked.connect(self.export_playlist)
        self.ui.btnClear.clicked.connect(self.clear_playlist)
        self.ui.cmbSessions.currentIndexChanged.connect(self.load_session_from_dropdown)
        self.ui.lstPlaylist.itemDoubleClicked.connect(self.play_video)
        self.ui.btnSaveSession.clicked.connect(self.save_current_session)

    def load_yaml(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir arquivo YAML", "", "YAML Files (*.yaml *.yml)")
        if not path:
            return
        urls = load_urls_from_file(path)
        for url in urls:
            self.add_to_playlist(url)
        self.refresh_playlist_ui()

    def add_url_manually(self):
        url, ok = QInputDialog.getText(self, "Adicionar URL", "Insira a URL do vídeo:")
        if ok and url.strip():
            self.add_to_playlist(url.strip())
            self.refresh_playlist_ui()

    def add_to_playlist(self, url):
        if any(item['url'] == url for item in self.playlist):
            return  # evitar duplicatas
        self.playlist.append({'url': url, 'title': None, 'valid': None, 'favorite': False})

    def refresh_playlist_ui(self):
        self.ui.lstPlaylist.clear()
        for item in self.playlist:
            status = "[✓]" if item.get('valid') else "[✗]" if item.get('valid') is False else "[?]"
            favorite = "★" if item.get('favorite') else " "
            title = item.get('title') or item['url']
            display_text = f"{favorite} {status} {title}"
            self.ui.lstPlaylist.addItem(display_text)

    def validate_playlist(self):
        for item in self.playlist:
            # Considera a URL como sendo a da página do Xvideos
            info = get_video_info(item['url'])
            if info:
                item['valid'] = True
                item['title'] = info['title'] or item['url']
                item['url'] = info['high']  # substitui pela URL .mp4 real
            else:
                item['valid'] = False
        self.refresh_playlist_ui()
    def download_selected(self):
        selected_items = self.ui.lstPlaylist.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Download", "Selecione um vídeo na lista para baixar.")
            return
        folder = QFileDialog.getExistingDirectory(self, "Escolha a pasta para salvar")
        if not folder:
            return
        for selected_item in selected_items:
            index = self.ui.lstPlaylist.row(selected_item)
            video_data = self.playlist[index]
            path = download_video(video_data['url'], folder)
            if path:
                QMessageBox.information(self, "Download", f"Vídeo baixado: {path}")
            else:
                QMessageBox.warning(self, "Download", f"Falha ao baixar: {video_data['url']}")

    def export_playlist(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar Playlist", "", "M3U Files (*.m3u)")
        if not path:
            return
        urls = [item['url'] for item in self.playlist]
        success = export_playlist_to_m3u(urls, path)
        if success:
            QMessageBox.information(self, "Exportar", "Playlist exportada com sucesso.")
        else:
            QMessageBox.warning(self, "Exportar", "Erro ao exportar playlist.")

    def clear_playlist(self):
        self.playlist = []
        self.refresh_playlist_ui()

    def play_video(self, item):
        index = self.ui.lstPlaylist.row(item)
        url = self.playlist[index]['url']
        webbrowser.open(url)

    def save_current_session(self):
        name, ok = QInputDialog.getText(self, "Salvar Sessão", "Nome da sessão:")
        if not ok or not name.strip():
            return
        # Salva a sessão no banco com a playlist atual
        self.db.save_session(name.strip(), self.playlist)
        self.load_sessions()
        QMessageBox.information(self, "Sessão", f"Sessão '{name.strip()}' salva com sucesso.")

    def load_sessions(self):
        sessions = self.db.list_sessions()
        self.ui.cmbSessions.clear()
        self.ui.cmbSessions.addItem("-- Selecione Sessão --")
        self.ui.cmbSessions.addItems(sessions)

    def load_session_from_dropdown(self, index):
        if index == 0:
            return
        name = self.ui.cmbSessions.currentText()
        playlist = self.db.load_session(name)
        if playlist is not None:
            self.playlist = playlist
            self.refresh_playlist_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
