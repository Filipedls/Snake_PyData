import numpy as np
import pandas as pd
import ast

def parse_and_preprocess_game_log(file_name):
    """
    Funtion that parses the game log .tsv file and converts all the strings to objects.
    This function also adds the column `time_to_apple`
    :param file_name: the name of the game log to open
    :return:
    """
    df = pd.read_csv(file_name, delimiter='|')
    # Converting the columns that contains lists from str to list()
    for c in ["snake_pos", "apple_pos" ,"snake_dir"]:
        df[c] = df[c].fillna("[]").apply(ast.literal_eval)
    # Once some values in the 'other' columns contains NaNs
    # We have to fill those with {}
    df['other'] = df['other'].fillna("{}").apply(ast.literal_eval)

    # Converting list type columns to np.array
    list_cols = df.columns[[type(v) == list for v in df.iloc[0]]]
    df[list_cols] = df[list_cols].applymap(np.array)

    # The time between two consecutive apples, in the same game
    # For the first apple is measured starting from the first key press
    df["time_to_apple"] = df.time_secs - df.time_secs.shift(1)
    df.loc[df.status == "start", "time_to_apple"] = 0

    return df
