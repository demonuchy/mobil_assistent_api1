import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройки
smtp_server = 'smtp.gmail.com'  # SMTP-сервер вашего почтового провайдера
smtp_port = 587                     # Порт (обычно 587 для TLS)
sender_email = 'demonuchy@gmail.com'  # Ваш email
receiver_email = 'mssrv92@gmail.com'  # Email получателя
password = 'D2i0m0a51966!'          # Ваш пароль

# Создание сообщения
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = 'Тема сообщения'

# Текст сообщения
body = 'Это тело сообщения.'
msg.attach(MIMEText(body, 'plain'))

try:
    # Подключение к серверу и отправка сообщения
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Начало защищенного соединения
    server.login(sender_email, password)  # Вход в почтовый ящик
    server.send_message(msg)  # Отправка сообщения
    print('Сообщение успешно отправлено')
except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    server.quit()  # Закрытие соединения
