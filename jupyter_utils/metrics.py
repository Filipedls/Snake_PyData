import shapely
from shapely.geometry import LineString, Point
import numpy as np
import math
from snake_game.config import SCR_SZ


def get_num_of_snake_intersections(snake_pos, apple_pos):
    """
    Computes the number of intersection with the sanke (explained in the notebook)
    :param snake_pos: array with the locations of each snake's square
    :param apple_pos: the position of the apple [x, y]
    :return: int with the number intersections
    """
    if len(snake_pos) < 2:
        line2 = Point(snake_pos[0])
    else:
        line2 = LineString(snake_pos)
    line1 = LineString([tuple(apple_pos), tuple(snake_pos[0])])

    int_pt = line1.intersection(line2)
    if type(int_pt) == Point:
        int_pt = [int_pt]
    elif type(int_pt) == LineString:
        return -1
    int_pt = [p for p in int_pt if p != Point(snake_pos[0])]
    return len(int_pt)


# Number of apple sides than have snake in front of them
def check_snake_around_apple(sn_pos, ap_pos):
    if len(sn_pos) < 2:
        return np.array(4 * [False])

    ap_x_line_points = [(ssx, ap_pos[1]) for ssx in [0, SCR_SZ[0]]] + [(ap_pos[0], ssy) for ssy in [0, SCR_SZ[1]]]

    ap_has_snake_sides = []  # L,R,U,D
    for ap_line in ap_x_line_points:
        line1 = LineString([tuple(ap_pos), ap_line])
        line2 = LineString(sn_pos)

        int_pt = line1.intersection(line2)
        ap_has_snake_sides.append(not int_pt.is_empty)

    return np.array(ap_has_snake_sides)


def compute_distance(p1, p2):
    """
    Computes the distance between 2 points
    :param p1: point 1 [x, y]
    :param p2: point 2 [x, y]
    :return: distance (float)
    """
    if p1.shape != p2.shape:
        raise Exception("p1 and p2 have different shapes!")
    return np.sqrt(np.sum(np.square(p1-p2), axis=len(p1.shape)-1))


def get_angle(p0, p1):
    """
    Computes the angle of a vector from p0 to p1 (0-360)
    :param p0:
    :param p1:
    :return:
    """
    return math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0])) % 360  # %360 > 0-360 conv


def compute_all_metrics(metrics_df, apple_pos_col_name="apple_pos"):
    """
    Computes all the metrics used in the notebook
    :param metrics_df:
    :param apple_pos_col_name:
    :return:
    """

    metrics_df["head_pos"] = metrics_df.snake_pos.apply(lambda p: p[0])
    metrics_df["apple_dist"] = metrics_df.apply(
        lambda r: compute_distance(r[apple_pos_col_name] ,r["head_pos"]), axis=1
    )
    # snake_dir_to_apple_angle
    snakes_head_angles = metrics_df.apply(lambda r :get_angle([0 , 0], r["snake_dir"]), axis=1)
    head_to_apples_angles = metrics_df.apply(lambda r :get_angle(r["head_pos"], r[apple_pos_col_name]), axis=1)
    snake_dir_to_apple_angle = (head_to_apples_angles - snakes_head_angles ) %360
    # Computing the module of the angle
    metrics_df["snake_dir_to_apple_angle"] = 180 - (180 - snake_dir_to_apple_angle).abs()
    # num_intersections_w_snake
    metrics_df["num_intersections_w_snake"] = \
        metrics_df[metrics_df.score != 0].apply \
            (lambda r: get_num_of_snake_intersections(r["snake_pos"], r[apple_pos_col_name]), axis=1)
    metrics_df["num_intersections_w_snake"] = metrics_df["num_intersections_w_snake"].fillna(0)

    # the number of sides of the apple that have the snake in front of them
    apple_sides_with_snake = \
        metrics_df.apply(lambda r: check_snake_around_apple(r["snake_pos"], r[apple_pos_col_name]), axis=1)

    metrics_df["num_apple_sides_w_snake"] = apple_sides_with_snake.apply(np.sum)

    return metrics_df.drop(columns="head_pos")


def get_n_highest_rows(df, col_name, n=3):
    high_time_idxs = df[col_name].sort_values(ascending=False).index[:n]
    return df.loc[high_time_idxs]
