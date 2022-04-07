from __future__ import annotations
from tabulate import tabulate
import json


class DataFrame:
    def __init__(self, data={}) -> None:
        self.data = data
        if DataFrame.is_valid(self.data) is False:
            raise ValueError("Data is not valid")

    @property
    def columns(self) -> list:
        return list(self.data.keys())

    @columns.setter
    def columns(self, newColumns: list) -> None:
        result = {}
        for (old_col, new_col) in list(zip(self.columns, newColumns)):
            result[new_col] = self.data[old_col]
        self.data = result

    def get_column(self, column: str) -> list:
        return self.data.get(column)

    def get_row(self, num: int) -> dict:
        result = {}
        for col in self.columns:
            result[col] = self.data[col][num]
        return result

    def copy(self) -> DataFrame:
        return DataFrame(self.data.copy())

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return tabulate(self.data, headers=self.columns)

    def __len__(self) -> int:
        return len(self.data[self.columns[0]]) if len(self.data) > 0 else 0

    def __getitem__(self, column: str) -> None:
        return self.data[column]

    def __setitem__(self, column: str, values: list) -> None:
        self.data[column] = values
        self.columns = list(self.data.keys())

    def __iter__(self) -> iter:
        # for col in self.columns:
        #     yield col
        return iter(self.columns)

    def __add__(self, df: DataFrame) -> DataFrame:
        result = {}
        for key in self.data.keys():
            type_key_df1 = type(self.data[key][0])
            type_key_df2 = type(df.data[key][0])
            if type_key_df1 == type_key_df2:
                result[key] = self.data[key] + df.data[key]
            else:
                raise ValueError("Error")
        return DataFrame(result)

    def to_json(self, filenPath: str) -> None:
        try:
            with open(filenPath, "w") as f:
                f.write(json.dumps(self.data))
        except Exception as e:
            print("Error " + str(e))

    @classmethod
    def read_json(cls, filePath: str) -> DataFrame:
        try:
            with open(filePath, "r") as f:
                data = json.load(f)
            f.close()
            return DataFrame(data)
        except (FileNotFoundError, ValueError) as e:
            print("Error" + str(e))

    @staticmethod
    def is_valid(data_dict) -> bool:
        if isinstance(data_dict, dict) is False:
            result = False
        else:
            cols = list(data_dict.keys())
            if len(cols) == 0:
                result = False
            else:
                for col in cols:
                    values = data_dict[col]
                    if isinstance(values, list) is False:
                        result = False
                    else:
                        if len(values) != len(data_dict[cols[0]]):
                            result = False
                        else:
                            for value1 in values:
                                for value2 in values:
                                    if type(value1) is not type(value2):
                                        result = False
                                else:
                                    result = True
        return result


if __name__ == "__main__":
    print("on est sur le dataframe fichier")
    data = {
        "prenoms": ["toto", "tata", "Paul"],
        "age": [10, 20, 30],
        "pays": ["france", "Angleterre", "Espagne"],
    }
    df1 = DataFrame(data)
    for i in df1:
        print(i)

    df2 = df1.copy()

    sumdf = df1 + df2

    df3 = DataFrame.read_json("/home/fitec/Documents/folder_class/artist.json")
    print("finish")
