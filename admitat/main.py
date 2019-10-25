from admitad import api, items
import json
from time import sleep


def get_client(scope):
    cred_json = json.load(open(r'C:\cred\cred.json', 'r', encoding='UTF-8'))
    client_id = cred_json['client_id']
    client_secret = cred_json['client_secret']
    scope = ''.join(set([scope]))

    client = api.get_oauth_client_client(
        client_id,
        client_secret,
        scope
    )
    return client

def write_json(data, filename):
    json_file = filename + '.json'
    with open(json_file, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def get_data(data):
    data_cup = {
        "advcampaign_id": data["campaign"]["id"],
        "name": data["short_name"],
        "site": data["campaign"]["site_url"],
        "rating": data["rating"],
        "advcampaign_name": data["campaign"]["name"],
        "logo": data["image"],
        "description": data["description"],
        "species": data["species"],
        "promocode": data["promocode"],
        "promolink": data["frameset_link"],
        "gotolink": data["goto_link"],
        "date_start": data["date_start"],
        "date_end": data["date_end"],
        "exclusive": data["exclusive"],
        "types": data["types"],
        "categories": data["categories"],
        "discount": data["discount"]
        }

    return data_cup


def get_all_CouponsForWebsite(offset=0):
    client = get_client('coupons_for_website')
    return client.CouponsForWebsite.get(1155537, limit=500, offset=offset)


def cupons():
    cupons_count = get_all_CouponsForWebsite()["_meta"]["count"]
    offset = 0
    all_cupons = []
    while True:
        all_cupons.extend(get_all_CouponsForWebsite(offset=offset)["results"])
        offset += 500
        if cupons_count < offset:
            break

    data_cupon = []
    for cupon in all_cupons:
        if cupon["regions"][0] == "RU":
            data_cupon.append(get_data(cupon))
#    print(data_cupon)
#    write_json(data_cupon, 'cupons')
    return data_cupon

def top_raiting():
    json_data = json.load(open('cupons.json', 'r', encoding='UTF-8'))
    types = []
    for type in json_data:
        if type["types"][0]["id"] == 2:
            types.append(type)
    cup_raiting = []
    for cup in types:
        cup_raiting.append(cup['rating'])
    raiting_top_20 = sorted(cup_raiting)[-20:]
    top_cupons = []
    for data_cup in json_data:
        if float(data_cup['rating']) >= float(raiting_top_20[0]):
            db_dict = {
                'rating':data_cup['rating'],
                "advcampaign_name":data_cup["advcampaign_name"],
                "discount":data_cup["discount"],
                "logo":data_cup["logo"]
                }
            top_cupons.append(db_dict)
#    return top_cupons
    write_json(top_cupons, 'top_cupons')

def main():
    pass
if __name__ == '__main__':
    main()
