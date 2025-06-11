import sys
import webbrowser
from functools import partial
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QInputDialog,
    QTableWidgetItem, QCheckBox
)
from PyQt6.QtCore import Qt
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
        self.playlist = []  # lista de dicts: {'page_url', 'url', 'title', 'valid', 'favorite'}
        self.current_session = None  # nome da sessão carregada/salva

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
        url, ok = QInputDialog.getText(self, "Adicionar URL manualmente", "Digite a URL do vídeo:")
        if ok and url:
            video = {
                'title': url,
                'page_url': url,
                'url': '',
                'valid': False,
                'favorite': False
            }
            self.playlist.append(video)
            self.refresh_playlist_ui()

    def add_to_playlist(self, url):
        if any(item['page_url'] == url for item in self.playlist):
            return  # evitar duplicatas
        self.playlist.append({
            'page_url': url,
            'url': None,
            'title': None,
            'valid': None,
            'favorite': False
        })

    def refresh_playlist_ui(self):
        self.ui.lstPlaylist.setRowCount(0)

        for i, video in enumerate(self.playlist):
            self.ui.lstPlaylist.insertRow(i)

            # Título
            title_item = QTableWidgetItem(video.get("title") or "")
            self.ui.lstPlaylist.setItem(i, 0, title_item)

            # Página (page_url)
            page_item = QTableWidgetItem(video.get("page_url") or "")
            self.ui.lstPlaylist.setItem(i, 1, page_item)

            # URL direta
            url_item = QTableWidgetItem(video.get("url") or "")
            self.ui.lstPlaylist.setItem(i, 2, url_item)

            # Válido ✔️ ou ✖
            valid = video.get("valid", False)
            valid_item = QTableWidgetItem("✔" if valid else "✖")
            valid_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.lstPlaylist.setItem(i, 3, valid_item)

            # Favorito (QCheckBox)
            fav_checkbox = QCheckBox()
            fav_checkbox.setChecked(video.get("favorite", False))
            fav_checkbox.setStyleSheet("margin-left:10px; margin-right:10px;")
            self.ui.lstPlaylist.setCellWidget(i, 4, fav_checkbox)

            def on_favorite_changed(state, index=i):
                self.playlist[index]["favorite"] = (state == Qt.CheckState.Checked)
                if self.current_session:
                    self.db.save_session(self.current_session, self.playlist)

            fav_checkbox.stateChanged.connect(partial(on_favorite_changed, index=i))

    def validate_playlist(self):
        for item in self.playlist:
            info = get_video_info(item['page_url'])
            if info:
                item['valid'] = True
                item['title'] = info.get('title') or item['page_url']
                item['url'] = info.get('high')
            else:
                item['valid'] = False
        self.refresh_playlist_ui()

    def download_selected(self):
        selected_rows = set(index.row() for index in self.ui.lstPlaylist.selectedIndexes())
        if not selected_rows:
            QMessageBox.warning(self, "Download", "Selecione um vídeo na lista para baixar.")
            return

        folder = QFileDialog.getExistingDirectory(self, "Escolha a pasta para salvar")
        if not folder:
            return

        for row in selected_rows:
            video_data = self.playlist[row]
            if not video_data.get('url'):
                QMessageBox.warning(self, "Download", f"URL de vídeo inválida: {video_data['page_url']}")
                continue
            path = download_video(video_data['url'], folder)
            if path:
                QMessageBox.information(self, "Download", f"Vídeo baixado: {path}")
            else:
                QMessageBox.warning(self, "Download", f"Falha ao baixar: {video_data['page_url']}")

    def export_playlist(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar Playlist", "", "M3U Files (*.m3u)")
        if not path:
            return
        urls = [item['url'] for item in self.playlist if item.get('url')]
        success = export_playlist_to_m3u(urls, path)
        if success:
            QMessageBox.information(self, "Exportar", "Playlist exportada com sucesso.")
        else:
            QMessageBox.warning(self, "Exportar", "Erro ao exportar playlist.")

    def clear_playlist(self):
        self.playlist = []
        self.refresh_playlist_ui()

    def play_video(self, item):
        index = item.row()
        url = self.playlist[index]['page_url']
        webbrowser.open(url)

    def save_current_session(self):
        name, ok = QInputDialog.getText(self, "Salvar Sessão", "Nome da sessão:")
        if not ok or not name.strip():
            return
        name = name.strip()
        self.current_session = name
        self.db.save_session(name, self.playlist)
        self.load_sessions()
        QMessageBox.information(self, "Sessão", f"Sessão '{name}' salva com sucesso.")

    def load_sessions(self):
        sessions = self.db.list_sessions()
        self.ui.cmbSessions.blockSignals(True)
        self.ui.cmbSessions.clear()
        self.ui.cmbSessions.addItem("-- Selecione Sessão --")
        self.ui.cmbSessions.addItems(sessions)
        self.ui.cmbSessions.blockSignals(False)

    def load_session_from_dropdown(self, index):
        if index == 0:
            return
        name = self.ui.cmbSessions.currentText()
        playlist = self.db.load_session(name)
        if playlist is not None:
            self.playlist = playlist
            self.current_session = name
            self.refresh_playlist_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
