from flask import (
    Flask, request, send_from_directory, render_template, jsonify, make_response, redirect, url_for, Blueprint, flash
)
from flask_login import login_required
from werkzeug.utils import secure_filename
#from flask_cors import cross_origin

import os
import json
import datetime

from .Helpers.PartNumberHelper.AddPartNumberHelper import AddPartNumberHelpers
from .Helpers.AddPurchaseOrder.AddPurchaseOrderHelper import AddPurchaseOrderHelpers, ConvertPurchaseOrdersIntoJson
from .Services.System.SystemService import SystemServices
from .Services.Excel.InspectionsSheetService import InspectionsSheetExcelService, InspectionSheetOpenPyManager
from .Constants.AddPurchaseOrderConstants import PurchaseOrderFormConstants
from .Constants.AddPurchaseOrderConstants import PurchaseOrderServerSideConstants, ImportPurchaseOrderFormConstants
from .Constants.PartNumberConstants import PartNumberConstantsClass
from .Models.PurchaseOrderFormModel import PurchaseOrderForm
from .Models.PartNumberFormModel import PartNumberForm
from .Services.Excel.PurchaseOrderService import PurchaseOrderExcel, PurchaseOrderManagement
from .Services.Status.PurchaseOrderStatusService import PurchaseOrderStatusManagement
from .Helpers.PartNumberHelper.PartNumberModule import ValidateOnlyNumbers

from . import db
from .modelsdb import *

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return redirect(url_for("auth.login"))

@main.route("/PurchaseOrderIndex")
@login_required
def purchase_order_index():
    purchaseOrderStatusManagement = PurchaseOrderStatusManagement()

    purchaseOrders = PurchaseOrdersTable.query.all() #Get purchase orders data for analysis
    purchaseOrders = purchaseOrderStatusManagement.ManagePurchaseOrderStatusTime(purchaseOrders, db) #analyze status time for purchase order

    return render_template("PurchaseOrderIndex.html", purchaseOrders=purchaseOrders, date=datetime.date.today())

@main.route("/InspectionsIndex")
@login_required
def InspectionsIndex():
    inspections = InspectionsTable.query.all()
    purchaseOrders = PurchaseOrdersTable.query.all()
    purchaseOrders = ConvertPurchaseOrdersIntoJson(purchaseOrders)

    for inspection in inspections:
        if inspection.Result is None:
            inspection.Result = ""
        if inspection.ResponsableName is None:
            inspection.ResponsableName = ""

    db.session.commit()

    return render_template("InspectionsIndex.html", inspections=inspections, purchaseOrders=purchaseOrders)

@main.route("/AddPurchaseOrder")
@login_required
def addPurchaseOrder():
    return render_template("AddPurchaseOrder.html")

