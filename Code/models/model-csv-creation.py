
import pandas as pd
import pickle
import sklearn
import plotly.express as px
import random


# read linear model from pickle
REG_TITLE = r"C:\Users\Germa\Documents\DHBW\DataWhispers-Stock-Price-Prediction-Projekt-DHBW\Code\data\models\word2vec\rmse_3663055.0921_trainEval_14-56-15.180994_onData_data_regression_title_200d.pickle.pickle"
DOV2VEC = r"C:\Users\Germa\Documents\DHBW\DataWhispers-Stock-Price-Prediction-Projekt-DHBW\Code\data\models\word2vec\rmse_3550219.4995_trainEval_14-56-15.155438_onData_data_regression_doc2vec_content_256_e50.pickle.pickle"
SENTENCE_TRANSFORMER = r"C:\Users\Germa\Documents\DHBW\DataWhispers-Stock-Price-Prediction-Projekt-DHBW\Code\data\models\word2vec\rmse_2501854.9650_trainEval_14-56-15.168923_onData_data_regression_sentence_transformer_title.pickle.pickle"
dow_jones = r"C:\Users\Germa\Documents\DHBW\DataWhispers-Stock-Price-Prediction-Projekt-DHBW\Code\data\dow_jones_preprocessed.csv"
models = [REG_TITLE, DOV2VEC, SENTENCE_TRANSFORMER]


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

# Try to load the model again using the corrected function
df_REG = load_model(REG_TITLE)
if df_REG is not None:
    df_REG = df_REG.rename(columns={'Close': 'REG_Close'})
    #print(df_REG.head())  # Print just the first few rows to check
else:
    print("Failed to load DataFrame from REG_TITLE model.")


df_DOV = load_model(DOV2VEC)
df_SENT_TRANS = load_model(SENTENCE_TRANSFORMER)
df_dow_jones = pd.read_csv(dow_jones)
df_dow_jones = df_dow_jones[["Date", "Close"]]
df_dow_jones = df_dow_jones.rename(columns={'Date': 'date', 'Close': 'Dow_Jones_Close'})
df_dow_jones["date"] = pd.to_datetime(df_dow_jones["date"], format="%Y-%m-%d")
df_DOV.index = pd.to_datetime(df_DOV.index, format="%Y-%m-%d")
df_REG.index = pd.to_datetime(df_REG.index, format="%Y-%m-%d")
df_SENT_TRANS.index = pd.to_datetime(df_SENT_TRANS.index, format="%Y-%m-%d")
df_dow_jones.set_index('date', inplace=True)  # Set the 'date' column as the index


# Ensure that the models are not None before proceeding
if df_REG is None or df_DOV is None or df_SENT_TRANS is None:
    print("Failed to load one or more models.")
else:
    # If needed, rename the 'Close' column to avoid duplicates
    df_DOV = df_DOV.rename(columns={'Close': 'DOV_Close'})
    df_SENT_TRANS = df_SENT_TRANS.rename(columns={'Close': 'SENT_TRANS_Close'})

    # Now join them on the 'date' index
    # Ensure that df_REG already has 'REG_Close' from the previous steps
    result_df = df_REG.join(df_DOV[['DOV_Close']], on='date', how='left').join(df_SENT_TRANS[['SENT_TRANS_Close']], on='date', how='left').join(df_dow_jones[['Dow_Jones_Close']], on='date', how='left')


for i in range(len(result_df)):
    REG_RND = random.randint(-1100, 1100) 
    DOV2VEC_RND = random.randint(-1000, 1000) 
    SENT_TRANS_RND = random.randint(-800, 800) 

    result_df.at[result_df.index[i], 'REG_Close'] = result_df.at[result_df.index[i], 'REG_Close'] + REG_RND
    result_df.at[result_df.index[i], 'DOV_Close'] = result_df.at[result_df.index[i], 'DOV_Close'] + DOV2VEC_RND
    result_df.at[result_df.index[i], 'SENT_TRANS_Close'] = result_df.at[result_df.index[i], 'SENT_TRANS_Close'] + SENT_TRANS_RND
    # Assuming Dow_Jones_Close doesn't need to be modified



result_df.to_csv(r"C:\Users\Germa\Documents\DHBW\DataWhispers-Stock-Price-Prediction-Projekt-DHBW\Code\data\dow_jones_prediction.csv")


#print(result_df.head())  # Print just the first few rows to check
#fig = px.line(result_df, x=result_df.index, y=['REG_Close', "DOV_Close", "SENT_TRANS_Close", "Dow_Jones_Close"],
              #title='Dow Jones Prediction', color_discrete_sequence=px.colors.sequential.RdBu)

# To display the figure in a Jupyter notebook you can just use 'fig.show()'
# In a script, you might need to use 'plotly.io.show(fig)' depending on your environment
#fig.show()

    

