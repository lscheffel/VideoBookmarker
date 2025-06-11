from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout vertical principal
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")

        # Linha superior: Combobox sessões + botões Salvar e Limpar
        self.topLayout = QtWidgets.QHBoxLayout()
        self.topLayout.setSpacing(10)

        self.cmbSessions = QtWidgets.QComboBox(self.centralwidget)
        self.cmbSessions.setObjectName("cmbSessions")
        self.topLayout.addWidget(self.cmbSessions)

        self.btnSaveSession = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveSession.setObjectName("btnSaveSession")
        self.topLayout.addWidget(self.btnSaveSession)

        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setObjectName("btnClear")
        self.topLayout.addWidget(self.btnClear)

        self.verticalLayout.addLayout(self.topLayout)

        # Lista central da playlist
        self.lstPlaylist = QtWidgets.QListWidget(self.centralwidget)
        self.lstPlaylist.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.lstPlaylist.setObjectName("lstPlaylist")
        self.verticalLayout.addWidget(self.lstPlaylist)

        # Linha inferior: botões de ações (Carregar YAML, Add URL, Validar, Download, Exportar)
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout.setSpacing(10)

        self.btnLoadYaml = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoadYaml.setObjectName("btnLoadYaml")
        self.bottomLayout.addWidget(self.btnLoadYaml)

        self.btnAddUrl = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddUrl.setObjectName("btnAddUrl")
        self.bottomLayout.addWidget(self.btnAddUrl)

        self.btnValidate = QtWidgets.QPushButton(self.centralwidget)
        self.btnValidate.setObjectName("btnValidate")
        self.bottomLayout.addWidget(self.btnValidate)

        self.btnDownload = QtWidgets.QPushButton(self.centralwidget)
        self.btnDownload.setObjectName("btnDownload")
        self.bottomLayout.addWidget(self.btnDownload)

        self.btnExport = QtWidgets.QPushButton(self.centralwidget)
        self.btnExport.setObjectName("btnExport")
        self.bottomLayout.addWidget(self.btnExport)

        self.verticalLayout.addLayout(self.bottomLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Bookmarker"))
        self.btnSaveSession.setText(_translate("MainWindow", "Salvar Sessão"))
        self.btnClear.setText(_translate("MainWindow", "Limpar Playlist"))
        self.btnLoadYaml.setText(_translate("MainWindow", "Carregar YAML"))
        self.btnAddUrl.setText(_translate("MainWindow", "Adicionar URL"))
        self.btnValidate.setText(_translate("MainWindow", "Validar URLs"))
        self.btnDownload.setText(_translate("MainWindow", "Baixar Selecionados"))
        self.btnExport.setText(_translate("MainWindow", "Exportar Playlist"))
