import os
import pandas as pd


def carregar_df(arquivo, dir):

    # carrega arquivo csv
    diretorio = os.path.dirname(__file__)
    diretorio = os.path.join(diretorio, dir)
    file = arquivo + ".csv"
    df = pd.read_csv(os.path.join(diretorio, file), ",")

    return df
