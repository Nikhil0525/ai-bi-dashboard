from sqlalchemy import create_engine
import pandas as pd
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def run_query(query):

    df = pd.read_sql(query, engine)

    return df