@main.route("/HandleAddPurchaseOrder", methods=["POST"])
@login_required
def HandleAddPurchaseOrder():
    purchaseOrderForm = PurchaseOrderForm()

    purchaseOrderForm.purchaseOrderInput = request.form.get(PurchaseOrderFormConstants().purchaseOrderInput)
    purchaseOrderForm.statusInput = request.form.get(PurchaseOrderFormConstants().statusInput)
    purchaseOrderForm.quantityInput = request.form.get(PurchaseOrderFormConstants().quantityInput)
    purchaseOrderForm.requestDateInput = request.form.get(PurchaseOrderFormConstants().requestDateInput)
    purchaseOrderForm.startDateInput = request.form.get(PurchaseOrderFormConstants().startDateInput)
    purchaseOrderForm.endDateInput = request.form.get(PurchaseOrderFormConstants().endDateInput)

    purchaseOrderForm = AddPurchaseOrderHelpers().TrimmSpaces(purchaseOrderForm)

    purchaseOrder = PurchaseOrdersTable.query.filter_by(PurchaseOrder=purchaseOrderForm.purchaseOrderInput).first()

    if purchaseOrder:
        flash("There is already a Purchase Order with this name")
        return redirect(url_for("main.addPurchaseOrder"))

    isValid = purchaseOrderForm.purchaseOrderInput and \
              purchaseOrderForm.quantityInput and \
              purchaseOrderForm.requestDateInput and \
              purchaseOrderForm.startDateInput and \
              purchaseOrderForm.endDateInput

    if not isValid:
        flash("All fields must be filled.")
        return redirect(url_for("main.addPurchaseOrder"))

    else:
        purchaseOrderExcel = PurchaseOrderExcel()
        systemServices = SystemServices(PurchaseOrderServerSideConstants.purchaseOrderFolderParent)
        purchaseOrderForm = AddPurchaseOrderHelpers().TrimmSpaces(purchaseOrderForm)

        db.session.add(PurchaseOrdersTable(PurchaseOrder=AddPurchaseOrderHelpers.TakeOutFileExtensionIfNecessary(purchaseOrderForm.purchaseOrderInput),
                                           Status=purchaseOrderForm.statusInput,
                                           StatusTime=PurchaseOrderFormConstants.purchaseOrderInTime,
                                           Quantity=purchaseOrderForm.quantityInput,
                                           RequestDate=purchaseOrderForm.requestDateInput,
                                           StartDate=purchaseOrderForm.startDateInput,
                                           EndDate=purchaseOrderForm.endDateInput,
                                           ModifiedDate=datetime.datetime.today(),
                                           FilePath=f"{os.path.join(systemServices.filesSavingPath, AddPurchaseOrderHelpers.AddExtensionIfNecessary(purchaseOrderForm.purchaseOrderInput))}",
                                           FileName=AddPurchaseOrderHelpers.AddExtensionIfNecessary(purchaseOrderForm.purchaseOrderInput),
                                           FileType=PurchaseOrderFormConstants.nativeFileType)
                       )

        db.session.commit()

        systemServices = SystemServices(PurchaseOrderServerSideConstants.purchaseOrderFolderParent)
        systemServices.CreateDirectory()

        wb = purchaseOrderExcel.CreatePurchaseOrderInExcel(purchaseOrderForm)
        systemServices.SavePurchaseOrder(wb, AddPurchaseOrderHelpers.AddExtensionIfNecessary(purchaseOrderForm.purchaseOrderInput))

    return redirect("/PurchaseOrderIndex", code=302)


@main.route("/ImportPurchaseOrder")
@login_required
def ImportPurchaseOrder():
    return render_template("ImportPurchaseOrder.html")


@main.route("/HandleImportPurchaseOrder", methods=["POST"])
@login_required
def HandleImportPurchaseOrder():
    file = request.files.get(ImportPurchaseOrderFormConstants.purchaseOrderFileInput)
    fileName = secure_filename(file.filename)

    if not fileName:
        flash("You have not selected a file :(")
        return redirect(url_for("main.ImportPurchaseOrder"))

    purchaseOrderForm = PurchaseOrderForm()

    systemServices = SystemServices(PurchaseOrderServerSideConstants.purchaseOrderFolderParent)
    systemServices.CreateDirectory()
    systemServices.SavePurchaseOrder(wb=None, fileName=fileName, file=file)

    filePath = systemServices.BuildPathForFile(fileName)

    purchaseOrderForm = PurchaseOrderExcel.GetBasicDataFromPurchaseOrder(filePath, purchaseOrderForm)

    print(purchaseOrderForm.purchaseOrderInput)
    print(purchaseOrderForm.quantityInput)

    db.session.add(PurchaseOrdersTable(PurchaseOrder=fileName,
                                       Quantity=purchaseOrderForm.quantityInput,
                                       RequestDate=purchaseOrderForm.requestDateInput,
                                       StartDate=purchaseOrderForm.startDateInput,
                                       EndDate=purchaseOrderForm.endDateInput,
                                       ModifiedDate=datetime.now(),
                                       FilePath=filePath,
                                       FileName=fileName,
                                       FileType=PurchaseOrderFormConstants.importedFileType)
                   )
    db.session.commit()

    return redirect(url_for("main.purchase_order_index"))

@main.route("/ModifyPurchaseOrder")
@login_required
def ModifyPurchaseOrder():
    #Get Parameters
    purchaseOrderId = request.args.get("id")

    purchaseOrder = PurchaseOrdersTable.query.filter_by(Id=purchaseOrderId).first()

    #Pass parameters to page
    return render_template("ModifyPurchaseOrder.html", purchaseOrder=purchaseOrder)

