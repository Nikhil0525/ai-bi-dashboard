import pandas as pd

df = pd.read_csv("data/dataset.csv")

def run_ai_query(question):

    q = question.lower()

    if "region" in q:
        return df.groupby("region")["sales_amount"].sum().reset_index()

    elif "product" in q:
        return df.groupby("product")["sales_amount"].sum().reset_index()

    elif "category" in q:
        return df.groupby("category")["sales_amount"].sum().reset_index()

    elif "top sales" in q:
        return df.sort_values("sales_amount", ascending=False).head(5)

    else:
        return df.head(10)