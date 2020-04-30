import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import datetime
import os
provinces = {1: "Вінницька", 13: "Миколаївська", 2: "Волинська", 14: "Одеська", 3: "Дніпропетровська", 15: "Полтавська",
             4: "Донецька", 16: "Рівенська", 5: "Житомирська", 17: 'Сумська', 6: "Закарпатська", 18: "Тернопільська",
             7: "Запорізька", 19: "Харківська",
             8: "Івано-Франківська", 20: "Херсонська", 9: "Київська", 21: "Хмельницька", 10: "Кіровоградська",
             22: "Черкаська", 11: "Луганська", 23: "Чернівецька",
             12: "Львівська", 24: "Чернігівська", 25: "Республіка Крим"}
correct_oblasti = {}

def get_url(url):
    page = BeautifulSoup(requests.get(url).content.decode("utf8"),'html.parser')
    key = re.findall(r'\d+', str(page))[0]
    value = str(page).split(",")[0].split(" ")[-1]
    data = str(page.find('pre').contents[0])
    return "{}:{}\n{}".format(key,value,data)

def datafile(oblast, when):
    global parse_from
    global parse_to
    parse_from,parse_to = when
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1={}&year2={}&type=Mean".format(oblast,parse_from,parse_to)

    now = datetime.datetime.now()
    filename = str(oblast) + "_" + 'Mean' + "_" + parse_from + "-" + parse_to + '.txt'
    if not os.path.isfile(filename):
        print("качаем")
        resp = get_url(url)
        open(filename, 'wb').write(str.encode(resp))
        print(filename, " created.")
    return filename


def choose_province():
    from_to = input('С какого по какой год ищем?: ').split()
    for every in dict.keys(provinces):
        datafile(every, from_to)




def replace_index(files):



    for file in files:
        if '.txt' in file:
            raw = open(file, 'r')
            index_oblast,oblast = raw.readline().split(":")
            provinces[int(index_oblast)] = oblast[:-1]
    for every in dict.keys(provinces):
        print(every, " <=> ", provinces[every])

def prepare_df(file):
    raw = open(file, 'r')
    index_oblast,oblast = raw.readline().split(":")
    data = raw.readlines()
    replace = lambda dat: str(re.sub(r',\s\s|\s\s|\s|,\s', ',', dat)[:-1]).split(',')
    data = list(map(replace,data))
    df = pd.DataFrame(data,columns=['year','week','SMN','SMT','VCI','TCI','VHI'])
    df.iloc[:,0:2] = df.iloc[:,0:2].applymap(int)
    df.loc[:,'SMN':'VHI'] = df.loc[:,'SMN':'VHI'].applymap(float)
    df['oblast'] = oblast[:-1]
    df['index_oblast'] = int(index_oblast)
    return df


def max_and_min(df):

    df_max_and_min = df[['year','VHI']].groupby(['year']).agg(['max','min'])


    print(df_max_and_min)

def extreme_drought(df):
    print(df.loc[df.VHI < 15, :])
    amount_of_droughts = df.loc[df.VHI < 15, :].shape[0]
    amount_of_data = df.shape[0]
    print("present of extreme droughts is: {}".format((amount_of_droughts/amount_of_data)*100))

def mild_drought(df):
    print(df.loc[(df.VHI < 35) & (df.VHI > 15), :])
    amount_of_droughts = df.loc[(df.VHI < 35) & (df.VHI > 15), :].shape[0]
    amount_of_data = df.shape[0]
    print("present of mild droudhst is: {}".format((amount_of_droughts / amount_of_data) * 100))

choose_province()
files = os.listdir()
replace_index(files)
df_list = [prepare_df(file) for file in files if parse_from + "-" + parse_to + '.txt' in file]
ukraine_df = pd.concat(df_list)
max_and_min(ukraine_df)


# print("###### EXTREME DROUGHTS ##########")
# extreme_drought(ukraine_df)
# print("\n"*4)
# print("###### MILD DROUGHTS ##########")
# mild_drought(ukraine_df)
# print("\n"*4)


