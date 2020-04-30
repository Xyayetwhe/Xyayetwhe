from spyre import server
import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plot
import matplotlib


class Lab2App(server.App):
    title = "Second Lab"

    inputs = [{
        "type": 'dropdown',
        "label": 'Choose the region',
        "options": [{"label": "Vinnitsya", "value": 1},
                    {"label": "Volyn'", "value": 2},
                    {"label": "Dnopropetrovs'k", "value": 3},
                    {"label": "Donets'k", "value": 4},
                    {"label": "Zhytomyr", "value": 5},
                    {"label": "Zacarpattya", "value": 6},
                    {"label": "Zaporyzhzhya", "value": 7},
                    {"label": "Ivano-Frankivs'k", "value": 8},
                    {"label": "Kyiv", "value": 9},
                    {"label": "Kirovohrad", "value": 10},
                    {"label": "Luhans'k", "value": 11},
                    {"label": "L'viv", "value": 12},
                    {"label": "Mikolyaiv", "value": 13},
                    {"label": "Odessa", "value": 14},
                    {"label": "Poltava", "value": 15},
                    {"label": "Rivne", "value": 16},
                    {"label": "Sumy", "value": 17},
                    {"label": "Ternopil'", "value": 18},
                    {"label": "Kharkiv", "value": 19},
                    {"label": "Kherson", "value": 20},
                    {"label": "Khmel'nyts'kyy", "value": 21},
                    {"label": "Cherkasy", "value": 22},
                    {"label": "Chernyvtsy", "value": 23},
                    {"label": "Chernihiv", "value": 24},
                    {"label": "Crimea", "value": 25}],
        "variable_name": 'region',
        "value": 1,
        "action_id": "update_data"
    }, {
        "type": 'dropdown',
        "label": 'Choose index',
        "options": [{"label": "VHI", "value": "VHI"},
                    {"label": "VCI", "value": "VCI"},
                    {"label": "TCI", "value": "TCI"}],
        "key": 'index',
        "action_id": "update_data"
    }
        , {
            "input_type": "text",
            "variable_name": "week1",
            "label": "Enter the first week",
            "value": 25,
            "key": 'week1',
            "action_id": "update_data"
        }, {
            "input_type": "text",
            "variable_name": "week2",
            "label": "Enter the last week",
            "value": 35,
            "key": 'week2',
            "action_id": "update_date"
        }, {
            "input_type": "text",
            "variable_name": "year1",
            "label": "Enter the year:",
            "value": 1982,
            "key": "year1",
            "action_id": "update_data"
        }
    ]

    controls = [
        {
            "type": "hidden",
            "id": "update_data"
        }
    ]

    outputs = [
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }, {
            "type": "plot",
            "id": "plot_id",
            "tab": "Plot",
            "control_id": "update_data"
        }, {
            "type": "table",
            "id": "table_one_id",
            "control_id": "update_data",
            "tab": "Table1",
            "on_page_load": True
        }, {
            "type": "plot",
            "id": "plot1_id",
            "control_id": "update_data",
            "tab": "Plot1",
            "on_page_load": True
        }

    ]

    tabs = ["Plot", "Table", "Plot1", "Table1"]

    def table_id(self, params):
        index = str(params['index'])
        week1 = int(params['week1'])
        week2 = int(params['week2'])
        region = int(params['region'])
        year1 = int(params['year1'])

        column = ['year', 'week', 'oblast', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
        df = pd.read_csv('final.csv', names=column)

        return df.loc[(df['week'] >= int(week1)) & (df['year'] == int(year1)) & (df['week'] <= int(week2)) & (
        df['oblast'] == int(region))]

    def table_one_id(self, params):
        column = ['year', 'week', 'oblast', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
        df1 = pd.read_csv('final.csv', names=column)

        df1.astype({'week': 'int32'}).dtypes
        df1.astype({'VHI': 'float'}).dtypes

        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        for i in range(12):
            if (months[i] % 3 == 0):
                months.extend(months[i:(i + 1)] * 4)
            else:
                months.extend(months[i:(i + 1) * 3])
        weeks = df1['week'].unique()

        all_min = []
        all_max = []

        for i in range(1, 53):
            vhi_min = df1[df1['week'] == i]['VHI'].min()
            vhi_max = df1[df1['week'] == i]['VHI'].max()

            all_min.append(vhi_min)
            all_max.append(vhi_max)

        print(all_min)

        d2 = {'month': months, 'vhi_min': all_min, 'vhi_max': all_max}
        df2 = pd.DataFrame(d2)
        df2 = df2.groupby(['month']).mean()
        print(df2)

        return df2

    def plot_id(self, params):
        index = params['index']
        df = self.table_id(params)

        plt_obj = df.plot(x='week', y=index,
                          linestyle='-',
                          linewidth=3,
                          color='pink'
                          )

        plt_obj.set_ylabel(index)
        fig = plt_obj.get_figure()
        return fig

    def plot1_id(self, params):
        index = params['index']
        df = self.table1_id(params)

        plt_obj = df.plot(x='years', y='vhi_min',
                          linestyle='-',
                          linewidth=3,
                          color='pink'
                          )

        plt_obj.set_ylabel(index)
        fig = plt_obj.get_figure()
        return fig


app = Lab2App()
app.launch()
