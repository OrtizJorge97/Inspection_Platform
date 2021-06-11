import os
import fnmatch
#from ..Excel.PurchaseOrderService import *

class SystemServices():
    def __init__(self, folderName):
        self.folderName = folderName
        self.desktopPath = os.path.normpath(os.path.expanduser('~/Desktop'))
        self.filesSavingPath = os.path.join(self.desktopPath, self.folderName) #filepath for the saving of inspection sheets

    def CheckIfFilePathExists(self, filePath):
        return os.path.exists(filePath)

    def CreateDirectory(self):
        # the above is valid on Windows (after 7) but if you want it in os normalized form:
        result = False
        print(f"File path is: {self.filesSavingPath}")
        try:
            if not os.path.exists(self.filesSavingPath):
                os.makedirs(self.filesSavingPath)

            result = True
            return result
        except KeyError as e:
            return result
            raise KeyError(f"Error description: {e}")

    def SavePurchaseOrder(self, wb, fileName, file=None):
        try:
            if wb is not None:
                if ".xlsx" in fileName:
                    # file.save(self.filesSavingPath)
                    wb.save(f"{os.path.join(self.filesSavingPath, fileName)}")
                if ".xlsx" not in fileName:
                    wb.save(f"{os.path.join(self.filesSavingPath, fileName)}.xlsx")
                print("Entered in wb")
            if wb is None:
                file.save(os.path.join(self.filesSavingPath, fileName))
                print("Entered in NOT wb")

        except KeyError as e:
            raise KeyError(f"Error description: {e}")

    def RenameFile(self, oldFileName, oldPath, newFileName, newPath):
        #old
        if oldFileName is not newFileName:
            extensionUsed = self.FindFileExtension(oldFileName)
            print(f"oldFilePath: {oldPath} | newFilePath: {newPath}")
            if ".xlsx" in oldPath and ".xlsx" in newPath:
                os.rename(f"{oldPath}", f"{newPath}") #Error cannot find oldpath
            else:
                os.rename(f"{oldPath}{extensionUsed}", f"{newPath}{extensionUsed}")  # Error cannot find oldpath
            print("I changed name")
        else:
            print("I did not change name")

    def BuildPathForFile(self, fileName):
        pathBuilt =  os.path.join(self.filesSavingPath, fileName)
        return pathBuilt

    def FindFileExtension(self, oldFileName):
        extensionUsed = ""
        for filename in os.listdir(self.filesSavingPath):
            if oldFileName in filename:
                if ".xlsx" in filename:
                    extensionUsed = ".xlsx"
                    break
                if ".xls" in filename:
                    extensionUsed = ".xls"

        return extensionUsed


    def DeleteFile(self, filePath):
        if os.path.exists(filePath):
            os.remove(filePath)

    def SaveInspectionFile(self, partNumberForm):
        partNumberForm.file.save(os.path.join(self.filesSavingPath, partNumberForm.fileName))
