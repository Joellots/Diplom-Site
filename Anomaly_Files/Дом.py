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

columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate", "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate", "diff_srv_rate", "srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","attack", "last_flag"]

numeric_cols = ["duration","src_bytes","dst_bytes",
"wrong_fragment","urgent","hot","num_failed_logins",
"num_compromised","num_root","num_file_creations",
"num_shells","num_access_files","num_outbound_cmds","count","srv_count","serror_rate", "srv_serror_rate",
"rerror_rate","srv_rerror_rate","same_srv_rate", "diff_srv_rate", "srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
"dst_host_diff_srv_rate","dst_host_same_src_port_rate",
"dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
"dst_host_rerror_rate","dst_host_srv_rerror_rate"]

categorical_cols = ["protocol_type", "service", "flag"]

binary_cols = ['land', 'logged_in', 'root_shell', 'su_attempted', 'is_host_login', 'is_guest_login']

target_cols = ['attack']

raw_selected_cols = ['land',
 'wrong_fragment',
 'logged_in',
 'serror_rate',
 'srv_serror_rate',
 'dst_host_same_src_port_rate',
 'dst_host_serror_rate',
 'dst_host_srv_serror_rate',
 'protocol_type',
 'service',
 'flag',
 'dst_host_same_srv_rate',
 'same_srv_rate',
 'dst_host_srv_diff_host_rate',
 'dst_host_srv_count',
 'srv_rerror_rate', 
 'dst_host_srv_rerror_rate',]

attack_class = {
    "DoS" : ['back', 'land', 'neptune', 'pod', 'smurf', 'teardrop', 'apache2', 'udpstorm', 'processtable', 'worm'],
    "Probe" : ['satan', 'ipsweep', 'nmap', 'portsweep', 'mscan', 'saint'],
    "R2L" : ['guess_passwd', 'ftp_write', 'imap', 'phf', 'multihop', 'warezmaster', 'warezclient', 'spy', 'xlock', 'xsnoop', 'snmpguess', 'snmpgetattack', 'httptunnel', 'sendmail', 'named'],
    "U2R" : ['buffer_overflow', 'loadmodule', 'rootkit', 'perl', 'sqlattack', 'xterm', 'ps',]
}

my_attack = ['neptune','normal','smurf','ipsweep','back','nmap','warezclient','satan', 'portsweep', 'teardrop', 'guess_passwd', 'pod', 'rootkit', 'ftp_write', 'buffer_overflow', 'land', 'multihop', 'imap', 'loadmodule', 'perl', 'warezmaster', 'phf', 'spy']

feature_map = {
    'duration': 'DURATION',
    'protocol_type': 'PROTOCOL TYPE (protocol_type)',
    'service': 'SERVICE (service)',
    'flag': 'FLAG (flag)',
    'src_bytes': 'SOURCE BYTES',
    'dst_bytes': 'DESTINATION BYTES',
    'dst_host_same_src_port_rate': 'DESTINATION HOST SAME SERVICE PORT RATE',
    'srv_count': 'SAME SERVICE COUNT',
    'dst_host_rerror_rate' : 'DESTINATION HOST R-FLAG ERROR RATE',
    
    'dst_host_same_srv_rate': 'DESTINATION HOST SAME SERVICE RATE',
    'dst_host_diff_srv_rate': 'DESTINATION HOST DIFFERENT SERVICE RATE',
    'dst_host_srv_rerror_rate': 'DESTINATION HOST SERVICE R-FLAG ERROR RATE',
    'same_srv_rate': 'SAME SERVICE RATE',
    
    'dst_host_srv_count': 'DESTINATION HOST SAME SERVICE COUNT',
    'diff_srv_rate': 'DIFFERENT SERVICE RATE',
    'count': 'COUNT',
    'dst_host_srv_diff_host_rate': 'DESTINATION HOST SERVICE RATE FROM DIFFERENT HOST',
    'dst_host_srv_serror_rate': 'DESTINATION HOST SERVICE S-FLAG ERROR RATE',
    'dst_host_serror_rate': 'DESTINATION HOST S-FLAG ERROR RATE'
}


