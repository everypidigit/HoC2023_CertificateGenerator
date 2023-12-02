from PIL import Image, ImageFont, ImageDraw

import pandas as pd
import xlrd
import datetime 

import smtplib                                      # Импортируем библиотеку по работе с SMTP
import os.path
import mimetypes
import email.encoders
import re
# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.base import MIMEBase                # Общий тип
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.image import MIMEImage              # Изображения
from email.mime.application import MIMEApplication
from pathlib import Path
#import exel file 
df = pd.read_excel("lists/Nauryz_contest_4th_grade.xlsx", "Статистика") #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#list of names should be in 'names' column
imya = df['Укажите имя на английском языке.'].values.tolist()
familiya = df['Укажите фамилию на английском языке.'].values.tolist()
names = [" "]
#list of ids should be in 'id' column
ids = df['№'].values.tolist()
#list of procents should be in 'percent' column
procents =  df['Процент правильных ответов (%)'].values.tolist()

i=1
while i<len(imya):
    names.append(imya[i].capitalize()+" "+familiya[i].capitalize())
    print(i)
    i+=1

    
addr_from = "Olympics@steptoenglish.org"                 # Адресат
password  = "Step2004"                                  # Пароль
addr_to = df['Укажите e-mail адрес, куда мы сможем отправить сертификат.'].values.tolist()


#converting procents from str to float 
i = 1
while i< len(procents):
    if isinstance(procents[i], int):
        xx =  float(procents[i])
    elif isinstance(procents[i], datetime.datetime):
        xx = 0
    elif isinstance(procents[i], float):
        xx = procents[i]
    elif(',' in procents[i]):
        xx =  float(procents[i].replace(',', '.'))
    
    print (xx)

    procents[i] = xx
    i = i+1
print (procents)



        

