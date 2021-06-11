class AddPartNumberHelpers:

    @staticmethod
    def TrimmSpaces(partNumberForm):
        partNumberForm.purchaseOrderBelong = partNumberForm.purchaseOrderBelong.replace(" ", "")
        return partNumberForm

    @staticmethod
    def ValidateForm(partNumberForm):
        isValid = True
        print(f"purchase order: {partNumberForm.purchaseOrderBelong} | file value: {partNumberForm.file} | file name: {partNumberForm.fileName}")
        if not partNumberForm.purchaseOrderBelong or not partNumberForm.file:
           isValid = False

        return isValid

