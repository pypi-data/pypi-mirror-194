import os

from a_pandas_ex_horizontal_explode import horizontal_explode
from normalize_lists import normalize_lists
import pandas as pd


def rf(file_or_string, sep="\t", encoding="utf-8"):

    if os.path.exists(file_or_string):
        with open(file_or_string, encoding=encoding) as f:
            data = f.read()
    else:
        data = file_or_string
    df = pd.concat(
        [
            pd.Series(p)
            for p in normalize_lists([x.split(sep) for x in data.splitlines()])
        ]
    )
    df = horizontal_explode(df.to_frame(), 0, False).reset_index(drop=True)
    return df


def pd_add_read_charsep_frames():
    pd.Q_read_charsep_frames = rf

