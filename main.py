import json
import numpy as np
import pandas as pd


def open_json():
    with open('./datasests/treasure.json', 'r', encoding='utf8') as f:
        data = f.read()
    data = json.loads(data)
    return data['RECORDS']


def read_file():
    df = pd.read_csv('./datasests/医院网站收集-江苏.csv', index_col=None)
    return np.array(df).tolist()


def save_file(datas: dict):
    for name, data in datas.items():
        with open(f'./datasests/Procurement_{name}', 'a+') as f:
            f.write(json.dumps(data))


def run():
    datas = open_json()
    dfs: list = read_file()
    save = {}
    maps = {}
    for df in dfs:
        maps[df[1]] = df[0]
    for data in datas:
        if maps[data['hospital_name']] not in save:
            save[maps[data['hospital_name']]] = []

        save[maps[data['hospital_name']]].append(data)
    save_file(save)


if __name__ == '__main__':
    run()
