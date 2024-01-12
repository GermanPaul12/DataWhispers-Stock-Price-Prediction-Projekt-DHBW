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

def load_model(path):
    with open(path, 'rb') as f:
        model_data = pickle.load(f)
        print(f"Loaded model data from {path} is of type: {type(model_data)}")
        
        # Check if the model data is a dictionary and contains the expected keys
        if isinstance(model_data, dict) and all(key in model_data for key in ["features", "targets", "predictions", "r_squared"]):
            features = model_data["features"]
            targets = model_data["targets"]
            predictions = model_data["predictions"]
            r_squared = model_data["r_squared"]

            # Check if the lengths of features, targets, and predictions match
            if len(features) == len(targets) == len(predictions):
                df_features = pd.DataFrame(features)
                df_targets = pd.DataFrame({'target': targets}, index=df_features.index)
                df_predictions = pd.DataFrame({'predictions': predictions}, index=df_features.index)

                # Combine into a single DataFrame
                df = df_features.join(df_targets).join(df_predictions)
                return df, r_squared
            else:
                print("Components of the model data are not of the same length.")
        else:
            print("The loaded model data is not in the expected dict format or missing keys.")

        return None, None


def load_models():
    path = "Code/data/models/reg_models/pickles/"

    models = []
    for (dirpath, dirnames, filenames) in walk(path):
        models.extend(filenames)
        break    
    
    model_dfs = {}
    for model in models:
        model_df, r_squared = load_model(path + model)
        path_trash, model_name = model.split("onData_")
        
        rsme = extract_rmse(path_trash)
        model_name = model_name.replace(".pickle", "").replace(".csv", "")
        if model_df is not None:
            if model_name not in model_dfs:
                model_dfs[model_name] = [model_df, rsme, r_squared]
            elif rsme is not None and rsme < model_dfs[model_name][1]:
                model_dfs[model_name] = [model_df, rsme, r_squared]
    return model_dfs

# Other functions remain the same

model_dfs = load_models()

# Now, model_dfs contains the R-squared value at index 2 for each model.  

def add_predictions_to_df(original_df, model_dfs):
    for model_name, model_df in model_dfs.items():
        # Rename the 'predictions' column to the model's name
        model_df = model_df[0].rename(columns={'predictions': model_name})
        model_df.index = pd.to_datetime(model_df.index, format="%Y-%m-%d")
        # Join the model's predictions to the original DataFrame
        original_df = original_df.join(model_df[model_name], how='left')

    return original_df

def create_rmse_df(model_dfs):
    # Extract model names and their RMSE scores
    model_names = []
    rmse_scores = []
    r_squared = []

    for model_name, data in model_dfs.items():
        model_names.append(model_name)
        rmse_scores.append(data[1])  # Assuming the RMSE score is the second element
        r_squared.append(data[2])  # Assuming the R-squared value

    # Create a DataFrame
    rmse_df = pd.DataFrame({
        'Model Name': model_names,
        'RMSE': rmse_scores,
        'R-squared': r_squared
    })

    # Save the DataFrame to a CSV file
    rmse_df.to_csv("Code/data/model_rmse_scores.csv", index=False)
    return rmse_df

model_dfs = load_models()

df = add_predictions_to_df(df, model_dfs)
df.dropna(inplace=True)
df.to_csv("Code/data/dow_jones_prediction_real.csv")

rmse_df = create_rmse_df(model_dfs)

print(model_dfs)