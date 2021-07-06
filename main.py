import sys
import os
import json
import datetime
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QListWidget, QPushButton, QVBoxLayout

class Form(QDialog):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Json Test")

        self.edit = QLineEdit("")
        self.save = QPushButton("Save new favorite")
        self.delete = QPushButton("Delete selected favorite")
        self.clear_all = QPushButton("Clear all favorites")
        self.favorites_list = QListWidget()

        self.startUp()

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.save)
        layout.addWidget(self.delete)
        layout.addWidget(self.clear_all)
        layout.addWidget(self.favorites_list)

        self.setLayout(layout)
        self.save.clicked.connect(self.saveFavorite)
        self.delete.clicked.connect(self.deleteFavorite)
        self.clear_all.clicked.connect(self.deleteAllFavorites)


    #Check to see user has a favorites file, if not create a favorites directory and file with an empty json dictionary
    def startUp(self):
        current_dir = os.getcwd()
        if not os.path.exists(os.path.join(current_dir, "Favorites")):
            print("Making new default directory")
            os.mkdir(os.path.join(current_dir, "Favorites"))
            with open(os.path.join(current_dir, "Favorites") + "/user_favorites.json", "w") as f:
                dict = {}
                json.dump(dict, f)
        with open(os.path.join(current_dir, "Favorites") + "/user_favorites.json", "r") as f:
            favorites = json.load(f)
            for item in favorites:
                self.favorites_list.addItem(favorites[item])


    #Save a new favorite whenever user hits save button
    def saveFavorite(self):
        #Load in current json dictionary
        current_dir = os.getcwd()  
        with open(os.path.join(current_dir, "Favorites") + "/user_favorites.json", "r") as f:
            favorites = json.load(f)
        if self.edit.text() in list(favorites.values()):
            return
        #Add new favorite with current date and time as key
        key = datetime.datetime.now().strftime("%Y/%d/%m,%H:%M:%S")
        favorites[key] = self.edit.text()
        self.favorites_list.addItem(self.edit.text())
        #Updated favorites file with updated json dictionary
        with open(os.path.join(current_dir, "Favorites") + "/user_favorites.json", "w") as f:
            json.dump(favorites, f, indent = 2)


    def deleteFavorite(self):
        current_dir = os.getcwd()
        selected_items = self.favorites_list.selectedItems()
        if not selected_items: return
        for item in selected_items:
            with open(os.path.join(current_dir, "Favorites") + "/user_favorites.json", "r") as f:
                favorites = json.load(f)
                key_list = list(favorites.keys())
                val_list = list(favorites.values())
                key = key_list[val_list.index(item.text())]
                print(key)
                del favorites[key]
            with open(os.path.join(current_dir, "Favorites") + "/user_favorites.json", "w") as f:
                json.dump(favorites, f, indent=2)
            self.favorites_list.takeItem(self.favorites_list.row(item))


    def deleteAllFavorites(self):
        current_dir = os.getcwd()
        self.favorites_list.clear()
        with open(os.path.join(current_dir, "Favorites") + "/user_favorites.json", "w") as f:
            dict = {}
            json.dump(dict, f)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    w = 600; h = 900
    form.resize(w, h)
    form.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec_())