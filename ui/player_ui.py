from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout vertical principal
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(8)

        # Layout superior: sessões + salvar + limpar
        self.topLayout = QtWidgets.QHBoxLayout()
        self.topLayout.setSpacing(6)

        self.cmbSessions = QtWidgets.QComboBox()
        self.cmbSessions.setMinimumWidth(200)
        self.topLayout.addWidget(self.cmbSessions)

        self.btnSaveSession = QtWidgets.QPushButton("💾 Salvar")
        self.btnSaveSession.setToolTip("Salvar a sessão atual")
        self.topLayout.addWidget(self.btnSaveSession)

        self.btnClear = QtWidgets.QPushButton("🧹 Limpar")
        self.btnClear.setToolTip("Limpar a playlist atual")
        self.topLayout.addWidget(self.btnClear)

        self.verticalLayout.addLayout(self.topLayout)

        # Tabela central da playlist
        self.lstPlaylist = QtWidgets.QTableWidget()
        self.lstPlaylist.setColumnCount(6)
        self.lstPlaylist.setHorizontalHeaderLabels([
            "Título", "Página", "Vídeo", "✔️ Válido", "★ Fav", "⚙ Ações"
        ])
        self.lstPlaylist.horizontalHeader().setStretchLastSection(True)
        self.lstPlaylist.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.lstPlaylist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.lstPlaylist.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)
        self.lstPlaylist.setAlternatingRowColors(True)
        self.lstPlaylist.setSortingEnabled(True)
        self.lstPlaylist.verticalHeader().setVisible(False)
        self.lstPlaylist.setShowGrid(True)
        self.lstPlaylist.setObjectName("lstPlaylist")
        self.verticalLayout.addWidget(self.lstPlaylist)

        # Layout inferior: botões de ação
        self.bottomLayout = QtWidgets.QGridLayout()
        self.bottomLayout.setHorizontalSpacing(10)
        self.bottomLayout.setVerticalSpacing(4)

        self.btnLoadYaml = QtWidgets.QPushButton("📂 Carregar YAML")
        self.btnAddUrl = QtWidgets.QPushButton("➕ Adicionar URL")
        self.btnValidate = QtWidgets.QPushButton("🔍 Validar URLs")
        self.btnDownload = QtWidgets.QPushButton("⬇️ Baixar Selecionados")
        self.btnExport = QtWidgets.QPushButton("📤 Exportar Playlist")

        self.bottomLayout.addWidget(self.btnLoadYaml, 0, 0)
        self.bottomLayout.addWidget(self.btnAddUrl, 0, 1)
        self.bottomLayout.addWidget(self.btnValidate, 0, 2)
        self.bottomLayout.addWidget(self.btnDownload, 0, 3)
        self.bottomLayout.addWidget(self.btnExport, 0, 4)

        self.verticalLayout.addLayout(self.bottomLayout)

        # Status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "🎞️ Video Bookmarker"))