@main.route("/HandleModifyPurchaseOrder", methods=["POST"])
@login_required
def HandleModifyPurchaseOrder():
    purchaseOrder = PurchaseOrderForm()
    purchaseOrderExcel = PurchaseOrderExcel()
    systemServices = SystemServices(PurchaseOrderServerSideConstants.purchaseOrderFolderParent)

    purchaseOrderId = request.form.get("idInput")

    purchaseOrder.purchaseOrderInput = request.form.get(PurchaseOrderFormConstants().purchaseOrderInput)
    purchaseOrder.statusInput = request.form.get(PurchaseOrderFormConstants().statusInput)
    purchaseOrder.quantityInput = request.form.get(PurchaseOrderFormConstants().quantityInput)
    purchaseOrder.requestDateInput = request.form.get(PurchaseOrderFormConstants().requestDateInput)
    purchaseOrder.startDateInput = request.form.get(PurchaseOrderFormConstants().startDateInput)
    purchaseOrder.endDateInput = request.form.get(PurchaseOrderFormConstants().endDateInput)

    purchaseOrderDb = PurchaseOrdersTable.query.filter_by(Id=purchaseOrderId).first()

    oldFileName = purchaseOrderDb.PurchaseOrder
    newFileName = purchaseOrder.purchaseOrderInput

    purchaseOrderDb.PurchaseOrder = purchaseOrder.purchaseOrderInput.replace(" ", "")
    purchaseOrderDb.Status = purchaseOrder.statusInput
    purchaseOrderDb.Quantity = purchaseOrder.quantityInput.replace(" ", "")
    purchaseOrderDb.RequestDate = purchaseOrder.requestDateInput
    purchaseOrderDb.StartDate = purchaseOrder.startDateInput
    purchaseOrderDb.EndDate = purchaseOrder.endDateInput
    purchaseOrderDb.ModifiedDate = datetime.datetime.today()
    purchaseOrderDb.FilePath = AddPurchaseOrderHelpers.AddExtensionIfNecessaryToPO(registerToCheckExtension=purchaseOrderDb.PurchaseOrder,
                                                                                   baseSavingFolder=systemServices.filesSavingPath,
                                                                                   fileName=purchaseOrder.purchaseOrderInput)
    purchaseOrderDb.FileName = AddPurchaseOrderHelpers.AddExtensionIfNecessaryToPO(registerToCheckExtension=purchaseOrderDb.PurchaseOrder,
                                                                                   fileName=purchaseOrder.purchaseOrderInput)


    systemServices = SystemServices(PurchaseOrderServerSideConstants.purchaseOrderFolderParent)
    oldPath = systemServices.BuildPathForFile(oldFileName) #Build new path for file
    newPath = systemServices.BuildPathForFile(newFileName)
    systemServices.RenameFile(oldFileName, oldPath, newFileName, newPath) #rename old file for new file if old name and new name are different it will rename

    wb = purchaseOrderExcel.ModifyPurchaseOrderInExcel(purchaseOrder, newPath) #modify the object excel file

    db.session.commit() #save changes in db
    systemServices.SavePurchaseOrder(wb, purchaseOrder.purchaseOrderInput) #Save Modifications to excel with new name

    return redirect(url_for("main.purchase_order_index"))

@main.route("/DeletePurchaseOrder")
@login_required
def DeletePurchaseOrder():
    purchaseOrderId = request.args.get("id")

    purchaseOrder = PurchaseOrdersTable.query.filter_by(Id=purchaseOrderId).first()

    return render_template("DeletePurchaseOrder.html", purchaseOrder=purchaseOrder)

@main.route("/HandleDeletePurchaseOrder", methods=["POST"])
@login_required
def HandleDeletePurchaseOrder():
    purchaseOrderId = int( request.form.get("idInput") )
    systemServicesForPurchaseOrder = SystemServices(PurchaseOrderServerSideConstants.purchaseOrderFolderParent)
    systemServicesForPartNumber = SystemServices(PartNumberConstantsClass.FOLDER_SAVE)

    purchaseOrder = PurchaseOrdersTable.query.filter_by(Id=purchaseOrderId).first()
    inspections = InspectionsTable.query.filter_by(PurchaseOrder=purchaseOrder.PurchaseOrder)

    for inspection in inspections:
        db.session.delete(inspection)
    db.session.delete(purchaseOrder)
    db.session.commit()

    for inspection in inspections:
        systemServicesForPartNumber.DeleteFile(inspection.FilePath)
    systemServicesForPurchaseOrder.DeleteFile(purchaseOrder.FilePath)

    return redirect(url_for("main.purchase_order_index"))

