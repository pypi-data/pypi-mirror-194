from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

data = [
    {'input': 'ch1', 'enable': True, 'name': 'ch1', 'type': 'EEG'},
    {'input': 'ch2', 'enable': True, 'name': 'ch2', 'type': 'EEG'},
    {'input': 'ch3', 'enable': True, 'name': 'ch3', 'type': 'EEG'},
    {'input': 'ch4', 'enable': True, 'name': 'ch4', 'type': 'EEG'},
]


class TableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self.chan_data = data
        self.checks = {}

        self.columns = [
            {'property': 'input', 'header': 'Channel', 'edit': False, 'editor': 'default'},
            {'property': 'enable', 'header': 'Enable', 'edit': True, 'editor': 'checkbox'},
            {'property': 'name', 'header': 'Name', 'edit': True, 'editor': 'limit_text'},
            {'property': 'type', 'header': 'Type', 'edit': False, 'editor': 'combobox'},
        ]

    def columnCount(self, index) -> int:
        """Return number of columns
        """
        if self.chan_data:
            return len(self.chan_data[0])
        return len(self.columns)

    def rowCount(self, *args):
        """Return number of rows
        """
        return len(self.chan_data)

    # def checkState(self, index):
    #     if index in self.checks.keys():
    #         return self.checks[index]
    #     else:
    #         return Qt.Unchecked

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        col = index.column()

        value = self._getitem(index.row(), index.column())
        if (role == Qt.DisplayRole) or (role == Qt.EditRole):
            return value
        elif role == Qt.CheckStateRole and col == 1:
            # print(f"{value=}")
            # print(f"{self.checkState(QPersistentModelIndex(index))=}")
            return value
            # return self.checkState(QPersistentModelIndex(index))

        if role == Qt.BackgroundRole:
            if index.column() == 2 and (
                "".join(
                    e for e in value if e.isalnum()).strip() == "" or self.get_list_names().count(value) > 1):
                return QBrush("#fa5c62")

        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignHCenter | Qt.AlignVCenter)
        return None

    def get_list_names(self, full=False) -> list:
        """Return list of custom names
        """
        if full is True:
            return [d["name"] for d in self.chan_data]
        return [d["name"] for d in self.chan_data if d["enable"]]

    def _getitem(self, row: int, column: int) -> str:
        """Get property item based on table row and column

        Args:
            row (int): row number
            column (int): column number

        Returns:
            str: property value
        """
        if (row >= len(self.chan_data)) or (column >= len(self.columns)):
            return None

        # get channel properties
        property = self.chan_data[row]
        # get property name from column description
        property_name = self.columns[column]['property']
        # get property value
        if property_name in ['input', 'name', 'type']:
            d = str(property[property_name])
        elif property_name == 'enable':

            d = 2 if property[property_name] is True else 0
        else:
            d = None
        return d

    def setData(self, index, value, role=Qt.EditRole):

        if not index.isValid():
            return False
        if role == Qt.CheckStateRole:
            self._setitem(index.row(), index.column(), value)
            # self.checks[QPersistentModelIndex(index)] = value
            return True
        return False

    def flags(self, index):
        """Abstract method from QAbstactTableModel
        """
        fl = QAbstractTableModel.flags(self, index)
        if self.columns[index.column()]['editor'] == "checkbox":
            fl |= Qt.ItemIsEditable | Qt.ItemIsUserCheckable
        if not index.isValid():
            return Qt.ItemIsEnabled
        if not self.columns[index.column()]['edit']:
            return Qt.NoItemFlags
        return fl | Qt.ItemIsEditable

    def _setitem(self, row: int, column: int, value: str) -> bool:
        """Set property item based on table row and column

        Args:
            row (int): row number
            column (int): column number
            value (str): value to set

        Returns:
            bool: True if property value was set, False if not
        """
        if (row >= len(self.chan_data)) or (column >= len(self.columns)):
            return False
        # get channel properties
        property = self.chan_data[row]
        # get property name from column description
        property_name = self.columns[column]['property']
        # set channel property
        if property_name == 'enable':
            print(f"\n{value=}")
            value = True if value == 2 else False
            property["enable"] = value
            print(f"{value=}")
            return True

        if property_name == 'name':
            n = value
            if "".join(n.split()) == "":
                return False
            property["name"] = value
            return True

        if property_name == 'type':
            n = value
            property["type"] = value
            return True

        return False

    def get_chan_mask(self) -> list:
        """Return channel mask as list"""
        return [d["enable"] for d in self.chan_data]

    # pylint: disable=invalid-name
    def headerData(self, col, orientation, role):
        """Abstract method from QAbstactTableModel to get the column header
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.columns[col]['header']

    def comboBoxList(self, column: int) -> list:
        """Get list of items for comboboxes

        Args:
            column (int): column number

        Returns:
            list: list of combobox items
        """
        if column >= len(self.columns):
            return None
        if self.columns[column]['property'] == 'type':
            return ExGModes.all_values()
        if self.columns[column]['property'] == 'name':
            return ELECTRODES_10_20

    def editorType(self, column: int) -> str:
        """Get the columns editor type from column description

        Args:
            column (int): column number

        Returns:
            str: editor type
        """
        if column >= len(self.columns):
            return None
        return str(self.columns[column]['editor'])


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QHBoxLayout Example")
        # Create a QHBoxLayout instance
        layout = QHBoxLayout()
        self.btn = QPushButton("Print")
        self.view = QTableView()
        self.model = TableModel()
        self.view.setModel(self.model)
        # Add widgets to the layout
        layout.addWidget(self.btn)
        layout.addWidget(self.view, 1)
        # Set the layout on the application's window
        self.setLayout(layout)
        self.btn.clicked.connect(lambda: print(self.model.chan_data))
        # print(self.children())


if __name__ == "__main__":
    import sys

    # app = QApplication(sys.argv)
    # view = QTableView()
    # model = TableModel()
    # view.setModel(model)
    # view.show()

    # sys.exit(app.exec_())
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
