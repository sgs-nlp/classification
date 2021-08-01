import openpyxl
from .models import add_news, add_category, add_word, add_stopword, add_reference
from nvd.pre_processing import normilizer


def xlsx2dict2db(file_name: str, reference_id: int) -> dict:
    wb_obj = openpyxl.load_workbook(file_name)
    sheet = wb_obj.active
    first = True
    column_title_list = []
    for row in sheet.iter_rows(max_row=10):
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

        titr_string = normilizer(_data['Titr'])
        content_string = normilizer(_data['Content'])
        add_news(
            titr_string=titr_string,
            content_string=content_string,
            # todo tedade query hara payin biyar
            category_id=add_category(_data['Category'], reference_id),
            reference_id=reference_id,
        )
