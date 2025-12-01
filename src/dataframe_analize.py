import pandas as pd
import numpy as np
def read_df(filename):
    df = pd.read_csv(filename)
    return df

def groupby(df, func, targer_column, other_columns, sort_type, sort_by):
    ascending = True

    if sort_type == ':.': 
        ascending = False         

    print(sort_by)

    columns = other_columns
    if len(other_columns) == 1:
        columns = other_columns[0]

    match func:
        case "values":
            return df.groupby(targer_column)[columns].value_counts() if sort_type == ":.:" else df.groupby(targer_column)[columns].value_counts().sort_values(ascending=ascending, by=sort_by)
        case "groupby::mean":
            return df.groupby(targer_column)[columns].mean() if sort_type == ":.:" else df.groupby(targer_column)[columns].mean().sort_values(ascending=ascending, by=sort_by)
        case "values-normalize":
            return df.groupby(targer_column)[columns].value_counts(normalize=True) if sort_type == ":.:" else df.groupby(targer_column)[columns].value_counts(normalize=True).sort_values(ascending=ascending, by=sort_by)
        case "groupby::std":
            return df.groupby(targer_column)[columns].std() if sort_type == ":.:" else df.groupby(targer_column)[columns].std().sort_values(ascending=ascending, by=sort_by)
        case "groupby::var":
            return df.groupby(targer_column)[columns].var() if sort_type == ":.:" else df.groupby(targer_column)[columns].var().sort_values(ascending=ascending, by=sort_by)
        case _:
            return "Select another agg function"
        
        
def request(df, query):
    result = df.query(query)
    return result

def corr(df, columns=None):
    if not columns:
        columns = df.select_dtypes(include=[np.number])
        return columns.corr()
    return df[columns].corr()


def metrica(name, df, column, mode_count):
    try:
        funcs = {
            "values": df[column].value_counts,
            "values-normalize": df[column].value_counts,
            "sort.:": df[column].sort_values,
            "sort:.": df[column].sort_values,
            "unique": df[column].nunique,
            "isna": df[column].isna,
            "duplicated": df[column].duplicated,
            "sum": df[column].sum,
            "mean": df[column].mean,
            "median": df[column].median,
            "mode": df[column].mode,
            "min": df[column].min,
            "max": df[column].max,
            "describe": df[column].describe,
            "std": df[column].std,
            "var": df[column].var,
            "skew": df[column].skew,
            "kurt": df[column].kurt,
        }

        result = funcs.get(name)

        if result:
            if name in ["isna","duplicated"]:
                return result().sum()
            if name[:4] == "sort":
                if name == "sort:.":
                    return result().sort_values(ascending=False)
                elif name == "sort.:":
                    return result().sort_values(ascending=True)
            if name == "values-normalize":
                return result(normalize=True)
            if name == "mode":
                mode_result = result()
                if len(mode_result) == 0:
                    return "No mode found"
                return mode_result[:mode_count]
            return result()

        return "use only int/float columns"

    except Exception as e:
        return  f"Most likely datatype error:"