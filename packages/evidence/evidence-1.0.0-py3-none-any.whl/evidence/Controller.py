import os
import time
import shutil

from datetime import datetime

class Controller():
    def __init__(self, output) -> None:
        self.startTime = time.time()
        self.workingDir = os.path.join(os.getcwd(), output) 
        self.pathPE = os.path.join(self.workingDir, "pe")
        self.pathME = os.path.join(self.workingDir, "me")
        self.pathCE = os.path.join(self.workingDir, "ce")

    def _createFolders(self):
        os.mkdir(self.workingDir)
        os.mkdir(self.pathPE)
        os.mkdir(self.pathME)
        os.mkdir(self.pathCE)

    def _clearFolders(self):
        if os.path.isdir(self.pathPE):
            shutil.rmtree(self.pathPE)
        if os.path.isdir(self.pathME):
            shutil.rmtree(self.pathME)
        if os.path.isdir(self.pathCE):
            shutil.rmtree(self.pathCE)
        if os.path.isdir(self.workingDir):
            shutil.rmtree(self.workingDir)

    def scaffold(self):
        self._clearFolders()
        self._createFolders()

    def printHeader(self, path):
        print("################################################################################")
        print("")
        print("evidence by 5f0")
        print("Insert description here...")
        print("")
        print("Current working directory: " + os.getcwd())
        print("")
        print(" Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("################################################################################")

    def printExecutionTime(self):
        end = time.time()
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")