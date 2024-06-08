import os
import time
import base64
import random
import string

import streamlit as st
import pandas as pd
from joblib import load
from PIL import Image
from pathlib import Path
import streamlit_authenticator as stauth
import yaml
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, auth
import json

import col_definition as cd

# Set page configuration
st.set_page_config(page_title="ОБНАРУЖЕНИЕ СЕТЕВЫХ АНОМАЛИЙ", page_icon=":guardsman:", layout="centered")

# Function to get credentials from Firebase
@st.cache_data(ttl=600)
def get_creds(db):
    cred_ref = db.collection("credentials")
    usernames_ref = cred_ref.document('usernames').collections()
    creds = {"usernames": {}}
    for username_col in usernames_ref:
        for doc in username_col.stream():
            creds["usernames"][doc.id] = doc.to_dict()
    return creds

# Initialize Firebase
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config.yaml')
cred_path = os.path.join(current_dir, 'anomaly-detection-d4b91-firebase-adminsdk-lwlgg-d92f4bd41c.json')
db = firestore.Client.from_service_account_json(cred_path)

# Load credentials
creds = get_creds(db)

# Initialize Authenticator
authenticator = stauth.Authenticate(
    creds,
    "anomaly_cookie",
    "anomaly_key",
    10,
    "okorejoellots@gmail.com",
)

name, authentication_status, username = authenticator.login(
    'main', 'Введите свое имя пользователя и пароль',
    fields={'Form name': 'Авторизоваться', 'Username':'Имя пользователя', 'Password':'Пароль', 'Login':'Вход'}
)

if authentication_status == False:
    st.error('Имя пользователя/пароль неверны')
elif authentication_status == None:
    st.warning('Пожалуйста, введите имя пользователя и пароль')

    with st.expander("Забыли пароль?"):
        try:
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(
                fields={'Form name': 'Запомнить пароль', 'Username':'Имя пользователя', 'Submit':'Далее'}
            )
            if username_of_forgotten_password:
                password = creds['usernames'][username_of_forgotten_password]['password']
                st.success('Ваш пароль был отправлен на вашу почту')
                from send_mail import send_email
                send_email(2, username_of_forgotten_password, email_of_forgotten_password, password)
            else:
                st.error('Имя пользователя не найдено')
        except Exception as e:
            st.error(e)

    st.header("Регистрация пользователя", divider='rainbow')

    with st.expander("Зарегистрировать нового пользователя"):
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                fields={'Form name': 'Заполните все поля', 'Name':'ФИО', 'Username':'Имя пользователя', 'Password':'Пароль', 'Email':'Электронная почта', 'Repeat password':'Повторите пароль', 'Register':'Зарегистрировать'},
                pre_authorization=False
            )

            if email_of_registered_user:
                random_password = ''.join(random.choice(string.ascii_letters) for _ in range(10))
                db.collection('credentials').document('usernames').collection(username_of_registered_user).document(username_of_registered_user).set({
                    'name': name_of_registered_user,
                    'email': email_of_registered_user,
                    'password': random_password,
                    'word': random_password,
                })

                st.success('Регистрация прошла успешно! Войдите в систему, используя учетные данные, отправленные на указанный электронный адрес')
                creds = get_creds(db)
                from send_mail import send_email
                send_email(1, username_of_registered_user, email_of_registered_user, random_password)
        except Exception as e:
            st.error(e)

