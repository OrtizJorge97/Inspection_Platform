import pandas as pd
from DeltaHubRestApi.Models.Entities.ShowableInspection import ShowableInspectionModel

class PartNumberClass:

    @staticmethod
    def InitializeDataToFillByAppAsPandas(dataToFillByAppPandasRaw, defaultNanValues):
        dataToFillByAppPandasRawCopy = dataToFillByAppPandasRaw.copy()

        dataToFillByAppPandasRawCopy.columns = defaultNanValues.keys()
        dataToFillByAppInitialized = dataToFillByAppPandasRawCopy.fillna(value=defaultNanValues)

        return dataToFillByAppInitialized

    @staticmethod
    def ConvertBasicInformationIntoPandas(inspectionSheetPandas, basicInformationData, basicInformationCellCoords):
        #basic information cells is a dictionary wich has the read write coordinates excel
        #inspectionSheet pandas is the whole partnumber sheet
        basicInformationDataEmpty = basicInformationData.copy()

        for basicInfoKey in basicInformationData:
            #loop through the coordinates and append it to basic Info list
            basicInformationData[basicInfoKey] = inspectionSheetPandas.iloc[basicInformationCellCoords[basicInfoKey][0], basicInformationCellCoords[basicInfoKey][1]]

        basicInformationPandas = pd.DataFrame(data=basicInformationData, columns=basicInformationData.keys(), index=[0])
        basicInformationPandas = PartNumberClass.ReplaceBasicInfoNanForEmpty(basicInformationPandas, basicInformationDataEmpty)

        return basicInformationPandas


    @staticmethod
    def ReplaceBasicInfoNanForEmpty(pandasValues, basicInformationDataEmpty):
        pandasWithDefaultValue = pandasValues.copy()
        pandasWithDefaultValue = pandasWithDefaultValue.fillna(basicInformationDataEmpty)

        return pandasWithDefaultValue

    @staticmethod
    def TryConvertToFloat(value):
        try:
            _value = float(value)
            isValid = True

            return isValid, _value
        except:
            _value = None
            isValid = False

            return isValid, _value

def ConvertShowableInspectionIntoObject(dataShowableDict):
     showableInspectionModel = ShowableInspectionModel()

     showableInspectionModel.dimension = dataShowableDict["dimension"]
     showableInspectionModel.units = dataShowableDict["units"]
     showableInspectionModel.infLimit = dataShowableDict["inferiorLimit"]
     showableInspectionModel.supLimit = dataShowableDict["superiorLimit"]
     showableInspectionModel.part1 = dataShowableDict["measure1"]
     showableInspectionModel.part2 = dataShowableDict["measure2"]
     showableInspectionModel.part3 = dataShowableDict["measure3"]
     showableInspectionModel.part4 = dataShowableDict["measure4"]
     showableInspectionModel.part5 = dataShowableDict["measure5"]
     showableInspectionModel.part6 = dataShowableDict["measure6"]
     showableInspectionModel.ok = dataShowableDict["ok"]
     showableInspectionModel.notOk = dataShowableDict["notOk"]

     return showableInspectionModel

def ValidateOnlyNumbers(stringToValidate):
    string_lowerCase = stringToValidate.lower()
    contains_letters = string_lowerCase.islower()

    return contains_letters

