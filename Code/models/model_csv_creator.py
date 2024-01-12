import pandas as pd
import pickle
from os import walk
import re
# the only true csv creator
# Read data and format it
df = pd.read_csv("Code/data/dow_jones_preprocessed.csv")
df["Dow Jones"] = df.Close
df.drop(columns=["High", "Low", "Open", "Close"], inplace=True)
df.set_index("Date", inplace=True)
df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
df["Dow Jones"] = df["Dow Jones"].astype("float")

def extract_rmse(file_path):
    # Regular expression to match the RMSE score in the file path
    rmse_pattern = r'rmse_([0-9]+\.[0-9]+)'
    match = re.search(rmse_pattern, file_path)

    if match:
        return float(match.group(1))
    else:
        return None

def load_models():
    def load_model(path):
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
            print(f"Loaded model data from {path} is of type: {type(model_data)}")
            
            if isinstance(model_data, list) and len(model_data) == 3:
                features, targets, predictions = model_data

                if len(features) == len(targets) == len(predictions):
                    # Convert targets and predictions to DataFrames
                    df_targets = pd.DataFrame({'target': targets}, index=features.index)
                    df_predictions = pd.DataFrame({'predictions': predictions}, index=features.index)

                    # Join the DataFrames
                    df = features.join(df_targets).join(df_predictions)
                    return df
                else:
                    print("Lists in the model data are not of the same length.")
            else:
                print("The loaded model data does not contain three lists.")

            return None
    
    
    path = "Code/data/models/test_reg_models/"

    models = []
    for (dirpath, dirnames, filenames) in walk(path):
        models.extend(filenames)
        break    
    
    model_dfs = {}
    for model in models:
        model_df = load_model(path + model)
        path_trash, model_name = model.split("onData_")
        
        rsme = extract_rmse(path_trash)
        model_name = model_name.replace(".pickle", "").replace(".csv", "")
        if model_df is not None:
            if model_name not in model_dfs:
                model_dfs[model_name] = [model_df, rsme]
            elif rsme is not None and rsme < model_dfs[model_name][1]: model_dfs[model_name] = [model_df, rsme]
            #print(f"Data from {model}:")
            #print(model_df.head())  # Inspect the first few rows of the loaded model DataFrame
    print(model_dfs)        
    return model_dfs        

def add_predictions_to_df(original_df, model_dfs):
    for model_name, model_df in model_dfs.items():
        # Rename the 'predictions' column to the model's name
        model_df = model_df[0].rename(columns={'predictions': model_name})
        model_df.index = pd.to_datetime(model_df.index, format="%Y-%m-%d")
        # Join the model's predictions to the original DataFrame
        original_df = original_df.join(model_df[model_name], how='left')

    return original_df

# Assuming 'models' is a dictionary where the key is the model name and the value is the corresponding DataFrame
# Example: models = {'model1': df_model1, 'model2': df_model2, ...}

#df_with_predictions = add_predictions_to_df(df, models)

# Display the first few rows of the updated DataFrame
#print(df_with_predictions.head())    

model_dfs = load_models()

df = add_predictions_to_df(df, model_dfs)
df.dropna(inplace=True)
df.to_csv("Code/data/dow_jones_prediction_real.csv")

print(df)