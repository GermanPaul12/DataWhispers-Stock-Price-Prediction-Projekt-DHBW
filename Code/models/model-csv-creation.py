
import pandas as pd
import pickle
import sklearn
import plotly.express as px
from os import walk



#print(models)
def main():
    # read linear model from pickle
    path = "Code/data/models/word2vec/"

    models = []
    for (dirpath, dirnames, filenames) in walk(path):
        models.extend(filenames)
        break


    def load_model(path):
        with open(path, 'rb') as f:
            model_list = pickle.load(f)
            print(f"Loaded model from {path} is of type: {type(model_list)}")
            if isinstance(model_list, list) and len(model_list) == 2:
                df_features, series_target = model_list
                # Check if the first element is a DataFrame and the second is a Series
                if isinstance(df_features, pd.DataFrame) and isinstance(series_target, pd.Series):
                    # Merge them into a single DataFrame
                    df = df_features.join(series_target.to_frame(name='Close'))
                    return df
                else:
                    print("The list elements are not as expected (DataFrame and Series).")
            else:
                print("The loaded model list does not contain two elements.")
            return None  # Returning None to indicate the object is not as expected

    df_real = pd.read_csv("Code/data/dow_jones_preprocessed.csv")
    df_real.set_index('Date', inplace=True)
    df_real.index = pd.to_datetime(df_real.index, format="%Y-%m-%d")

    print(df_real)

    for model in models:
        df = load_model(path + model)
        if df is not None:
            original_column_name = 'Close'  # Change if the column name in the model DataFrame is different
            new_column_name = model.rstrip('.pickle')  # Assuming model file names end with '.pickle'
            df = df.rename(columns={original_column_name: new_column_name})
            df.index = pd.to_datetime(df.index, format="%Y-%m-%d")

            print(f"Data from {model}:")
            print(df.head())  # Inspect the first few rows of the loaded model DataFrame

            df_real = df_real.join(df[new_column_name], on='Date', how='left')
            
            print(f"df_real after joining {model}:")
            print(df_real.head())  # Inspect df_real after each join
        else:
            print(f"Failed to load DataFrame from {path + model} model.")


    df_real.to_csv(r"C:\Users\Germa\Documents\DHBW\DataWhispers-Stock-Price-Prediction-Projekt-DHBW\Code\data\dow_jones_prediction_real.csv")


if __name__ == "__main__":
    pass
    main()