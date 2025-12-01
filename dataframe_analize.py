import pandas as pd
def read_df(filename):
    df = pd.read_csv(filename)
    return df

def request(df, query):
    result = df.query(query)
    return result

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
        return  f"Most likely datatype error: {e}"