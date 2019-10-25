from django.shortcuts import render
import json


def test():
    j_data = json.load(open('admitat/top_cupons.json', 'r', encoding='UTF-8'))
    for data in j_data:
        return data


def index(request):
    work = test()
    workin = {
        "work": work
    }
    return render(request, 'procup/index.html', workin)