if authentication_status:
    authenticator.logout('Выход', 'sidebar')
    st.sidebar.title(f'Добро пожаловать {name}')

    CUSTOM_CSS = """
    <style>
    body {
        background-color: #f0f2f6;
        font-family: Arial, sans-serif;
        line-height: 1.6;
        padding: 20px;
    }
    h1, h2, h3 {}
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    </style>
    """
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    @st.cache_data(ttl=600)
    def load_data():
        url = os.path.join(current_dir, "Train.txt")
        return pd.read_csv(url, header=None, names=cd.columns)

    df = load_data()

    st.title("ОБНАРУЖЕНИЕ АНОМАЛИЙ В СЕТЕВОМ ТРАФИКЕ")
    st.sidebar.header("Ввод данных пользователя")
    user_input = {}

    Forest_Map = load(os.path.join(current_dir, "Forest_Map"))
    model = Forest_Map['model']
    scaler = Forest_Map['scaler']
    encoder = Forest_Map['encoder']
    KBestFeatures = Forest_Map['KBestFeatures']
    KB_numeric_cols = Forest_Map['KB_numeric_cols']
    KB_categorical_cols = Forest_Map['KB_categorical_cols']
    KB_target_cols = Forest_Map['KB_target_cols']
    encoded_cols = Forest_Map['encoded_cols']

    def nominal(col: str):
        user_input[col] = st.sidebar.selectbox(cd.feature_map[col], df[col].unique())

    def binary(col: str):
        user_input[col] = st.sidebar.selectbox(cd.feature_map[col], [0, 1])

    def numeric(col: str):
        user_input[col] = st.sidebar.text_input(cd.feature_map[col], f"", key=col, placeholder=col)
        try:
            user_input[col] = float(user_input[col])
        except ValueError:
            user_input[col] = df[col].mean()

    for item in KBestFeatures:
        if item in cd.binary_cols:
            binary(item)
        elif item in cd.numeric_cols:
            numeric(item)
        elif item in cd.categorical_cols:
            nominal(item)

    input_df = pd.DataFrame([user_input], columns=KBestFeatures)
    input_df[KB_numeric_cols] = scaler.transform(input_df[KB_numeric_cols])
    input_df[encoded_cols] = encoder.transform(input_df[KB_categorical_cols])
    user_df = input_df[KB_numeric_cols + encoded_cols].copy()

    def autoplay_audio(file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true" id="beep" style="display:none">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(md, unsafe_allow_html=True)
            st.markdown('<script>document.getElementById("beep").play();</script>', unsafe_allow_html=True)
    def remove_audio():
        st.markdown('<script>document.getElementById("beep").remove();</script>', unsafe_allow_html=True)

    def display_prediction(prediction):
        attack_type = prediction[0].upper()
        if attack_type == 'NORMAL':
            st.success("Все хорошо. Обнаруженный трафик нормальный")
        else:
            attack_msg = {
                'DOS': ("Обнаружена атака типа: {}; Тип атаки: Отказ в обслуживании (DOS)", st.error),
                'PROBE': ("Обнаружена атака типа: {}; Тип атаки: Проникновение (Probe)", st.warning),
                'R2L': ("Обнаружена атака типа: {}; Тип атаки: Удаленный доступ к локальному (R2L)", st.warning),
                'U2R': ("Обнаружена атака типа: {}; Тип атаки: Локальный доступ к Root (U2R)", st.error)
            }
    
            for key, (msg, display_func) in attack_msg.items():
                if attack_type in cd.attack_class[key]:
                    display_func(msg.format(attack_type))
                    autoplay_audio(os.path.join(current_dir, "beep_warning.mp3"))
                    break

    if st.sidebar.button('Predict'):
        prediction = model.predict(user_df.to_numpy())
        remove_audio()
        st.subheader("Прогноз:")
        display_prediction(prediction)
    
    # Display the image
    webp_image = Image.open(os.path.join(current_dir, "detection_img.jpg"))
    jpg_image = webp_image.convert("RGB")
    st.image(jpg_image, caption="Обнаружение аномалий в кибербезопасности сети", width=800)
    
    # Define the content for the help page
    help_content = """
    ### Содержимое страницы помощи
    
    **Объяснение характеристик:**
    - **DURATION:** Продолжительность соединения в секундах.
    - **PROTOCOL TYPE:** Тип протокола, например, TCP, UDP.
    - **SERVICE:** Сетевой сервис на стороне назначения, например, http, ftp.
    - **FLAG:** Статус соединения (нормальный или с ошибкой).
    - **SOURCE BYTES:** Количество байтов данных от источника к назначению.
    - **DESTINATION BYTES:** Количество байтов данных от назначения к источнику.
    - **LAND:** 1, если соединение от/к тому же хосту/порту; 0 в противном случае.
    - **WRONG FRAGMENT:** Количество неверных фрагментов.
    - **URGENT:** Количество срочных пакетов.
    
    ... (Дополнительную информацию можно просмотреть на странице помощи)
    """
    
    # Render the help content on a separate page
    st.markdown(help_content, unsafe_allow_html=True)
    
    # Create a link to the help page on the home page
    st.markdown("[Перейти на страницу помощи](Help_Page)")
