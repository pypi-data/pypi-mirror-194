import os

class PrepareEvidence():
    def __init__(self):
        self.currentType = ""
        self.fileType = { "NEW_FILES": "New files", "DEL_FILES": "Deleted files", 
                          "RE_FILES": "Renamed files", "MOD_FILES": "Files with modified contents",
                          "PROP_FILES": "Files with changed properties"}
        self._idiff = []    # Initiale Liste - Enthält die Zeilen der idiff Dateien
        self._list = []     # Prozessierte Liste - Enthält die Zeilen die nach der gegebenen Logik 
                            #                      prozessiert wurden
        self._unique = []   # Duplikatfreie Liste - Enthält die Zeilen ohne Duplikate
        self._sorted = []   # Sortierte Liste - Enthält die alphabetisch sortieren Zeilen
    
    def _checkFileType(self, line):
        if(self.fileType["NEW_FILES"] in line):
                self.currentType = self.fileType["NEW_FILES"]
        elif(self.fileType["DEL_FILES"] in line):
                self.currentType = self.fileType["DEL_FILES"]
        elif(self.fileType["RE_FILES"] in line):
                self.currentType = self.fileType["RE_FILES"]
        elif(self.fileType["MOD_FILES"] in line):
                self.currentType = self.fileType["MOD_FILES"]
        elif(self.fileType["PROP_FILES"] in line):
                self.currentType = self.fileType["PROP_FILES"]

    def _reset(self):
        self._idiff.clear()
        self._list.clear()
        self._unique.clear()
        self._sorted.clear()

    def _sortAlphabetically(self):
        self._sorted = sorted(self._unique)

    def _makeUnique(self):
        self._unique = list(set(self._list))

    def _addLine(self, line):
        self._list.append(line)

    def _writeToFile(self, path):
        file = open(path, "w", encoding="utf-8")
        for line in self._sorted:
            file.write(line + "\n")

    def _setIdiffData(self, idiff):
        self._idiff = idiff

    def _sanitize(self):
        for line in self._idiff:
            if(line == ""):
                self._idiff.remove("")
            elif(line == "\n"):
                self._idiff.remove("\n")

    def _process(self):
        for line in self._idiff:
            # Prüft um welchen FileType es sich handelt und setzt den gegenwärtigen FileType
            self._checkFileType(line)

            # Handelt es sich um "New Files"...
            if(self.currentType == self.fileType["NEW_FILES"]):
                if(line != "" and line != "\n"):
                    newFile = line.split("\t")
                    if(len(newFile) == 3):
                        for ts in ["m", "a", "c", "cr"]:
                            self._addLine(newFile[1] + "\t" + ts)

            # Handelt es sich um "Deleted Files"...
            elif(self.currentType == self.fileType["DEL_FILES"]):
                if(line != "" and line != "\n"):
                    delFile = line.split("\t")
                    if(len(delFile) == 3):
                            self._addLine(delFile[1] + "\t" + "d")

            # Handelt es sich um "Renamed Files", "Files with modified contents" oder
            # "Files with changed properties"...
            elif(self.currentType == self.fileType["RE_FILES"] 
                or self.currentType == self.fileType["MOD_FILES"]
                or self.currentType == self.fileType["PROP_FILES"]):
                if(line != "" and line != "\n"):
                    fi = line.split("\t")
                    if("mtime" in line):
                        self._addLine(fi[0] + "\t" + "m")
                    elif("ctime" in line):
                        self._addLine(fi[0] + "\t" + "c")
                    elif("atime" in line):
                        self._addLine(fi[0] + "\t" + "a")
                    elif("crtime" in line):
                        self._addLine(fi[0] + "\t" + "cr")

    def process(self, path, file, pathPE):
        self._reset()
        # Name des neuen Files
        newFileName = file.replace("idiff", "pe")
        # Der vollständige Pfad aus Pfad und Dateiname
        fullPath = os.path.join(path, file)
        # Öffnet die jeweilige idiff Datei
        idiff = open(fullPath, "r", encoding="utf-8")
        # Liest alle Zeilen aus der idiff Datei
        lines = idiff.readlines()
        # Übergibt sie dem Controller
        self._setIdiffData(lines)
        # Entfernt Leerzeichen und Zeilenumbrüche 
        self._sanitize() 
        # Prozessiert die Zeilen nach der gegebenen Logik
        self._process()
        # Sorgt dafür, dass keine Duplikate vorhanden sind
        self._makeUnique()
        # Sortiert die Zeilen alphabetisch
        self._sortAlphabetically()
        # Schreibt die Zeilen in eine Datei
        p = os.path.join(pathPE, newFileName)
        self._writeToFile(p)  