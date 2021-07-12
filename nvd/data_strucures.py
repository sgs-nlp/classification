def data2pandas_data_frame(data: list):
    import pandas
    _data = []
    for itm in data:
        data.append({'data': f'{itm.titr_string_code} {itm.content_string_code}', 'flag': itm.category.title_code})
    data = pandas.DataFrame(data, columns=['data', 'flag'])
    return data
