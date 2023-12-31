from PIL import Image, ImageDraw, ImageFont
from email_validator import validate_email, EmailNotValidError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import pandas as pd
import re
import smtplib
import csv
import sys

def validation_check(email):
    try:
        email = validate_email(email)
        return True
    except EmailNotValidError as e:
        print(f"for email {email} the error is: {str(e)}")

def send_email(subject, body, to_email, cert_path, address, student_name):
    message = MIMEMultipart()
    message['From'] = address
    message['To'] = to_email
    message['Subject'] = subject

    with open(cert_path, 'rb') as attachment:
        certificate = MIMEImage(attachment.read(), _subtype='jpeg', name='HourOfCode2023_certificate.jpg')
    message.attach(certificate)
    message.attach(MIMEText(body, 'plain'))

    try:
        server.sendmail(address, to_email, message.as_string())
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [student_name, to_email, timestamp]
        
        with open(good_log_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)
            
        print("SENT EMAIL")
        
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [student_name, to_email, timestamp]
        
        with open(bad_log_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)
            
            
        print("                      ")
        print("THE EMAIL WAS NOT SENT")
        print("                      ")
        print({e})
    
def generate_certificate(input_image_path, output_image_path, name, email_address, addr, index):
    try:
        initCertificateImage = Image.open(input_image_path)
        drawCertificate = ImageDraw.Draw(initCertificateImage)
        
    except Exception:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [input_image_path, email_address, timestamp]
        
        with open(bad_log_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)
        
        pass
    
    index = index + 1
    index = str(index)
    
    index_str = f"HoC-2023-0000{index}"  
    
    if int(index) >= 10 and int(index) < 100:
        index_str = f"HoC-2023-000{index}"  
    elif int(index) >= 100 and int(index) < 1000:
        index_str = f"HoC-2023-00{index}"
    elif int(index) >= 1000:
        index_str = f"HoC-2023-0{index}"
    
    certificateFont = ImageFont.truetype('./font/FreeMono.ttf', 80)
    longCertificateFont = ImageFont.truetype('./font/FreeMono.ttf', 25)
    intermediateCertificateFont = ImageFont.truetype('./font/FreeMono.ttf', 70)
    indexFont = ImageFont.truetype('./font/FreeMono.ttf', 80)
    
    if len(name) < 7:
        drawCertificate.text((2200, 1420), name, font=certificateFont, fill=(255, 0, 0))
        drawCertificate.text((2750, 2350), index_str, font=indexFont, fill=(255, 0, 0))
        
    elif len(name) > 6 and len(name) < 10:
        drawCertificate.text((2150, 1420), name, font=certificateFont, fill=(255, 0, 0))
        drawCertificate.text((2750, 2350), index_str, font=indexFont, fill=(255, 0, 0))
 
    elif len(name) > 9 and len(name) < 13: 
        drawCertificate.text((2050, 1420), name, font=certificateFont, fill=(255, 0, 0))
        drawCertificate.text((2750, 2350), index_str, font=indexFont, fill=(255, 0, 0))
        
    elif len(name) > 12 and len(name) < 20:
        drawCertificate.text((1870, 1420), name, font=certificateFont, fill=(255, 0, 0))
        drawCertificate.text((2750, 2350), index_str, font=indexFont, fill=(255, 0, 0))
        
    elif len(name) >= 20 and len(name) < 26:
        drawCertificate.text((1800, 1420), name, font=certificateFont, fill=(255, 0, 0))
        drawCertificate.text((2750, 2350), index_str, font=indexFont, fill=(255, 0, 0))
        
    elif len(name) >= 26 and len(name) < 33:
        drawCertificate.text((1740, 1420), name, font=certificateFont, fill=(255, 0, 0))
        drawCertificate.text((2750, 2350), index_str, font=indexFont, fill=(255, 0, 0))
        
    elif len(name) >= 33 and len(name) < 40:
        drawCertificate.text((1660, 1420), name, font=intermediateCertificateFont, fill=(255, 0, 0))
        drawCertificate.text((2750, 2350), index_str, font=indexFont, fill=(255, 0, 0))

    elif len(name) >= 40:
        drawCertificate.text((1590, 1465), name, font=longCertificateFont, fill=(255, 0, 0))
        drawCertificate.text((2750, 2350), index_str, font=indexFont, fill=(255, 0, 0))

    try:
        initCertificateImage.save(output_image_path)
        
    except Exception:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [input_image_path, email_address, timestamp]
        
        with open(bad_log_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)
        
        pass
    
    send_email(email_subject, email_body, email_address, output_image_path, addr, name)

