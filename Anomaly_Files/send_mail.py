import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(choice, receiver_login, receiver_email, receiver_password):
    # Email configuration
    smtp_server = 'smtp-relay.brevo.com'
    smtp_port = 587
    sender_email = 'okorejoellots@gmail.com'
    receiver_email = receiver_email.strip()
    password = 'U3OGPFgME9dnVkrC'

    # Create the email content
    
    if choice == 1:
        subject = 'РЕГИСТРАЦИЯ ПРОШЛА УСПЕШНО'
        body = f"""
        Дорогой пользователь,

        Вы успешно зарегистрировались на сайте Казанского национального исследовательского технологического университета по обнаружению аномалий.

        ===>>>-----------------------------------------------
        Ваш логин: {receiver_login}
        Ваш пароль: {receiver_password}
        ===>>>-----------------------------------------------
        
        Если у вас возникнут какие-либо вопросы или проблемы, свяжитесь с нами по адресу okorejoellots@gmail.com.

        Лучший,
        Команда по обнаружению сетевых аномалий - ФГБОУ ВО «КНИТУ»"""
    if choice == 2:
        subject = 'ЗАПОМИНАНИЕ ПАРОЛЯ'
        body = f"""
        Вы запросили напоминание пароля для доступа к вашему профилю на сайте Казанского национального исследовательского технологического университета по обнаружению аномалий.
        
        ===>>>-----------------------------------------------
        Ваш логин: {receiver_login}
        Ваш пароль: {receiver_password}
        ===>>>-----------------------------------------------

        Если у вас возникнут какие-либо проблемы при входе в свою учетную запись, свяжитесь с нами по адресу okorejoellots@gmail.com.
        
        Лучший,
        Команда по обнаружению сетевых аномалий - ФГБОУ ВО «КНИТУ»"""



    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = 'okorejoellots@gmail.com'
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server and log in
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()  # Secure the connection
        server.login(sender_email, password)
        
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Terminate the SMTP session and close the connection
        server.quit()