@main.route("/DownloadPurchaseOrderFile/<path:fileName>")
@login_required
def DownloadPurchaseOrderFile(fileName):
    systemServices = SystemServices(PurchaseOrderServerSideConstants.purchaseOrderFolderParent)

    return send_from_directory(directory=systemServices.filesSavingPath, filename=AddPurchaseOrderHelpers.AddExtensionIfNecessary(fileName))


@main.route("/DetailsPurchaseOrder", methods=["GET"])
@login_required
def DetailsPurchaseOrder():
    purchaseOrderId = request.args.get("id")

    purchaseOrder = PurchaseOrdersTable.query.filter_by(Id=purchaseOrderId).first()

    return render_template("DetailsPurchaseOrder.html", purchaseOrder=purchaseOrder)

@main.route("/AddNewPartNumber")
@login_required
def AddNewPartNumber():
    purchaseOrderStatusManagement = PurchaseOrderStatusManagement()

    purchaseOrders = PurchaseOrdersTable.query.all()  # Get purchase orders data for analysis
    purchaseOrders = purchaseOrderStatusManagement.ManagePurchaseOrderStatusTime(purchaseOrders, db)  # analyze status time for purchase order

    inspections = InspectionsTable.query.all()

    return render_template("AddNewPartNumber.html", purchaseOrders=purchaseOrders, inspections=inspections)

@main.route("/HandleAddNewPartNumber", methods=["POST"])
@login_required
def HandleAddNewPartNumber():
    partNumberForm = PartNumberForm()
    systemServices = SystemServices(PartNumberConstantsClass.FOLDER_SAVE)

    partNumberForm.purchaseOrderBelong = request.form.get(PartNumberConstantsClass.PURCHASE_ORDER_INPUT) #purchase order which belongs
    quantity = request.form.get("partNumberQuantity")
    partNumberForm.file = request.files.get(PartNumberConstantsClass.FILE_INPUT) #file object
    partNumberForm.fileName = secure_filename( partNumberForm.file.filename ) #file name

    isValid = AddPartNumberHelpers.ValidateForm(partNumberForm)

    print(f"isValid: {isValid}")
    if not isValid:
        flash("All fields must be filled!")
        return redirect(url_for("main.AddNewPartNumber"))
    
    partNumberForm = AddPartNumberHelpers.TrimmSpaces(partNumberForm)

    quantityHasLetters = ValidateOnlyNumbers(quantity)
    if quantityHasLetters:
        flash("Quantity must not have letters")
        return redirect(url_for("main.AddNewPartNumber"))

    if ".xlsx" not in partNumberForm.purchaseOrderBelong:
        partNumberForm.purchaseOrderBelong = f"{partNumberForm.purchaseOrderBelong}.xlsx"

    partNumberForm.purchaseOrderBelong = AddPurchaseOrderHelpers.TakeOutFileExtensionIfNecessary(partNumberForm.purchaseOrderBelong)

    purchaseOrder = PurchaseOrdersTable.query.filter_by(PurchaseOrder=partNumberForm.purchaseOrderBelong).first()
    if not purchaseOrder:
        flash("Purchase Order not registered, please add it in Purchase Order section :(")
        return redirect(url_for("main.AddNewPartNumber"))

    inspections = InspectionsTable.query.filter_by(PartNumber=partNumberForm.fileName).first()
    if inspections:
        flash("There is already a Part Number document registered :(")
        return redirect(url_for("main.AddNewPartNumber"))

    db.session.add(InspectionsTable(PartNumber=partNumberForm.fileName,
                                    PurchaseOrder=partNumberForm.purchaseOrderBelong,
                                    Quantity=quantity,
                                    Status=purchaseOrder.Status,
                                    ModifiedDate=datetime.datetime.today(),
                                    FilePath=f"{os.path.join(systemServices.filesSavingPath, partNumberForm.fileName)}",
                                    FileName=partNumberForm.fileName))

    db.session.commit()

    systemServices.CreateDirectory()
    systemServices.SaveInspectionFile(partNumberForm)

    return redirect(url_for("main.InspectionsIndex"))

