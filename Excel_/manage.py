from Excel_ import external_excel_reference,create_nw_config

if __name__ == '__main__':
    sheet = external_excel_reference.load_excel_sheet("./resource/NW_admin.xlsx", "context1")

    print(
        create_nw_config.create_cisco_config(
            port_number=external_excel_reference.reference_excel_cell(sheet, cell_row="B", cell_col="5"),
            vlan=external_excel_reference.reference_excel_cell(sheet, cell_row="C", cell_col="5"),
            ip_address=external_excel_reference.reference_excel_cell(sheet, cell_row="D", cell_col="5"),
            subnet_mask=external_excel_reference.reference_excel_cell(sheet, cell_row="E", cell_col="5"),
            description=external_excel_reference.reference_excel_cell(sheet, cell_row="F", cell_col="5")
        )
    )
