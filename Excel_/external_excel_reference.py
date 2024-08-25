import openpyxl


def load_excel_sheet(file_dir: str,sheet_name: str):
    excel_instance = openpyxl.load_workbook(file_dir)
    excel_sheet = excel_instance[sheet_name]
    return excel_sheet


def reference_excel_cell(excel_sheet: openpyxl, cell_row: str, cell_col: str):
    return excel_sheet[f"{cell_row}{cell_col}"].value


sheet = load_excel_sheet("./resource/NW_admin.xlsx","context1")

print(sheet)
print(reference_excel_cell(sheet, cell_row= "B", cell_col="5"))

