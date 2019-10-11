import numpy as np

# Postion features
def position_norm(snake_pos, n_points):
    """
    Funtion that normalizes the snake's location array to 'n_points'
    :param snake_pos: array with the locations of each snake's square
    :param n_points: number of points of the output array
    :return: array with n_points [[x0, y0], [x1, y1], ...]
    """
    if len(snake_pos) == 1:
        return np.array([tuple(snake_pos[0])] * n_points)

    x = snake_pos[: , 0]
    y = snake_pos[: , 1]
    ar_len = len(x)

    x_interp, y_interp = map(lambda a: np.interp(np.linspace(0, ar_len-1, n_points), np.arange(0, ar_len), a) , [x, y])
    return np.stack([x_interp, y_interp], axis=1)


def get_position_stats(snake_pos, stat_funcs):
    """
    Funtion that computes statistics of the snakes position.
    :param snake_pos: array with the locations of each snake's square
    :param stat_funcs: a list with the function to compute
    :return: an array with the all the stats for x and y [x_for_func_0, y_for_func_0, ...]
    """
    return np.concatenate([func(snake_pos, axis=0) for func in stat_funcs])


def get_dir_str(snake_dir):
    """
    Return the direction of the snake as a one letter string.
    R (right), L (left), D (down), U (up) or S (stop)
    :param snake_dir: snake's direction array [x_dir, y_dir]
    :return:
    """
    if snake_dir[0] > 0:
        return "R"
    elif snake_dir[0] < 0:
        return "L"
    elif snake_dir[1] > 0:
        return "D"
    elif snake_dir[1] < 0:
        return "U"
    else:
        return "S"

# Config of the statistics to compute
stats_config = {
    "min": np.min,
    "max": np.max,
    "avg": np.mean
}

def compute_all_feats(snake_pos, snake_dir, game_score, return_names=False, stats_config=stats_config):
    """
    Computes all the features
    :param snake_pos: array with the locations of each snake's square
    :param snake_dir: snake's direction array [x_dir, y_dir]
    :param game_score: the score of the game when the apple is placed
    :param return_names: flag to also return the feature name
    :param stats_config: a dict with the names as key and the stats funtions as values
    :return: if 'return_names' is False: a list of features; else a dict with names as keys and features as values
    """
    snake_pos = np.array(snake_pos)

    # Normalized position
    n_points = 5
    norm_snake_pos = position_norm(snake_pos, n_points)

    # Auxiliary vars
    stats_names = list(stats_config.keys())
    stat_funcs = [stats_config[name] for name in stats_names]
    snake_pos_stats = get_position_stats(snake_pos, stat_funcs)

    # Dummies for snake_dir
    snake_dir_str = get_dir_str(snake_dir)
    snake_dir_order = ["R", "L", "D", "U"]
    snake_dir_arr = (np.array(snake_dir_order) == snake_dir_str).astype(int)

    # Game score as a list to be able to use np.concatenate()
    game_score = [int(game_score)]

    feature_vals = np.concatenate([norm_snake_pos.flatten(), snake_dir_arr, snake_pos_stats, game_score ])

    # Make sure that this order is the same as in `feature_vals`
    if return_names:
        # getting the names of the features
        norm_pos_column_names = [f"norm_pos_{i}_{c}" for i in range(n_points) for c in "xy"]
        stats_column_names = [s + "_" + c for s in stats_names for c in "xy"]
        snake_dir_column_names = ["snake_dir_" + s for s in snake_dir_order]
        feature_names = norm_pos_column_names + snake_dir_column_names + stats_column_names + ["game_score"]
        feature_vals = dict(zip(feature_names, feature_vals))

    return feature_vals
