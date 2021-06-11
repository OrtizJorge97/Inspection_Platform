#Third Party Modules
import pandas as pd
import numpy as np



class PandasHelpers:

    @staticmethod
    def MapExcelHubToApp(excelPandas):
        generalData = PandasHelpers().AnalyzeGeneralData(excelPandas.copy(), len(excelPandas), len(excelPandas.columns))
        tableData = PandasHelpers().AnalyzeTableData(excelPandas.copy(), len(excelPandas), len(excelPandas.columns))

        return None

    @staticmethod
    def AnalyzeGeneralData(excelPandas, totalRows, totalCols):
        generalDictionary = {}
        generalDictionary["Organization"] = excelPandas.iloc[1, 2]
        generalDictionary["Supplier/Vendor_Code"] = excelPandas.iloc[2, 2]
        generalDictionary["Inspection_Facility"] = excelPandas.iloc[4, 0]

        generalDictionary["Part_Number"] = excelPandas.iloc[1, 9]
        generalDictionary["Part_Name"] = excelPandas.iloc[2, 9]
        generalDictionary["Design_Record_Change_Level"] = excelPandas.iloc[3, 10]
        generalDictionary["Engineering_Change_Documents"] = excelPandas.iloc[4, 10]

        #print(excelPandas)
        #print(f"Total Rows: {totalRows}")
        #print(f"Total Cols: {totalCols}")
        #print(f"Dictionary:\n{generalDictionary}")

    @staticmethod
    def AnalyzeTableData(excelPandas, totalRows, totalCols):
        rawHeaders = list(excelPandas.iloc[6, 0:]) #6 is the beginning of the row which is the header.
        pandasSeries = pd.Series(rawHeaders,
                                index = np.arange(len(rawHeaders)))
        rowStart = 7
        tableRows = len(excelPandas.iloc[rowStart:, :])

        #print(tableRows)
        #print( type(pandasSeries) )
        #print(pandasSeries)
        #print(pandasSeries.isnull())
        #print(pandasSeries[pandasSeries.isnull()].index) #prints an array of index which indicates which one is null
        for header in pandasSeries[pandasSeries.isnull()].index:
            pandasSeries[header] = pandasSeries[header-1]

        tableDataFrame = pd.DataFrame(columns=pandasSeries,
                                      index=np.arange(tableRows))
        #print(tableDataFrame)
        columnsIndexArray = np.arange(totalCols)

        #tableDataFrame = excelPandas.iloc[rowStart:, :] #ESTO NO SIRVE!!!
        for columIndex in columnsIndexArray:
            tableDataFrame.iloc[0:, columIndex] = excelPandas.iloc[rowStart:, columIndex]
            #print(f"this header is: {header}")
            #recorrer cada columna del datafrmae

            #en cada columna voy a agarrar desde donde empiezan los datos y todo hasta abajo
            #y ponerla en la columna que este ahorita mismo


        print(f"Excel dataframe:\n{excelPandas.iloc[rowStart:, 0:2]}")
        print(f"My own dataframe:\n{tableDataFrame.iloc[:, 0:2]}")

        #print(excelPandas)
        #print(tableHeaders)
        #print(f"Total Rows: {totalRows}")
        #print(f"Total Cols: {totalCols}")


"""
def AddColumnToList(dataFromApp, column, rowName, columnValues):
    valueCell = dataFromApp[column][rowName]
    columnValues.append(valueCell)

    return columnValues

def GetCommand(column, rowName):
    command = ""
    if column == "generalInformation" and rowName != "PartNumber":
        command = "Insert General Column"
    if column == "actionColumn" and rowName != "PartNumber":
        command = "Insert Action Column"
    if column == "dateColumn" and rowName != "PartNumber":
        command = "Insert Date Column"
    if column == "inspectionColumn" and rowName != "PartNumber":
        command = "Insert Inspection Column"
    if column == "performedByColumn" and rowName != "PartNumber":
        command = "Insert PerformedBy Column"
    if column == "quantityColumn" and rowName != "PartNumber":
        command = "Insert Quantity Column"
    if column == "resultColumn" and rowName != "PartNumber":
        command = "Insert Result Column"
    if column == "toolColumn" and rowName != "PartNumber":
        command = "Insert Tool Column"

    return command

def UpdateColumnInformationDataFrame(command, dataFrameColumnInformation, dataFrameGeneralInfo, columnValues):
    if command == "Insert General Column":
        dataFrameGeneralInfo.GeneralInformation = columnValues
        print(columnValues)
    if command == "Insert Action Column":
        dataFrameColumnInformation.Action = columnValues
        print(columnValues)
    if command == "Insert Date Column":
        dataFrameColumnInformation.Date = columnValues
        print(columnValues)
    if command == "Insert Inspection Column":
        dataFrameColumnInformation.Inspection = columnValues
        print(columnValues)
    if command == "Insert PerformedBy Column":
        dataFrameColumnInformation.PerformedBy = columnValues
        print(columnValues)
    if command == "Insert Quantity Column":
        dataFrameColumnInformation.Quantity = columnValues
        print(columnValues)
    if command == "Insert Result Column":
        dataFrameColumnInformation.Result = columnValues
        print(columnValues)
    if command == "Insert Tool Column":
        dataFrameColumnInformation.Tool = columnValues
        print(columnValues)

    return dataFrameColumnInformation, dataFrameGeneralInfo

def SaveDataFromAppInExcelSheet(partNumber, dataFrameColumnInformation, dataFrameGeneralInfo):
    result = False
    print(f"\nPartNumber: {partNumber}")
    excelPandas = pd.read_excel('./Documents/SheetOne/INSPECC-02-604-ATest.xlsx',
                         sheet_name='Sheet1')

    sheetFromExcel = SheetFromExcelClass(excelPandas)
    sheetFromExcel.Map_FromDataFromApp_To_SheetFromExcel(dataFrameGeneralInfo,
                                                         dataFrameColumnInformation)

    WriteIntoSheetOneExcel(sheetFromExcel.excelSheetOne)


    return result

def WriteIntoSheetOneExcel(sheetOneDataForExcel):
    pass

"""