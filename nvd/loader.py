def xlsx2dict(file_name: str) -> dict:
    import openpyxl
    wb_obj = openpyxl.load_workbook(file_name)
    sheet = wb_obj.active
    data = []
    first = True
    column_title_list = []
    for row in sheet.iter_rows(max_row=5):
        col = []
        for cell in row:
            col.append(cell.value)
        if first:
            column_title_list = col
            first = False
            continue
        _data = {}
        for i in range(len(column_title_list)):
            _data[column_title_list[i]] = col[i]
        data.append(_data)
    return data
