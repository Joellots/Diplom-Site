import streamlit as st
from PIL import Image
import os

# Set page title and styles
st.set_page_config(page_title="СТРАНИЦА ПОМОЩИ", layout="wide")

CUSTOM_CSS = """
<style>
body {
    background-color: #f0f2f6; /* Set background color */
    font-family: Arial, sans-serif;
    line-height: 1.6;
    padding: 20px;
    
}

.sidebar .sidebar-content {
    background-color: #ffffff; /* Set sidebar background color */
}

/* Add more custom styles as needed */
</style>
"""

# Apply custom CSS styles
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Define CSS styles
st.markdown(
    """
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
            color: #333;
        }
        ul {
            list-style-type: disc;
            padding-left: 20px;
        }
        li {
            margin-bottom: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_directory = os.path.abspath(os.path.join(current_dir, os.pardir))
st.logo(os.path.join(parent_directory,"knrtu_logo.png"), link=None)

# Render the content using Streamlit markdown
st.title("ПОНИМАНИЕ ОСОБЕННОСТЕЙ СЕТЕВОГО ТРАФИКА")

# Total Features in Dataset
st.header("ОСОБЕННОСТИ НАБОРА ДАННЫХ", divider='rainbow')
features_list = [
    "DURATION (duration): Продолжительность соединения",
    "PROTOCOL TYPE (protocol_type): Протокол, используемый в соединении",
    "SERVICE (service): Используемая сетевая служба назначения",
    "FLAG (flag): Состояние соединения: Нормальное или ошибка",
    "SOURCE BYTES (src_bytes): Количество байт данных, передаваемых от источника к получателю в одном соединении",
    "DESTINATION BYTES (dst_bytes): количество байт данных, передаваемых от получателя к источнику в одном соединении",
    "DESTINATION HOST SAME SERVICE PORT RATE (dst_host_same_src_port_rate): Процент подключений, которые были подключены к одному и тому же исходному порту, среди подключений, агрегированных в DESTINATION HOST SERVICE COUNT (dst_host_srv_count)",
    "SAME SERVICE COUNT (srv_count): Количество подключений к той же службе (номер порта), что и текущее подключение, за последние две секунды",
    "DESTINATION HOST R-FLAG ERROR RATE (dst_host_rerror_rate): Процент подключений, для которых активирован флаг REJ, среди подключений, агрегированных в DESTINATION HOST COUNT (dst_host_count)",
    "DESTINATION HOST S-FLAG ERROR RATE (dst_host_serror_rate): Процент подключений, для которых активирован флаг (4) s0, s1, s2 или s3, среди подключений, агрегированных в DESTINATION HOST COUNT (dst_host_count)"
    "DESTINATION HOST SAME SERVICE RATE (dst_host_same_srv_rate): Процент подключений к одной и той же службе среди подключений, агрегированных в DESTINATION HOST COUNT (dst_host_count)",
    "DESTINATION HOST DIFFERENT SERVICE RATE (dst_host_diff_srv_rate): Процент подключений к различным сервисам среди подключений, агрегированных в DESTIONATION HOST COUNT (dst_host_count)",
    "DESTINATION HOST SERVICE R-FLAG ERROR RATE (dst_host_srv_rerror_rate): Процент подключений, для которых активирован флаг REJ, среди подключений, агрегированных в DESTINATION HOST SERVICE COUNT (dst_host_srv_count)",
    "SAME SERVICE RATE (same_srv_rate): Процент подключений, которые были подключены к одной и той же службе, среди подключений, агрегированных в COUNT (count)",
    "DESTINATION HOST SAME SERVICE COUNT (dst_host_srv_count): Количество подключений с одинаковым номером порта",
    "DIFFERENT SERVICE RATE (diff_srv_rate): Процент подключений к различным службам среди подключений, агрегированных в COUNT (count)",
    "COUNT: Количество подключений к тому же узлу назначения, что и текущее соединение, за последние две секунды",
    "DESTINATION HOST COUNT (count): Количество подключений, имеющих один и тот же IP-адрес узла назначения",
    "DESTINATION HOST SERVICE RATE FROM DIFFERENT HOST: Процент подключений, которые были установлены к различным компьютерам назначения, среди подключений, агрегированных в DESTINATION HOST SERVICE COUNT (dst_host_srv_count)",
    "DESTINATION HOST SERVICE S-FLAG ERROR RATE (dst_host_srv_serror_rate): Процент подключений, для которых активирован флаг s0, s1, s2 или s3, среди подключений, агрегированных в DESTINATION HOST SERVICE COUNT (dst_host_srv_count)",
    "LAND (land): совпадают ли IP-адреса источника и назначения и номера портов (1, если да, 0, если нет)",
    "WRONG FRAGMENT (wrong_fragment): общее количество неверных фрагментов в этом соединении",
    "URGENT (urgent): количество срочных пакетов в этом соединении. Для срочных пакетов активирован бит срочности",
    # Add more features here
]

for feature in features_list:
    st.markdown(f"- **{feature}**")

# Categories within Categorical Features
st.header("КАТЕГОРИИ ВНУТРИ КАТЕГОРИАЛЬНЫХ ПРИЗНАКОВ", divider='rainbow')

# Protocol Types
st.subheader("ТИПЫ ПРОТОКОЛОВ")
st.markdown("Сетевой протокол определяет правила и соглашения для обмена данными, гарантируя, что устройства смогут передавать и получать информацию точно и эффективно.")
protocol_types = {
    "TCP": "Протокол управления передачей (ориентированный на подключение)",
    "ICMP": "Протокол управляющих сообщений Интернета (диагностика и сообщения об ошибках)",
    "UDP": "Протокол пользовательских дейтаграмм (без установления соединения)",
}

for protocol, description in protocol_types.items():
    st.markdown(f"- **{protocol}:** {description}")

# Service Types
st.subheader("ТИПЫ СЕТЕВЫХ СЛУЖБ")
st.markdown("Сетевые службы - это функции или ресурсы, предоставляемые сетью для облегчения связи, передачи данных и других операций между устройствами и приложениями.")
service_types = {
    "FTP_data": "Протокол передачи файлов (передача данных)",
    "Other": "Другие сетевые службы",
    "Private": "Пользовательские или частные сетевые службы",
    "HTTP": "Протокол передачи гипертекста (веб-коммуникация)",
    "Remote_job": "Удаленное выполнение задач",
    "Name": "Имя сервера",
    "Netbios_ns": "NetBIOS Name Service (сервис имен NetBIOS)",
    "Eco_i": "ECO I (ECOnet информационный сервис)",
    "MTP": "Message Transfer Protocol (протокол передачи сообщений)",
    "Telnet": "Удаленный доступ к командной строке",
    "Finger": "Сетевой протокол для запроса информации о пользователях",
    "Domain_u": "Доменные услуги",
    "Supdup": "SUPDUP (простой протокол удаленного доступа к портам)",
    "Uucp_path": "Путь UUCP (протокол Unix-to-Unix Copy)",
    "Z39_50": "Z39.50 (протокол доступа к библиотечным каталогам)",
    "SMTP": "Протокол передачи почты Simple Mail Transfer Protocol",
    "Csnet_ns": "CSNET NS (сетевой протокол для поиска имен)",
    "Uucp": "Протокол Unix-to-Unix Copy",
    "Netbios_dgm": "NetBIOS Datagram Service (сервис датаграмм NetBIOS)",
    "Urpi_i": "URP I (протокол информационного обмена)",
    "Auth": "Сетевая служба аутентификации",
    "Domain": "Служба доменных имен",
    "FTP": "Протокол передачи файлов",
    "Bgp": "Протокол межсетевых шлюзов (Border Gateway Protocol)",
    "Ldap": "Lightweight Directory Access Protocol (протокол доступа к каталогам)",
    "Ecr_i": "ECR I (протокол информационного обмена)",
    "Gopher": "Протокол поиска информации в интернете",
    "Vmnet": "Виртуальная сеть",
    "Systat": "Протокол системного состояния",
    "HTTP_443": "Протокол передачи гипертекста (зашифрованный)",
    "Efs": "Encrypting File System (система зашифрованных файлов)",
    "Whois": "Протокол определения информации о домене",
    "Imap4": "Internet Message Access Protocol version 4 (протокол доступа к почте)",
    "Iso_tsap": "ISO TSAP (протокол простого доступа к транспортному уровню)",
    "Echo": "Сетевая служба эха",
    "Klogin": "Протокол входа в систему Kerberos",
    "Link": "Протокол установления линка",
    "Sunrpc": "Sun Remote Procedure Call (удаленный вызов процедур Sun)",
    "Login": "Сетевая служба входа в систему",
    "Kshell": "Протокол оболочки Kerberos",
    "Sql_net": "SQL*NET (протокол баз данных Oracle)",
    "Time": "Сетевая служба времени",
    "Hostnames": "Сетевые имена",
    "Exec": "Сетевая служба выполнения команд",
    "Ntp_u": "Протокол времени Network Time Protocol (не аутентифицированный)",
    "Discard": "Сетевая служба отбрасывания",
    "Nntp": "Протокол передачи новостей Network News Transfer Protocol",
    "Courier": "Сетевая служба курьера",
    "Ctf": "Чистый текст FTP (FTP без шифрования)",
    "Ssh": "Secure Shell (защищенный канал связи)",
    "Daytime": "Сетевая служба времени суток",
    "Shell": "Сетевая служба командной оболочки",
    "Netstat": "Сетевая служба статистики",
    "Pop_3": "Post Office Protocol version 3 (протокол доступа к почте)",
    "Nnsp": "Протокол управления новостным сервером",
    "Irc": "Internet Relay Chat (протокол интернет-чата)",
    "Pop_2": "Post Office Protocol version 2 (протокол доступа к почте)",
    "Printer": "Протокол печати",
    "Tim_i": "Tim_i (неизвестный протокол)",
    "Pm_dump": "PM Dump (протокол удаленного дампа)",
    "Red_i": "Red_i (неизвестный протокол)",
    "Netbios_ssn": "NetBIOS Session Service (сетевая служба сеанса NetBIOS)",
    "Rje": "Remote Job Entry (удаленный ввод задач)",
    "X11": "X Window System (система оконного интерфейса)",
    "Urh_i": "Urh_i (неизвестный протокол)",
    "HTTP_8001": "Протокол передачи гипертекста (пользовательский)",
    "Aol": "America Online (протокол онлайн-сервиса)",
    "HTTP_2784": "Протокол передачи гипертекста (пользовательский)",
    "Tftp_u": "Trivial File Transfer Protocol (протокол передачи небольших файлов)",
    "Harvest": "Harvest (неизвестный протокол)"

    # Add more service types here
}

for service, description in service_types.items():
    st.markdown(f"- **{service}:** {description}")

# Flag Types
st.subheader("ТИПЫ ФЛАГОВ")
st.markdown("Флаг обычно относится к определенному биту или набору битов в заголовке сетевого протокола, который указывает на определенный статус или управляющую информацию.")
flag_types = {
    "SF": "Соединение успешно установлено и завершено",
    "S0": "Нет ответа от пункта назначения (скрытая проверка)",
    "REJ": "Запрос на подключение отклонен",
    "RSTR": "Сброс соединения пунктом назначения",
    "SH": "Соединение прервано (отправлено RST)",
    "RSTO": "Сброс соединения пунктом назначения",
    "S1": "Сканирование с низкой частотой сканирования",
    "RSTOS0": "Сброс соединения с нулевыми байтами (отправлено RST)",
    "S3": "Сканирование с высокой частотой сканирования",
    "S2": "Сканирование с средней частотой сканирования",
    "OTH": "Другие типы пакетов",
}

for flag, description in flag_types.items():
    st.markdown(f"- **{flag}:** {description}")

# Attack Types
st.subheader("ТИПЫ СЕТЕВЫХ АТАК")

attack_types = {
    "DoS (Denial of Service)": "Атаки этого класса направлены на затруднение или прекращение доступа к ресурсам системы для легальных пользователей. Включает в себя различные типы атак, такие как атаки на уровне сетевых протоколов (например, smurf, teardrop) и атаки на уровне приложений (например, apache2).",

    "Probe (Probe)": "Эти атаки направлены на исследование уязвимостей в сети и системах. Проникновение в систему не происходит, но злоумышленник собирает информацию для последующих атак. Примеры включают в себя атаки типа сканирования портов (например, nmap, portsweep) и сканирование уязвимостей (например, satan, ipsweep).",

    "R2L (Remote-to-Local)": "Эти атаки происходят, когда злоумышленник пытается получить доступ к локальной системе из удаленной сети. Примеры включают в себя атаки на подбор паролей (например, guess_passwd), атаки на удаленные уязвимости (например, ftp_write, sendmail) и атаки на идентификацию (например, snmpguess, named).",

    "U2R (User-to-Root)": "Эти атаки пытаются получить привилегированный доступ к системе от имени обычного пользователя. Примеры включают в себя атаки на переполнение буфера (например, buffer_overflow), использование уязвимостей при загрузке модулей (например, loadmodule) и атаки с использованием программных уязвимостей (например, perl, sqlattack).",
}

for attack, description in attack_types.items():
    st.markdown(f"- **{attack}:** {description}")


st.subheader("рекомендации по предотвращению".upper())

recommendation = {
    "DoS (Denial of Service)": ["Использование межсетевых экранов (firewalls): Настройка межсетевых экранов для фильтрации и блокировки подозрительного трафика.", "Мониторинг трафика: Использование систем мониторинга для выявления аномального трафика и атак в реальном времени.", "Сетевые решения: Внедрение систем распределения нагрузки (load balancers) и сервисов по смягчению DoS атак, таких как Content Delivery Networks (CDN)."],

    "Probe (Probe)": ["Регулярные сканирования безопасности: Выполнение регулярных сканирований безопасности для выявления и устранения уязвимостей.", "Обновление программного обеспечения: Обновление всех программных и аппаратных компонентов для защиты от известных уязвимостей.", "Сегментация сети: Разделение сети на сегменты для ограничения распространения атак."],

    "R2L (Remote-to-Local)": ["Многофакторная аутентификация (MFA): Внедрение многофакторной аутентификации для защиты учетных записей.", "Сильные пароли: Использование сложных и уникальных паролей для каждой учетной записи.", "Антивирусное ПО: Установка и регулярное обновление антивирусного программного обеспечения для обнаружения и удаления вредоносных программ."],

    "U2R (User-to-Root)": ["Ограничение прав пользователей: Минимизация прав пользователей и использование принципа наименьших привилегий.", "Обновление системы: Регулярное обновление операционной системы и всех приложений для устранения уязвимостей.", "Мониторинг логов: Активный мониторинг логов системы для выявления подозрительной активности и несанкционированных попыток получения прав суперпользователя."],
}

for attack, description in recommendation.items():
    st.markdown(f"**{attack}:**")
    for desc in description:
        st.markdown(f"- {desc}")
