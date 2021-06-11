import pandas as pd
import os

class FilesServices:

    def __init__(self, fileName):
        self.folderName = "InspectionFiles"
        self.fileName = fileName #the only pure filename
        self.filePath = os.path.join(
                                     os.path.normpath(os.path.expanduser('~/Desktop')),
                                     self.folderName
                                     ) #filepath without the filename

    def GetFileDataForApp(self, originalFileName):
        try:
            if(originalFileName):
                excelPandas = pd.read_excel(os.path.join(self.filePath, originalFileName),
                                            sheet_name='DTR')

                return excelPandas
            else:
                raise Exception("No especified fileName!")

        except Exception as e:
            raise Exception(f"Error: {e}")

    def CheckIfFileExists(self, fileName):
        result = False
        listOfFiles = os.listdir(self.filePath)
        originalFile = None

        for _fileName in listOfFiles:
            if fileName in _fileName:
                print(f"All good! original file: {_fileName}, fileName: {fileName}")
                result = True
                originalFile = _fileName

        return result, originalFile

    def ConvertFileToJson(self, fileData):
        pass