i = 1
while i< len(names):
    html = """"""
    if procents[i]>=90:
        #choosing path to gold certificate
        image = Image.open("gold.jpg")
    elif procents[i]>=75:
        #choosing path to silver certificate
        image = Image.open("silver.jpg")
    elif procents[i]>=60:
        #choosing path to bronze certificate
        image = Image.open("bronze.jpg")
    else:
        #choosing path to blue certificate
        image = Image.open("blue.jpg")
    
    font_type = ImageFont.truetype("Roboto/Roboto-Light.ttf",size=65)
    draw = ImageDraw.Draw(image)
    W, H = (1240,200)
    w, h = draw.textsize(names[i])
    print (names[i])
    draw.text(xy = (1120-(1.35*w),930), text = names[i], fill = "black", font = font_type)
    #choosing font 
    font_type_grade = ImageFont.truetype("Roboto/Roboto-Light.ttf", size=55)
    
    draw.text(xy = (1220,1125), text = '4', fill = "black", font = font_type_grade) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    draw.text(xy = (720,1125), text = str(int(procents[i])), fill = "black", font = font_type_grade)
    draw.text(xy = (195,1540), text = '№ '+ str(int(ids[i])), fill = "black", font = font_type_grade)
    #saving image in the right location
    image.save("sertificates/4/" + names[i] + ".jpg") #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
    try:
        file = "sertificates/4/" + names[i] + ".jpg" #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        filename = os.path.basename(file)
        print(filename, file)
        
        
        msg = MIMEMultipart()                               # Создаем сообщение
        msg['From']    = addr_from                          # Адресат
        msg['To']      = addr_to[i]                            # Получатель
        msg['Subject'] = names[i]+"'s certificate"                   # Тема сообщения


        html = """\
        <!DOCTYPE html>
        <html>
        <body>
            <img width=800 src="cid:image1" alt="STEP Olympics">
            
            <h3 style="text-align:center;color:black">
                Дорогой друг тебя приветствует школа английского языка Step to English!
            </h3>
            <p>
                Мы подвели итоги весенней олимпиады по английскому <b>Step Olympics</b> посвященной празднику Наурыз, поэтому спешим отправить лично сертификат участника прямиком из нашего европейского офиса в Праге (Чехия).
            </p>
            <p>
                Результаты всех участников Step Olympics опубликованы по ссылке - <a href="https://steptoenglish.org/news" rel="details" target="_blank">https://steptoenglish.org/news</a>
            </p>
            <p>
                Обладателей золотых сертификатов мы приглашаем <b>1 апреля</b> к участию в розыгрыше подарков от компании Burger King и Step to English. 
            </p>
            <p>
                Место проведения розыгрыша в прямом эфире нашего Инстаграм - <b>@step_to_english</b> 1 апреля. Подписывайтесь на нас, чтобы не упустить розыгрыш.
            </p>
            <p>
                <strong>Уникальность Step to English:</strong>
            </p>
            <ul>
                <li>офлайн и онлайн английский для всех возрастов, заказать бесплатный урок - <a href="https://steptoenglish.org/online-test" rel="details" target="_blank">https://steptoenglish.org/online-test</a>;</li>
                <li>собственное мобильное приложение «Step to English» для эффективного обучения английскому для iPhone и Android устройств можно скачать по ссылке - <a href="https://steptoenglish.org/app" rel="details" target="_blank">https://steptoenglish.org/app</a>;</li>
                <li>собственный онлайн маркет для обучающихся в нашей школе, ссылка - <a href="https://steptoenglish.org/market" rel="details" target="_blank">https://steptoenglish.org/market</a>;</li>
                <li>школа программирования Love to Code, заказать бесплатный урок - <a href="https://steptoenglish.org/coding-and-robotics" rel="details" target="_blank">https://steptoenglish.org/coding-and-robotics</a>;</li>
                <li style="background-color:yellow">Летние каникулы в Лондоне в июле 2022 года - <a href="https://steptoenglish.org/language-tours/england" rel="details" target="_blank">https://steptoenglish.org/language-tours/england</a>;</li>
                <li style="background-color:yellow">Высшее образование в Чехии - <a href="https://steptoenglish.org/language-tours/czech" rel="details" target="_blank">https://steptoenglish.org/language-tours/czech</a>.</li>
            </ul>
            <br>
            <p>
                Единый контакный номер по Казахстану - <b>8(775)8849681</b>
            </p>
            <p>
                По вопросам сотрудничества просьба обращаться - <a href="mailto:eu@steptoenglish.org">eu@steptoenglish.org</a>
            </p>
            <p>
                Всегда твой - Step to English!
            </p>
        </body>
        </html>
        """
        
        
        
        msg.attach(MIMEText(html, 'html', 'utf-8'))         # Добавляем в сообщение HTML-фрагмент

        File1 = 'D:\Abay\scriptSert\oblozhka_fb_olimpiada2.jpg'
        image = MIMEImage(open(File1,'rb').read(),File1.split('.')[-1])
        # Определите идентификатор изображения, ссылку в HTML Text
        image.add_header('Content-ID','<image1>')
        msg.attach(image)
        print(1)

        if os.path.isfile(file):                              # Если файл существует
            ctype, encoding = mimetypes.guess_type(file)        # Определяем тип файла на основе его расширения
            if ctype is None or encoding is not None:               # Если тип файла не определяется
                ctype = 'application/octet-stream'                  # Будем использовать общий тип
            maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
            with open(file, 'rb') as fp:
                file2 = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
                file2.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                email.encoders.encode_base64(file2)                        # Содержимое должно кодироваться как Base64
            file2.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
            msg.attach(file2)                                        # Присоединяем файл к сообщению
        print(2)
        
        server = smtplib.SMTP_SSL('smtp.yandex.ru',465)          # Создаем объект SMTP
        #server.set_debuglevel(True)                         # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
        #server.starttls()                                   # Начинаем шифрованный обмен по TLS
        print(3)
        server.login(addr_from, password)                   # Получаем доступ
        print(4)
        server.send_message(msg)                            # Отправляем сообщение
        print(5)
        server.quit()                                       # Выходим
        print("---success---"+addr_to[i]+"---")

    except:
        print("!!!!!!!!!!!!!!!!!!!!!!FAIL "+addr_to[i]+"---"+file+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    i+=1
