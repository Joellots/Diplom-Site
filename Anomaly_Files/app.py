import streamlit as st
import pandas as pd
import col_definition as cd
from sklearn.ensemble import RandomForestClassifier
from typing import Union

# from sklearn.metrics import accuracy_score, classification_report
# from sklearn.preprocessing import OneHotEncoder
#from sklearn.preprocessing import MinMaxScaler

# Load the dataset
@st.cache_data
def load_data():
    url = "Train.txt"  # Replace with the actual URL or path to your dataset
    df = pd.read_csv(url, header=None, names=cd.columns)
    return df

df = load_data()

class Exception(Exception):
    pass



# Streamlit app
st.title("Network Traffic Anomaly Detection")

# Sidebar with user input
st.sidebar.header("Input Features")
user_input = {}

def nominal(col: str):
    global user_input
    user_input[col] = st.sidebar.selectbox(col, df[col].unique())

def binary(col: str):
    global user_input
    user_input[col] = st.sidebar.selectbox(col, [0, 1])

def numeric(col: str):
    global user_input
    user_input[col] = st.sidebar.text_input(col, f"", key=col)
    try:
        user_input[col] = float(user_input[col])  # Try to convert to float
    except ValueError:
        user_input[col] = df[col].mean()  # Default to mean if input is not a valid number

binary('land')
binary('logged_in')
numeric('wrong_fragment')
numeric('serror_rate')
numeric('srv_serror_rate')
numeric('dst_host_same_src_port_rate')
numeric('dst_host_serror_rate')
numeric('dst_host_srv_serror_rate')
nominal('protocol_type')
nominal('service')
nominal('flag')


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
def scale(df: pd.DataFrame, numeric_cols: list, key=None) -> Union[pd.DataFrame, list]:
    global scaler
    if key == 'fit':
        scaler.fit(df[numeric_cols])
    if key == 'trans': 
        df[numeric_cols] = scaler.transform(df[numeric_cols])
    return df, numeric_cols


from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore') #sparse=False
def encode(df: pd.DataFrame, encoded_cols: list, categorical_cols: list, key=None) -> Union[pd.DataFrame, list]:
    global encoder
    if key == 'fit':
        encoder.fit(df[categorical_cols])
        encoded_cols_out = list(encoder.get_feature_names_out(categorical_cols))
        return encoded_cols_out
    if key == 'trans':
        df[encoded_cols] = encoder.transform(df[categorical_cols])
        return df

    raise Exception("Invalid Key Input")


# Prepare input data for prediction
input_df = pd.DataFrame([user_input])

# Scale numeric features
numeric_cols = [i for i in cd.numeric_cols if i in cd.raw_selected_cols]
df = scale(df, numeric_cols, 'fit')[0]
df = scale(df, numeric_cols, 'trans')[0]
input_df = scale(input_df, numeric_cols, 'trans')[0]

# Encode categorical features
selected_categorical_cols = [i for i in cd.categorical_cols if i in cd.raw_selected_cols]
encoded_cols = encode(df, encoded_cols=None, categorical_cols=selected_categorical_cols, key='fit')
df = encode(df, encoded_cols=encoded_cols, categorical_cols=selected_categorical_cols, key='trans')
input_df = encode(input_df, encoded_cols=encoded_cols, categorical_cols=selected_categorical_cols, key='trans')

# Concatenate scaled numeric and encoded categorical features
#prepared_input = pd.concat([pd.DataFrame(scaled_numeric_input, columns=numeric_cols), pd.DataFrame(encoded_categorical_input, columns=encoded_cols)], axis=1)
prepared_df = df[numeric_cols + encoded_cols].to_numpy()
prepared_input = input_df[numeric_cols + encoded_cols].to_numpy()

# df[numeric_cols + encoded_cols + cd.target_cols].to_csv('df.csv', index=False)
# input_df[numeric_cols + encoded_cols].to_csv('input_df.csv', index=False)


# Predict the attack type
forest = RandomForestClassifier(n_estimators=60, random_state=2, max_features=11)
forest.fit(prepared_df, df[cd.target_cols].values.ravel())


from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(C=1, multi_class='multinomial', solver='lbfgs', random_state=42, max_iter=1000)
logreg.fit(prepared_df, df[cd.target_cols].values.ravel())
prediction = forest.predict(prepared_input)

# Display the result
st.subheader("Prediction")
#st.write(f"{prediction[0]}")
if str(prediction[0]) == 'normal':
    st.write(f"The Network is in baseline normal state.")
else:
    if str(prediction[0]) in cd.attack_class['DoS']:
        st.write(f"The network might be under attack. The predicted attack type is: {prediction[0]}; Attack Class: Denial of Service (DoS)")
    elif str(prediction[0]) in cd.attack_class['Probe']:
        st.write(f"The network might be under attack. The predicted attack type is: {prediction[0]}; Attack Class: Probe")
    elif str(prediction[0]) in cd.attack_class['R2L']:
        st.write(f"The network might be under attack. The predicted attack type is: {prediction[0]}; Attack Class: Unauthorized Access from a Remote Machine (R2L)")
    elif str(prediction[0]) in cd.attack_class['U2R']:
        st.write(f"The network might be under attack. The predicted attack type is: {prediction[0]}; Attack Class: Unauthorized Access to Local Root Privileges (U2R)")