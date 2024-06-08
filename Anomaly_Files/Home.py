import streamlit as st
import pandas as pd
import col_definition as cd
from joblib import load
from PIL import Image
import base64

from pathlib import Path
import pickle
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

st.set_page_config(page_title="ОБНАРУЖЕНИЕ СЕТЕВЫХ АНОМАЛИЙ", page_icon=":guardsman:", layout="centered")


# names = ['Okore', 'Albert']
# usernames = ['admin', "Albert"]

# file_path = Path(__file__).parent / 'hashed_pw.pkl'
# with file_path.open('rb') as file:
#     hashed_passwords = pickle.load(file)

config_path = os.path.join('.', 'config.yaml')

with open('config_2.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('main', 'Введите свое имя пользователя и пароль', fields={'Form name': 'Авторизоваться', 'Username':'Имя пользователя', 'Password':'Пароль', 'Login':'Вход'})


if authentication_status == False:
    st.error('Имя пользователя/пароль неверны')
if authentication_status == None:
    
    st.warning('Пожалуйста, введите имя пользователя и пароль')

    with st.expander("Забыли пароль?"):
    
        try:
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(fields={'Form name': 'Запомнить пароль', 'Username':'Имя пользователя', 'Submit':'Далее'})
        
            if username_of_forgotten_password:
                # with open('config.yaml', 'r') as file:
                #     data = yaml.safe_load(file)

                # data['credentials']['usernames'][username_of_forgotten_password]['password'] = new_random_password
                
                
                # with open('config.yaml', 'w') as file:
                #     yaml.safe_dump(data, file)

                with open('config.yaml', 'r') as file:
                    data = yaml.safe_load(file)
                password = data['credentials']['usernames'][username_of_forgotten_password]['password'] 

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
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(fields = {'Form name': 'Заполните все поля', 'Name':'ФИО', 'Username':'Имя пользователя', 'Password':'Пароль', 'Email':'Электронная почта', 'Repeat password':'Повторите пароль', 'Register':'Зарегистрировать'}, pre_authorization=False)
            if email_of_registered_user:            
                with open('config.yaml', 'r') as file:
                    data = yaml.safe_load(file)

                import random
                import string

                letters = string.ascii_letters  # This includes both lowercase and uppercase letters
                random_string = ''.join(random.choice(letters) for i in range(8))

                new_data = {
                        'email': email_of_registered_user,
                        'name': name_of_registered_user,
                        'password': random_string,
                    }

                data['credentials']['usernames'][username_of_registered_user] = new_data

                with open('config.yaml', 'w') as file:
                    yaml.safe_dump(data, file)

                st.success('Регистрация прошла успешно! Войдите в систему, используя учетные данные, отправленные на указанный электронный адрес')

                from send_mail import send_email
                send_email(1, username_of_registered_user, email_of_registered_user, random_string)
                
        except Exception as e:
            st.error(e)

    
if authentication_status:
    #authenticator.logout('Logout', 'main')
    authenticator.logout('Выход', 'sidebar')
    st.sidebar.title(f'Добро пожаловать {name}')

    ### CODE

    @st.cache_data
    def load_data():
        url = "Train.txt"  # Replace with the actual URL or path to your dataset
        df = pd.read_csv(url, header=None, names=cd.columns)
        return df



    CUSTOM_CSS = """
    <style>
    body {
        background-color: #f0f2f6; /* Set background color */
        font-family: Arial, sans-serif;
        line-height: 1.6;
        padding: 20px;
        color: #333; /* Set text color */
    }

    h1, h2, h3 {
        color: #333; /* Set heading color */
    }

    .sidebar .sidebar-content {
        background-color: #ffffff; /* Set sidebar background color */
    }

    /* Add more custom styles as needed */
    </style>
    """

    # Apply custom CSS styles
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.logo("knrtu_logo.png", link=None)

    # Load Data
    df = load_data()

    st.title("ОБНАРУЖЕНИЕ АНОМАЛИЙ В СЕТЕВОМ ТРАФИКЕ")

    # Sidebar with user input
    st.sidebar.header("Ввод данных пользователя")
    user_input = {}

    # Access the components from the loaded file
    Forest_Map = load(r"C:\Users\okore\OneDrive\Desktop\MACHINE_LEARNING\Anomaly_Detection\streamlit\Forest_Map")
    model = Forest_Map['model']
    scaler = Forest_Map['scaler']
    encoder = Forest_Map['encoder']
    KBestFeatures = Forest_Map['KBestFeatures']
    KB_numeric_cols = Forest_Map['KB_numeric_cols']
    KB_categorical_cols = Forest_Map['KB_categorical_cols']
    KB_target_cols = Forest_Map['KB_target_cols']
    encoded_cols = Forest_Map['encoded_cols']

    def nominal(col: str):
        global user_input
        global serv_type_dict, proto_type_dict, flag_type_dict
        raw_input = st.sidebar.selectbox(cd.feature_map[col], df[col].unique())

        user_input[col] = raw_input

    def binary(col: str):
        global user_input
        user_input[col] = st.sidebar.selectbox(cd.feature_map[col], [0, 1])

    def numeric(col: str):
        global user_input
        user_input[col] = st.sidebar.text_input(cd.feature_map[col], f"", key=col, placeholder= col)
        try:
            user_input[col] = float(user_input[col])  # Try to convert to float
        except ValueError:
            user_input[col] = df[col].mean()  # Default to mean if input is not a valid number


    for item in KBestFeatures:
        if item in cd.binary_cols:
            binary(item)
        if item in cd.numeric_cols:
            numeric(item)
        if item in cd.categorical_cols:
            nominal(item)


    input_df = pd.DataFrame([user_input], columns=KBestFeatures)
    #print(input_df)
    input_df[KB_numeric_cols] = scaler.transform(input_df[KB_numeric_cols])
    input_df[encoded_cols] = encoder.transform(input_df[KB_categorical_cols])
    user_df = input_df[KB_numeric_cols + encoded_cols].copy()
    #print(input_df)

    #st.markdown('<audio id="beep" src="beep-warning.mp3" preload="auto" ;"></audio>', unsafe_allow_html=True)

    def autoplay_audio(file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true" id="beep" style="display:none">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            
            st.markdown(
                md,
                unsafe_allow_html=True,
            )
            
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
            if str(prediction[0]) in cd.attack_class['DoS']:
                st.error(f"""Обнаружена атака типа: {prediction[0].upper()}; 
                            Тип атаки: Отказ в обслуживании (DOS)""")
                autoplay_audio("beep_warning.mp3")
                remove_audio()
            elif str(prediction[0]) in cd.attack_class['Probe']:
                st.warning(f"""Обнаружена атака типа: {prediction[0].upper()}; 
                            Тип атаки: Проникновение (Probe)""")
                remove_audio()
                autoplay_audio("beep_warning.mp3")
                remove_audio()
            elif str(prediction[0]) in cd.attack_class['R2L']:
                st.warning(f"""Обнаружена атака типа: {prediction[0].upper()}; 
                            Тип атаки: Удаленный доступ к локальному (R2L)""")
                autoplay_audio("beep_warning.mp3")
                remove_audio()
            elif str(prediction[0]) in cd.attack_class['U2R']:
                st.error(f"""Обнаружена атака типа: {prediction[0].upper()}; 
                            Тип атаки: Локальный доступ к Root (U2R)""")
                autoplay_audio("beep_warning.mp3")
                remove_audio()

    # Display the image
    webp_image = Image.open(r"C:\Users\okore\OneDrive\Desktop\MACHINE_LEARNING\Anomaly_Detection\streamlit\detection_img.jpg")
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