if __name__ == "__main__":
    DF = pd.read_excel("/Users/daniyarkakimbekov/Workspaces/HoC2023_DataAnalytics/teachers.xlsx")
    bad_log_path = "/Users/daniyarkakimbekov/Workspaces/HoC2023_CertificateGenerator/bad_teacher_emails.csv"
    good_log_path = "/Users/daniyarkakimbekov/Workspaces/HoC2023_CertificateGenerator/good_teacher_emails.csv"
    
    limit = 594
    
    DF = DF[limit:]
    
    # Credentials order: smtp_server, smtp_login, smtp_password
    credentials = [
                    "mail.hourofcode.kz", "hoc2023certificates1@hourofcode.kz", "absorbantReverer17", 
                    "mail.studycs.kz", "hoc2023certificates1@studycs.kz", "qwerasdzx19!",
                    # "smtp.gmail.com", "daniyar@ustemrobotics.kz", "afos vsor ermk crua",
                    "smtp.yandex.ru", "Olympics@steptoenglish.org", "Step4ever!"
                   ]
    
    email_body = """
    
Дорогой учитель, вас приветствует команда Час Кода Казахстан!

С 4 по 10 декабря мы проводили самую масштабную акцию по программированию для учащихся 5 - 11 классов в Казахстане.
Благодарим вас за ваш вклад в нашу общую цель!
В качестве подтверждения отправляем официальный именной сертификат учителя.

Организаторы акции:
✅ USTEM Foundation. https://firstrobotics.kz/first-kaz
✅ StudySC

Партнеры:
✅ Республиканский научно-практический центр «Дарын» Министерства просвещения Республики Казахстан https://daryn.kz/о-центре/
✅ Step Europe s.r.o. https://steptoenglish.org/

Хочешь стать частью нашей команды?
Пиши в директ нашей официальной страницы в Instagram - @hourofcode.kz

Бұл электрондық пошта автоматты түрде жасалды. Жауап бермеңіз.
Это письмо было сгенерировано автоматически. Пожалуйста, не отвечайте на него.
    """
    email_subject = "Код Сағаты 2023 / Час Кода 2023. Сертификат учителя."
    
    for n in range(0,len(credentials), 3):
        
        smtp_server = credentials[n]
        smtp_login = credentials[n+1]
        smtp_password = credentials[n+2]
        
        
        print("-------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------")
        print(f"STARTING EMAILING PROCESS FOR CREDENTIALS: {smtp_server}, {smtp_login}, {smtp_password}")
        print("-------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------")
        
        with smtplib.SMTP_SSL(smtp_server, 465) as server:
                server.login(smtp_login, smtp_password)
                print("did login")
                
                for i in range(0, 500):
                    
                    index = limit+i
                    
                    name = str(DF["name"][index]).lower().split()
                    capitalized_strings = [s.capitalize() for s in name]
                    name = ' '.join(capitalized_strings)
                    
                    participant_email = str(DF["email"][index]).replace(" ", "")
                    
                    if validation_check(participant_email):
                        language = "kazakh"
                
                        name_for_path_dirty = str(DF["name"][index])
                        patterns_to_remove = ['https://www.', '/', ',', '&', '^', '%', '$', '#', '.', '-', '+', ' ']
                        pattern = '|'.join(re.escape(p) for p in patterns_to_remove)
                        name_for_path = re.sub(pattern, '', name_for_path_dirty)
                        
                        certificate_path = "".join(["./templates/kazakh/teacher.jpg"])
                        
                        output_path = "".join(["./certificates/teacher/", name_for_path, ".jpeg"])
                        
                        print(f"starting process for user number {i}, email {participant_email}, name {name}")
                        generate_certificate(certificate_path, output_path, name, participant_email, smtp_login, index)
                        
                    else: 
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        row = [name, participant_email, timestamp]
                        
                        with open(bad_log_path, 'a', newline='') as csv_file:
                            csv_writer = csv.writer(csv_file)
                            csv_writer.writerow(row)

                server.quit()
            
            
        print("-------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------")
        print(f"current limit: {limit}")
        limit = limit + 500
        print(f"NEW LIMIT: {limit}")
        print("-------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------")
        
    

    print("*********************************************************")
    print("****************FINISHED SENDING MAIL********************")
    print("*********************************************************")
