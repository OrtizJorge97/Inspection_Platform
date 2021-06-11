class PurchaseOrderFormConstants:
        purchaseOrderInput = "purchaseOrderInput"
        statusInput = "statusInput"
        quantityInput = "quantityInput"
        requestDateInput = "requestDateInput"
        startDateInput = "startDateInput"
        endDateInput = "endDateInput"

        importedFileType = "IMPORTED"
        nativeFileType = "NATIVE"

        purchaseOrderLate = "LATE" #used for indicating if purchase order already passed its deadline
        purchaseOrderInTime = "IN TIME" #used for indicating if purchase order already passed its deadline

        IN_PROGRESS_STATUS = "In Progress"
        FINISHED_STATUS = "Finished"

class PurchaseOrderServerSideConstants:
    purchaseOrderFolderParent = "PurchaseOrderFiles"

class ImportPurchaseOrderFormConstants:
        purchaseOrderFileInput = "purchaseOrderFileInput"
        dateFormat = "%y/%m/%d"