@main.route("/HandlePartNumberFilter")
@login_required
def HandlePartNumberFilter():
    #purchaseOrderFilter = request.form.get("filterInput")
    purchaseOrderFilter = request.args.get("filterInput")
    inspections = None
    filterText = ""

    if not purchaseOrderFilter:
        inspections = InspectionsTable.query.all()
    else:
        filterText = purchaseOrderFilter
        inspections = InspectionsTable.query.filter_by(PurchaseOrder=purchaseOrderFilter)
        if not inspections:
            filterText = ""
            flash("Purchase Order Not Available")
            return render_template("InspectionsIndex.html", inspections=InspectionsTable.query.all())

    return render_template("InspectionsIndex.html", inspections=inspections, filterText=filterText)



@main.route("/DeletePartNumber")
@login_required
def DeletePartNumber():
    partNumberId = request.args.get("id")

    inspection = InspectionsTable.query.filter_by(Id=partNumberId).first()

    return render_template("DeletePartNumber.html", inspection=inspection)

@main.route("/HandleDeletePartNumber", methods=["DELETE"])
#@cross_origin(origin='*',headers=['Content-Type','Authorization'])
#@login_required
def HandleDeletePartNumber():
    idsToDelete = request.get_json()
    print(idsToDelete)
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    """
    partNumberId = request.form.get("idInput")
    systemServices = SystemServices(PartNumberConstantsClass.FOLDER_SAVE)

    inspection = InspectionsTable.query.filter_by(Id=partNumberId).first()

    #Delete inspection resume from purchase order document.
    purchaseOrderManagement = PurchaseOrderManagement(inspection.PurchaseOrder)
    purchaseOrderManagement.DeletePartNumberFromPurchaseOrderDoc(inspection.PurchaseOrder, inspection.PartNumber)

    db.session.delete(inspection)

    filePath = systemServices.BuildPathForFile(inspection.FileName)

    db.session.commit()
    systemServices.DeleteFile(filePath)

    return redirect(url_for("main.InspectionsIndex"))
    """

@main.route("/DownloadPartNumber/<path:filename>")
@login_required
def DownloadPartNumber(filename):
    systemServices = SystemServices(PartNumberConstantsClass.FOLDER_SAVE)

    return send_from_directory(directory=systemServices.filesSavingPath, filename=filename)

@main.route("/ViewPartNumber", methods=["GET"])
@login_required
def ViewPartNumber():
    idInspection = request.args.get("id")
    inspection = InspectionsTable.query.filter_by(Id=idInspection).first()

    partNumber = inspection.PartNumber
    partNumber = partNumber.replace(" ", "")

    inspectionsSheetService = InspectionsSheetExcelService(partNumber)
    inspectionsSheetService.ReadInspectionSheetExcel()

    if inspectionsSheetService.errorMessage is not None:
        print(inspectionsSheetService.jsonInspectionSheet)
        return inspectionsSheetService.jsonInspectionSheet

    inspection = InspectionsTable.query.filter_by(PartNumber=inspectionsSheetService.fileName).first()

    inspectionsSheetService.purchaseOrder = inspection.PurchaseOrder
    inspectionsSheetService.ConvertInspectionSheetToJson()
    print(inspectionsSheetService.dataToShowInPlatform)
    #return inspectionsSheetService.jsonInspectionSheet

    return render_template("ViewPartNumber.html", inspection=inspection, inspectionToShow=inspectionsSheetService.dataToShowInPlatform)


@main.route("/GetInspectionSheet", methods=["GET"])
def GetEspecificFile():
    # This method will be called from App
    partNumber = request.args.get('partnumber')
    partNumber = partNumber.replace(" ", "")

    inspectionsSheetService = InspectionsSheetExcelService(partNumber)
    inspectionsSheetService.ReadInspectionSheetExcel()

    if inspectionsSheetService.errorMessage is not None:
        print(inspectionsSheetService.jsonInspectionSheet)
        return inspectionsSheetService.jsonInspectionSheet

    inspection = InspectionsTable.query.filter_by(PartNumber=inspectionsSheetService.fileName).first()

    inspectionsSheetService.purchaseOrder = inspection.PurchaseOrder
    inspectionsSheetService.ConvertInspectionSheetToJson()

    return inspectionsSheetService.jsonInspectionSheet

