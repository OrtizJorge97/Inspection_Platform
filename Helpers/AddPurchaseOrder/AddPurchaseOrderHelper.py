from datetime import date
import os
import json
from flask import jsonify

class AddPurchaseOrderHelpers:
    @staticmethod
    def ValidateForm(purchaseOrderForm):
        isValid = False


        if(purchaseOrderForm.purchaseOrderInput.strip() != "" and
           purchaseOrderForm.quantityInput.strip() != "" and
           purchaseOrderForm.requestDateInput != "" and
           purchaseOrderForm.startDateInput != "" and
           purchaseOrderForm.endDateInput != ""):

            isValid = True

        return isValid

    @staticmethod
    def TrimmSpaces(purchaseOrderForm):

        purchaseOrderForm.purchaseOrderInput = purchaseOrderForm.purchaseOrderInput.replace(" ", "")
        purchaseOrderForm.quantityInput = purchaseOrderForm.quantityInput.replace(" ", "")

        return purchaseOrderForm

    @staticmethod
    def AddExtensionIfNecessaryToPO(registerToCheckExtension, fileName, baseSavingFolder=None):
        stringToReturn = ""
        if ".xlsx" in registerToCheckExtension:
            if baseSavingFolder is not None:
                stringToReturn = f"{os.path.join(baseSavingFolder, fileName)}"
            if baseSavingFolder is None:
                stringToReturn = f"{fileName}"

        if ".xlsx" not in registerToCheckExtension:
            if baseSavingFolder is not None:
                stringToReturn = f"{os.path.join(baseSavingFolder, fileName)}.xlsx"
            if baseSavingFolder is None:
                stringToReturn = f"{fileName}.xlsx"

        return stringToReturn

    @staticmethod
    def AddExtensionIfNecessary(purchaseOrderName):
        filename, file_extension = os.path.splitext(purchaseOrderName)
        if file_extension:
            purchaseOrderName = purchaseOrderName.replace(file_extension, "")

        filename, file_extension = os.path.splitext(purchaseOrderName)
        if not file_extension:
            purchaseOrderName = f"{purchaseOrderName}.xlsx"


        return purchaseOrderName

    @staticmethod
    def TakeOutFileExtensionIfNecessary(purchaseOrderName):
        filename, file_extension = os.path.splitext(purchaseOrderName)
        if file_extension:
            purchaseOrderName = purchaseOrderName.replace(file_extension, "")
        """
        if ".xlsx" in purchaseOrderName:
            purchaseOrderName = purchaseOrderName.replace(".xlsx", "")
        if ".XLSX" in purchaseOrderName:
            purchaseOrderName = purchaseOrderName.replace(".XLSX", "")
            """

        return purchaseOrderName

    @staticmethod
    def GetSeriesForGraph(listOfCriteriaFilled, evaluationCriteria):
        seriesForGraph = []
        for evaluation in evaluationCriteria:
            quantityOfRepetitions = 0
            serie = []
            serie.append(evaluation)
            for criteria in listOfCriteriaFilled:
                if evaluation == criteria:
                    quantityOfRepetitions += 1
            serie.append(quantityOfRepetitions)
            seriesForGraph.append(serie)

        print(seriesForGraph)

        return seriesForGraph

def ConvertPurchaseOrdersIntoJson(listOfPurchaseOrders):
    listToConvertToJson = []
    for purchaseOrder in listOfPurchaseOrders:
        purchaseOrderDict = {}

        purchaseOrderDict["StartDate"] = purchaseOrder.StartDate
        purchaseOrderDict["PurchaseOrder"] = purchaseOrder.PurchaseOrder
        purchaseOrderDict["Status"] = purchaseOrder.Status

        listToConvertToJson.append(purchaseOrderDict)
    

    jsonPurchaseOrder = json.dumps(listToConvertToJson, indent=4)
    print(jsonPurchaseOrder)
    #jsonPurchaseOrder = jsonify(listToConvertToJson)
    return jsonPurchaseOrder
