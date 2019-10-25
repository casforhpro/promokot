import xlrd
import json

def xlsx_convert_json():
    excel_data_file = xlrd.open_workbook('admitad_coupons.xlsx')
    sheet = excel_data_file.sheet_by_index(0)

    batch_Names_wanted = []
    row_number = sheet.nrows

    for row in range(0, row_number):
        one_row = []
        for one in sheet.row(row):
            one_row.append(str(one).replace("https", "").replace("http", "").replace("text:", "").replace("\"", "").replace("number:", "").replace("'", "").replace(":", "").replace(",", "").replace("\\r\\n", "")) #
        batch_Names_wanted.append(one_row)

    full_dict_list = []
    for bach_text in batch_Names_wanted[1:]:
        i = 0
        str_data = {}
        for batch_key in batch_Names_wanted[0]:
            data = {batch_key: bach_text[i]}
            str_data.update(data)
            i += 1
        full_dict_list.append(str_data)

    with open('full_dict.json', 'w', encoding='UTF-8') as fd:
        json.dump(full_dict_list, fd, indent=2, ensure_ascii=False)

def top_raiting():
    json_data = json.load(open('full_dict.json', 'r', encoding='UTF-8'))
    cup_raiting = []
    for cup in json_data:
        cup_raiting.append(cup['rating'])
    raiting_top_20 = sorted(cup_raiting)[-20:]
    top_cupons = []
    for data_cup in json_data:
        if float(data_cup['rating']) >= float(raiting_top_20[0]):
            db_dict = {
                "types":data_cup["types"],
                "discount":data_cup["discount"],
                "logo":'https:' + data_cup["logo"]
            }
            top_cupons.append(db_dict)
    return top_cupons
#    with open('not_null.json', 'w', encoding='UTF-8') as fd:
#        json.dump(top_cupons, fd, indent=2, ensure_ascii=False)

def dostvka_free():
    json_data = json.load(open('full_dict.json', 'r', encoding='UTF-8'))
    free_dostavka = []
    for cup in json_data:
        if cup["types"] == 'Бесплатная доставка':
            free_dostavka.append(cup)
    print(len(free_dostavka))

xlsx_convert_json()
top_raiting()
