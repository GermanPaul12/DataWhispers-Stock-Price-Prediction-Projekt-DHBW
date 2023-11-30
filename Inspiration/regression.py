import os
from datetime import datetime

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

DATA_DIR = "./word2vec/regression_data/"  # use all pickle (or csv, depend on PICKLE) files in this directory
PICKLE = False


def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn


def evaluate_model_from_csv(csv: str):
    """
    Evaluate a model from a csv filepath. See evaluate_model for more details.
    :param csv: str
    :return: passthrough from evaluate_model
    """
    df = pd.read_csv(csv, index_col="date")
    df = df.drop(columns=["Unnamed: 0"])
    print()
    print(f"Evaluating model: {csv} with last modified: {datetime.fromtimestamp(os.path.getmtime(csv))}")
    return evaluate_model(df, file_path)


def evaluate_model_from_pickle(pickle: str):
    """
    Evaluate a model from a pickle filepath. See evaluate_model for more details.
    :param pickle: str
    :return: pass through from evaluate_model
    """
    df = pd.read_pickle(pickle)
    print()
    print(f"Evaluating model: {pickle} with last modified: {datetime.fromtimestamp(os.path.getmtime(pickle))}")
    return evaluate_model(df, file_path)


def evaluate_model(df, file_path):
    """
    Run a linear regression with df as features and the dow jones index as target. Evaluates with RMSE.
    Saves the model and Data. Return list of results.
    :param df: pd.DataFrame
    :param file_path: csv or pickle file path
    :return: list of results
    """
    file_path_stripped = file_path.split("/")[-1]
    # LOAD DOW JONES
    target = pd.read_csv("./dow_jones/dow_jones_preprocessed.csv")
    df_target = target[["Date", "Close"]]
    df_target = df_target.set_index("Date")
    df_target.rename_axis("date", inplace=True)

    # PREPROCESS
    df = df.join(df_target, how="left", on='date')
    df = df.dropna()
    df = df.sort_index(axis=0)

    # AGGREGATE
    df = df.groupby("date").mean()

    # BUILD FEATURES AND TARGET
    X = df.drop(columns=["Close"])
    y = df["Close"]

    # TRAIN
    estimator = LinearRegression()
    estimator.fit(X, y)

    # PREDICT
    predictions = estimator.predict(X)

    # EVALUATE
    rmse = mean_squared_error(y, predictions, squared=True)
    rmse_div_num_test_samples = rmse / len(y)

    # Format with 1000s separator and 4 decimal places
    print(f"RMSE: {rmse:,.4f}")
    print(f"RMSE / num_test_samples: {rmse_div_num_test_samples:,.4f}")
    current_time = datetime.now().time()

    list_result = [file_path_stripped, rmse, rmse_div_num_test_samples]

    # SAVE MODEL FOR FUTURE USE
    with open(
            f'./word2vec/regression_data/models/rmse_{rmse:.4f}_trainEval_{current_time}_onData_{file_path_stripped}.pickle'.replace(
                ":", "-"), 'wb') as f:
        pickle.dump(estimator, f)

    # SAVE DATA FOR FUTURE USE
    with open(
            f'./word2vec/regression_data/data/rmse_{rmse:.4f}_trainEval_{current_time}_onData_{file_path_stripped}.pickle'.replace(
                ":", "-"), 'wb') as f:
        pickle.dump([X, y], f)

    return list_result


if __name__ == '__main__':
    list_of_list_res = []
    for filename in os.listdir(DATA_DIR):
        if PICKLE:
            if filename.endswith(".pickle"):
                file_path = os.path.join(DATA_DIR, filename)
                list_of_list_res.append(evaluate_model_from_pickle(file_path))
        else:
            if filename.endswith(".csv"):
                file_path = os.path.join(DATA_DIR, filename)
                list_of_list_res.append(evaluate_model_from_csv(file_path))
    df_result = pd.DataFrame(list_of_list_res, columns=["file_path", "rmse", "rmse_div_num_test_samples"])
    df_result.to_csv('result_df.csv')
    print(df_result)
