import datetime
from DeltaHubRestApi.Constants.AddPurchaseOrderConstants import PurchaseOrderFormConstants
from DeltaHubRestApi.modelsdb import *

class PurchaseOrderStatusManagement:
    def __init__(self):
        self.__todayDate = datetime.date.today()
        self.__dateFormat = "%Y-%m-%d"

    def ManagePurchaseOrderStatusTime(self, purchaseOrders, db):
        for purchaseOrder in purchaseOrders:
            purchaseOrderEndDate = datetime.datetime.strptime(purchaseOrder.EndDate, self.__dateFormat).date()
            #IF today's date is greater than end date of purchase order and de status of document is in progress
            if self.__todayDate > purchaseOrderEndDate and purchaseOrder.Status == PurchaseOrderFormConstants.IN_PROGRESS_STATUS:
                purchaseOrder.StatusTime = PurchaseOrderFormConstants.purchaseOrderLate
            else:
                purchaseOrder.StatusTime = PurchaseOrderFormConstants.purchaseOrderInTime

        db.session.commit()
        purchaseOrders = PurchaseOrdersTable.query.all()

        return purchaseOrders