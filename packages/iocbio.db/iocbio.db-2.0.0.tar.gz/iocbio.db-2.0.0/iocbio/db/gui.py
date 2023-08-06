# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  Copyright (C) 2019-2021
#   Laboratory of Systems Biology, Department of Cybernetics,
#   School of Science, Tallinn University of Technology
#  This file is part of project: IOCBIO Db
#

from PySide6.QtCore import QSettings, QByteArray
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QCheckBox,
    QStackedLayout,
    QRadioButton,
    QGridLayout,
    QLineEdit,
    QDialog,
)

from collections import OrderedDict


class SmallLabel(QLabel):
    def __init__(self, text, word_wrap=True):
        QLabel.__init__(self, "<small>" + text + "</small>")
        self.setWordWrap(word_wrap)


class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("PostgreSQL login")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton("Login", self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.rememberPassword = QCheckBox("Store password in keyring")
        self.rememberPassword.setChecked(False)
        layout = QGridLayout(self)
        layout.addWidget(QLabel("User:"), 0, 0)
        layout.addWidget(self.textName, 0, 1)
        layout.addWidget(QLabel("Password:"), 1, 0)
        layout.addWidget(self.textPass, 1, 1)
        layout.addWidget(self.buttonLogin, 2, 1)
        layout.addWidget(self.rememberPassword, 3, 1)

    def handleLogin(self):
        self.username = self.textName.text()
        self.password = self.textPass.text()
        self.accept()


class ConnectionParameters(QWidget):
    def __init__(self, parameters):
        QWidget.__init__(self)

        self.parameters = parameters
        layout = QGridLayout()
        for k, v in self.parameters.items():
            input_widget = QLineEdit(v["default"])
            input_widget.setMinimumWidth(150)
            v["field"] = input_widget

            row = layout.rowCount()
            layout.addWidget(QLabel(v["short"]), row, 0)
            layout.addWidget(input_widget, row, 1)
            layout.addWidget(SmallLabel(v["description"]), row + 1, 0, 1, 2)
            layout.addWidget(SmallLabel(""), row + 2, 0, 1, 2)

        self.setLayout(layout)

    def get_parameter_values(self):
        d = {}
        for k, v in self.parameters.items():
            d[k] = v["field"].text()
        return d


class ConnectionParametersSQLite(QWidget):
    def __init__(self, parameters):
        QWidget.__init__(self)

        self.parameters = d = parameters
        sqlite_fn_select_btn = QPushButton("Select SQLite database")
        sqlite_fn_select_btn.clicked.connect(self.get_filename)
        self.sqlite_filename = QLabel(d["filename"]["default"])
        self.sqlite_filename.setWordWrap(True)

        layout = QGridLayout()
        layout.addWidget(QLabel(d["filename"]["short"] + ":"), 0, 0, 1, 2)
        layout.addWidget(self.sqlite_filename, 1, 0, 1, 2)
        layout.addWidget(QLabel(" "), 3, 0, 1, 2)
        layout.addWidget(sqlite_fn_select_btn, 4, 0, 1, 2)
        layout.addWidget(SmallLabel("Select exitsing or create new SQLite database"), 5, 0, 1, 2)
        layout.addWidget(QLabel(""), 6, 0, 5, 2)

        self.setLayout(layout)

    def get_filename(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Select/create sqlite database",
            self.sqlite_filename.text(),
            "(*.sqlite)",
            options=QFileDialog.DontConfirmOverwrite,
        )

        self.sqlite_filename.setText(filename)

    def get_parameter_values(self):
        d = {"filename": self.sqlite_filename.text()}
        return d


class ConnectDatabaseGUI(QWidget):
    """Class for selecting database type"""

    settingGeometry = "Connect Database GUI/geometry"

    def __init__(self, DatabaseInterface):
        QWidget.__init__(self)

        self.DatabaseInterface = DatabaseInterface
        settings = QSettings()
        dbtype = str(settings.value(DatabaseInterface.settings_dbtype, "sqlite3"))
        self.save_settings = False
        self.sqlite3 = QRadioButton("SQLite")
        self.postgresql = QRadioButton("PostgreSQL")
        getattr(self, dbtype).setChecked(True)
        connect = QPushButton("Connect")

        self.sqlite3.toggled.connect(self.show_dbtype_options)
        connect.clicked.connect(self.connect_database)

        psql_parameters = OrderedDict(
            [
                ["hostname", {"short": "Hostname", "description": "Hostname of database server", "default": ""}],
                ["database", {"short": "Database name", "description": "", "default": ""}],
                [
                    "schema",
                    {"short": "Schema", "description": "PostgreSQL schema. For example: public", "default": "public"},
                ],
            ]
        )

        sqlite_parameters = OrderedDict(
            [
                ["filename", {"short": "Filename", "description": "Filename of SQLite database", "default": ""}],
            ]
        )

        for key, value in psql_parameters.items():
            value["default"] = str(settings.value(getattr(self.DatabaseInterface, "settings_pg_" + key), ""))

        for key, value in sqlite_parameters.items():
            value["default"] = str(
                settings.value(
                    getattr(self.DatabaseInterface, "settings_sqlite3_" + key),
                    self.DatabaseInterface.get_sqlite3_filename(self.DatabaseInterface.settings_appname, settings),
                )
            )

        self.layout_stack = QStackedLayout()
        self.sqlite_connection_parameters = ConnectionParametersSQLite(sqlite_parameters)
        self.psql_connection_parameters = ConnectionParameters(psql_parameters)
        self.layout_stack.addWidget(self.sqlite_connection_parameters)
        self.layout_stack.addWidget(self.psql_connection_parameters)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select database type:"))
        layout.addWidget(self.sqlite3)
        layout.addWidget(self.postgresql)
        layout.addLayout(self.layout_stack)
        layout.addStretch(1)
        layout.addWidget(connect)

        self.setWindowTitle(self.DatabaseInterface.settings_appname + ": connect to database")
        self.setLayout(layout)
        self.show_dbtype_options()

        # load settings
        settings = QSettings()
        self.restoreGeometry(settings.value(ConnectDatabaseGUI.settingGeometry, QByteArray()))

    def show_dbtype_options(self):
        if self.sqlite3.isChecked():
            self.layout_stack.setCurrentWidget(self.sqlite_connection_parameters)
        if self.postgresql.isChecked():
            self.layout_stack.setCurrentWidget(self.psql_connection_parameters)

    def connect_database(self):
        settings = QSettings()
        settings.setValue(ConnectDatabaseGUI.settingGeometry, self.saveGeometry())
        if self.sqlite3.isChecked():
            settings.setValue(self.DatabaseInterface.settings_dbtype, "sqlite3")
            for k, v in self.layout_stack.currentWidget().get_parameter_values().items():
                settings.setValue(getattr(self.DatabaseInterface, "settings_sqlite3_" + k), v)

        if self.postgresql.isChecked():
            settings.setValue(self.DatabaseInterface.settings_dbtype, "postgresql")
            for k, v in self.layout_stack.currentWidget().get_parameter_values().items():
                settings.setValue(getattr(self.DatabaseInterface, "settings_pg_" + k), v)
        self.save_settings = True
        self.close()
