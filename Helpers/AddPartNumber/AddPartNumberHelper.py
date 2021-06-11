import pandas as pd
from itertools import islice

class AddPartNumberHelpers:

    @staticmethod
    def TrimmSpaces(partNumberForm):
        partNumberForm.purchaseOrderBelong = partNumberForm.purchaseOrderBelong.replace(" ", "")
        return partNumberForm

    @staticmethod
    def ValidateForm(partNumberForm):
        isValid = True
        print(f"purchase order: {partNumberForm.purchaseOrderBelong} | file value: {partNumberForm.file} | file name: {partNumberForm.fileName}")
        if partNumberForm.purchaseOrderBelong is None or partNumberForm.file is None:
           isValid = False

        return isValid

def PreprocessToMainDataFrame(data, cols):
    df = pd.DataFrame(data=[cols], columns=None)
    #print(df)
    data = list(data)

    # idx = [r[0] for r in data]
    # print(idx)
    data = (islice(r, 0, None) for r in data)
    df2 = pd.DataFrame(data, columns=None)

    mainDataFrame = df.append(df2, ignore_index=True)

    return mainDataFrame