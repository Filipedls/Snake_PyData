import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from snake_game.config import SCR_SZ


# Plots the snake and apple/s
def plot_snake(df, SCR_SZ=SCR_SZ, apple_cols=["prev_apple_pos", "apple_pos"]):
    """
    (This feature is also used to copare the model's prediction with the ground true)
    :param df: DataFrame with "snake_pos" and the columns set in the 'apple_cols' variable
    :param SCR_SZ: the size of the screen during the game
    :param apple_cols: the columns where the apples to plot are in
    :return:
    """
    # The size of each square, both for the sanke and apples
    square_size = [31, 31]

    # The start status just represents to beginning of a game and not an apple placement, so we need to filter those
    df = df[df["status"] != "start"]

    # Creates a subplot with a max of 3 columns and the necessary rows to represent all the rows in df
    splots_size = (int(np.ceil(df.shape[0] / 3)), min(df.shape[0], 3))
    fig, axs = plt.subplots(splots_size[0], splots_size[1], figsize=np.array(splots_size)[::-1] * 7, squeeze=False)

    for ax, row in zip(axs.flatten(), df.iterrows()):

        snake_pos = np.array(row[1]["snake_pos"])

        apple_pos = [v for v in row[1][apple_cols].dropna().values if len(v)]
        apple_pos = np.stack(apple_pos) if len(apple_pos) else np.array([])
        ax.set(xlim=[0, SCR_SZ[0]], ylim=[SCR_SZ[1], 0], facecolor='lightgrey',
               xlabel='x', ylabel='y', title=f"Loc: {row[0]} - Size:{len(snake_pos)}")

        # Loop over all the squares, for the snake and apples
        boxes = []
        for x, y in np.concatenate([snake_pos, apple_pos]):
            rect = Rectangle((x, y), square_size[0], square_size[1])
            boxes.append(rect)
        # Create patch collection with specified colour/alpha
        pc = PatchCollection(boxes, facecolor=['darkgreen'] + (snake_pos.shape[0] - 1) * ['g'] + apple_pos.shape[0] * ['r'],
                             alpha=0.8, edgecolor='k')
        # Add collection to axes
        ax.add_collection(pc)

        # numerates the apples
        if len(apple_pos) != 1:
            for i, ap in enumerate(apple_pos):
                ax.text(ap[0] + square_size[0] / 3, ap[1] + square_size[1] / 1.5, str(i), fontsize="x-large")



