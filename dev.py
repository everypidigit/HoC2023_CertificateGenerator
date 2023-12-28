from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import csv
from datetime import datetime
import sys
from email_validator import validate_email, EmailNotValidError

def validation_check(email):
    try:
        email = validate_email(email)
        return True
    except EmailNotValidError as e:
        print(f"for email {email} the error is: {str(e)}")

def send_email(subject, body, to_email, cert_path, vouch_path, address, student_name):
    
    # test_email = "heethesee@gmail.com"
    
    message = MIMEMultipart()
    message['From'] = address
    message['To'] = to_email
    message['Subject'] = subject

    with open(cert_path, 'rb') as attachment:
        certificate = MIMEImage(attachment.read(), _subtype='jpeg', name='HourOfCode2023_certificate.jpg')
    with open(vouch_path, 'rb') as attachment:
        voucher = MIMEImage(attachment.read(), _subtype='jpeg', name='Voucher.jpg')
    message.attach(certificate)
    message.attach(voucher)

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
    
def generate_certificate(input_image_path, voucher_path, output_image_path, output_voucher_path, text_to_add, email_address, addr):
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
    
    initVoucherImage = Image.open(voucher_path)
    drawVoucher = ImageDraw.Draw(initVoucherImage)
    
    certificateFont = ImageFont.truetype('./font/FreeMono.ttf', 120)
    voucherFont = ImageFont.truetype('./font/FreeMono.ttf', 80)
    
    if len(text_to_add) < 7:
        drawCertificate.text((2200, 1390), text_to_add, font=certificateFont, fill=(255, 0, 0))
        drawVoucher.text((430, 1320), text_to_add, font=voucherFont, fill=(0, 0, 0))
        
    elif len(text_to_add) > 6 and len(text_to_add) < 10:
        drawCertificate.text((2150, 1390), text_to_add, font=certificateFont, fill=(255, 0, 0))
        drawVoucher.text((380, 1320), text_to_add, font=voucherFont, fill=(0, 0, 0))
        
    elif len(text_to_add) > 9 and len(text_to_add) < 13: 
        drawCertificate.text((2050, 1390), text_to_add, font=certificateFont, fill=(255, 0, 0))
        drawVoucher.text((300, 1320), text_to_add, font=voucherFont, fill=(0, 0, 0))
        
    elif len(text_to_add) > 12:
        drawCertificate.text((1850, 1390), text_to_add, font=certificateFont, fill=(255, 0, 0))
        drawVoucher.text((220, 1320), text_to_add, font=voucherFont, fill=(0, 0, 0))

    original_width, original_height = initCertificateImage.size
    new_width = int(original_width * 0.3)
    new_height = int(original_height * 0.3)    
    initCertificateImage = initCertificateImage.resize((new_width, new_height))
    
    original_width, original_height = initVoucherImage.size
    new_width = int(original_width * 0.3)
    new_height = int(original_height * 0.3)    
    initVoucherImage = initVoucherImage.resize((new_width, new_height))
    
    try:
        initCertificateImage.save(output_image_path)
        initVoucherImage.save(output_voucher_path)
        
    except Exception:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [input_image_path, email_address, timestamp]
        
        with open(bad_log_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)
        
        pass
    
    send_email(email_subject, email_body, email_address, output_image_path, output_voucher_path, addr, text_to_add)
        
if __name__ == "__main__":
    DF = pd.read_csv("./data/clean_final.csv")
    bad_log_path = "./bad_email.csv"
    good_log_path = "./good_email.csv"
    
    limit = 23105
    
    DF = DF[limit:]
    
    # Credentials order: smtp_server, smtp_login, smtp_password
    credentials = ["mail.hourofcode.kz", "hoc2023certificates1@hourofcode.kz", "absorbantReverer17", 
              "mail.studycs.kz", "hoc2023certificates1@studycs.kz", "qwerasdzx19!", 
              'smtp.gmail.com', "daniyar@ustemrobotics.kz", "afos vsor ermk crua"]
    
    email_body = """
    
Дорогой друг, тебя приветствует команда Час Кода Казахстан.

С 4 по 10 декабря мы проводим самую масштабную акцию по программированию для учащихся 5 - 11 классов в Казахстане.
Благодарим тебя за участие и успешное прохождение заданий.
В качестве подтверждения отправляем официальный именной сертификат участника, а также в знак нашей признательности вручаем тебе лимитированный ваучер на обучение в школе английского Step.

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
    email_subject = "Код Сағаты 2023 / Час Кода 2023. Сертификат"
    
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
                
                for i in range(0, 500):
                    
                    index = limit+i
                    
                    name = str(DF["name"][index]).lower().split()
                    capitalized_strings = [s.capitalize() for s in name]
                    name = ' '.join(capitalized_strings)
                    
                    participant_email = str(DF["email"][index]).replace(" ", "")
                    
                    if validation_check(participant_email):
                        role = str(DF["role"][index]).replace(" ", "")
                        language = str(DF["language"][index]).replace(" ", "")
                    
                        if role == "teacher" or role == " teacher" or role == "volunteer" or role == " volunteer":
                            pass
                        
                        if language == "english":
                            language = "kazakh"
                
                        name_for_path_dirty = str(DF["name"][index])
                        patterns_to_remove = ['https://www.', '/', ',', '&', '^', '%', '$', '#', '.', '-', '+']
                        pattern = '|'.join(re.escape(p) for p in patterns_to_remove)
                        name_for_path = re.sub(pattern, '', name_for_path_dirty)
                        
                        certificate_path = "".join(["./templates/", language, "/", role, ".jpg"])
                        voucher_path = "".join(["./templates/", language, "/voucher.jpg"])
                        
                        output_path = "".join(["./certificates/",role, "/", name_for_path, ".jpeg"])
                        out_voucher_path = "".join(["./certificates/",role, "/", name_for_path, "_Voucher.jpeg"])
                        
                        print(f"starting process for user number {i}, email {participant_email}, name {name}")
                        generate_certificate(certificate_path, voucher_path, output_path, out_voucher_path, name, participant_email, smtp_login)
                        
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
        print("-------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------")
        limit = limit + 500
        
    

    print("*********************************************************")
    print("****************FINISHED SENDING MAIL********************")
    print("*********************************************************")