@main.route("/GetAllInspections", methods=["GET"])
def GetAllData():
    #mobile app will send the current item registered,
    #here it will compare if the newest record in db is equals to the newest record sent by mobile app, then it will send all of the partnumbers
    #the parameter to receive will be the part number
    # the parameter may come as None or with a value
    newestPartNumberFromApp = request.args.get("newestPartNumber")
    jsonDictionary = {
        "ShortPartNumberList": None,
        "ErrorMessage": None
    }
    if ".xlsx" not in newestPartNumberFromApp:
        newestPartNumberFromApp = f"{newestPartNumberFromApp}.xlsx"
    listOfPartNumbers = []

    newestPartNumberServer = db.session.query(InspectionsTable).order_by(InspectionsTable.Id.desc()).first()
    print(f"part number from app: {newestPartNumberFromApp}")
    print(f"Newest part number from server side: {newestPartNumberServer.PartNumber}")
    print(newestPartNumberFromApp == newestPartNumberServer.PartNumber)
    if newestPartNumberFromApp != newestPartNumberServer.PartNumber:
        partNumbers = InspectionsTable.query.all()
        for partNumber in partNumbers:
            purchaseOrder = PurchaseOrdersTable.query.filter_by(PurchaseOrder=partNumber.PurchaseOrder).first()
            shortPartNumber = {
                "PartNumber": InspectionsSheetExcelService.TakeOutFileExtensionIfNecessary(partNumber.PartNumber),
                "PurchaseOrder": partNumber.PurchaseOrder,
                "Status": purchaseOrder.Status
            }

            listOfPartNumbers.append(shortPartNumber)
        listOfPartNumbers.reverse()

        print( listOfPartNumbers )
        jsonDictionary["ShortPartNumberList"] = listOfPartNumbers

    elif newestPartNumberFromApp != newestPartNumberServer:
        jsonDictionary["ShortPartNumberList"] = None


    jsonData = json.dumps(jsonDictionary, indent=4)

    return jsonData

@main.route("/PostInspection", methods=["POST"])
def PostInspection():
    jsonPostedDict = request.get_json()
    print(jsonPostedDict)
    systemServices = SystemServices(PartNumberConstantsClass.FOLDER_SAVE)
    inspectionService = InspectionsSheetExcelService(jsonPostedDict["BasicInformation"]["PartNumber"])
    inspectionSheetOpenPy = InspectionSheetOpenPyManager()

    #inspectionService.AddFileExtensionIfNecessary()
    #inspectionService.filePath = systemServices.BuildPathForFile(inspectionService.fileName)
    print(inspectionService.filePath)

    inspectionService.ReadInspectionSheetExcel()
    if not systemServices.CheckIfFilePathExists(inspectionService.filePath):
        #if file path does not exist, then return a 404 code telling there is not file
        PostInspectionResponse = {
            "errorMessage": "No file found!",
            "responseMessage": None
        }
        return make_response(PostInspectionResponse, 404)

    inspectionSheetOpenPy.ReadInspectionSheet(inspectionService.filePath)
    inspectionSheetOpenPy.UpdateInspectionSheet(jsonPostedDict)

    inspection = InspectionsTable.query.filter_by(PartNumber=inspectionService.fileName).first()
    purchaseOrder = PurchaseOrdersTable.query.filter_by(PurchaseOrder=inspection.PurchaseOrder).first()

    purchaseOrderManagement = PurchaseOrderManagement(inspection.PurchaseOrder)
    purchaseOrderManagement.AddFileExtensionIfNecessary()
    purchaseOrderManagement.ReadInspectionSheetExcel()
    if purchaseOrderManagement.errorMessage is not None:
        raise ValueError( purchaseOrderManagement.errorMessage )

    purchaseOrderManagement.UpdateInspectionSheet(jsonPostedDict, purchaseOrder, inspection)

    #Update Database partNumber
    #PurchaseOrdersTable.query.filter_by(PurchaseOrder=purchaseOrderForm.purchaseOrderInput).first()
    inspection.ModifiedDate = datetime.datetime.today()
    inspection.Result = jsonPostedDict["BasicInformation"]["Resultado"]
    inspection.Comments = jsonPostedDict["BasicInformation"]["Comentarios"]
    inspection.ResponsableName = jsonPostedDict["BasicInformation"]["InspectedBy"]

    db.session.commit()

    return "veri gud"