# Set page configuration
st.set_page_config(page_title="ОБНАРУЖЕНИЕ СЕТЕВЫХ АНОМАЛИЙ", page_icon=":guardsman:", layout="centered")

# Function to get credentials from Firebase
# @st.cache_data(ttl=600)
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
st.logo(os.path.join(current_dir, 'knrtu_logo.png'), link=None)

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
      fields={'Form name': 'Авторизоваться', 'Username':'Имя пользователя', 'Password':'Пароль', 'Login':'Вход'})

if authentication_status == False:
    st.error('Имя пользователя/пароль неверны')
if authentication_status == None:
    st.warning('Пожалуйста, введите имя пользователя и пароль')

    with st.expander("Забыли пароль?"):
        try:
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(
                fields={'Form name': 'Запомнить пароль', 'Username':'Имя пользователя', 'Submit':'Далее'}
            )
            
            if email_of_forgotten_password:
                password = creds['usernames'][username_of_forgotten_password]['word']
                st.success('Ваш пароль был отправлен на вашу почту')
                from send_mail import send_email
                send_email(2, username_of_forgotten_password, email_of_forgotten_password, password)
            elif username_of_forgotten_password == False:
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
        return pd.read_csv(url, header=None, names=columns)

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
        user_input[col] = st.sidebar.selectbox(feature_map[col], df[col].unique())

    def binary(col: str):
        user_input[col] = st.sidebar.selectbox(feature_map[col], [0, 1])

    def numeric(col: str):
        user_input[col] = st.sidebar.text_input(feature_map[col], f"", key=col, placeholder=col)
        try:
            user_input[col] = float(user_input[col])
        except ValueError:
            user_input[col] = df[col].mean()

    for item in KBestFeatures:
        if item in binary_cols:
            binary(item)
        elif item in numeric_cols:
            numeric(item)
        elif item in categorical_cols:
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

    # Display the result
    if st.sidebar.button('Predict'):
        # st.write(" ".join(map(str, input_df.stack().tolist())))
        prediction = model.predict(user_df.to_numpy())
        remove_audio()
        st.subheader("Прогноз:")
        #st.write(f"{prediction[0]}")
        if str(prediction[0]) == 'normal':
            st.success(f"Все хорошо. Обнаруженный трафик нормальный")
        else:
            if str(prediction[0]) in attack_class['DoS']:
                st.error(f"""Обнаружена атака типа: {prediction[0].upper()}; 
                            Тип атаки: Отказ в обслуживании (DOS)""")
                autoplay_audio(os.path.join(current_dir, "beep_warning.mp3"))
                remove_audio()
            elif str(prediction[0]) in attack_class['Probe']:
                st.warning(f"""Обнаружена атака типа: {prediction[0].upper()}; 
                            Тип атаки: Проникновение (Probe)""")
                remove_audio()
                autoplay_audio(os.path.join(current_dir, "beep_warning.mp3"))
                remove_audio()
            elif str(prediction[0]) in attack_class['R2L']:
                st.warning(f"""Обнаружена атака типа: {prediction[0].upper()}; 
                            Тип атаки: Удаленный доступ к локальному (R2L)""")
                autoplay_audio(os.path.join(current_dir, "beep_warning.mp3"))
                remove_audio()
            elif str(prediction[0]) in attack_class['U2R']:
                st.error(f"""Обнаружена атака типа: {prediction[0].upper()}; 
                            Тип атаки: Локальный доступ к Root (U2R)""")
                autoplay_audio(os.path.join(current_dir, "beep_warning.mp3"))
                remove_audio()
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
    st.markdown("[Перейти на страницу помощи](Помощь)")
