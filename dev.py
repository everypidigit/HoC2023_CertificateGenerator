from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(subject, body, to_email, cert_path, vouch_path, address, student_name):
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
        file = open(log_path, 'a')
        file.write(f"sent email to {to_email} | {student_name}" + '\n')
        file.close()
        
    except Exception:
        file = open(log_path, 'a')
        file.write(f"bad email {to_email} | {student_name}" + '\n')
        file.close()
        
        pass
    

def generate_certificate(input_image_path, voucher_path, output_image_path, output_voucher_path, text_to_add, email_address, addr):
    initCertificateImage = Image.open(input_image_path)
    drawCertificate = ImageDraw.Draw(initCertificateImage)
    
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
    
    initCertificateImage.save(output_image_path)
    initVoucherImage.save(output_voucher_path)
    
    send_email(email_subject, email_body, email_address, output_image_path, output_voucher_path, addr, text_to_add)
        
if __name__ == "__main__":
    DF = pd.read_csv("/Users/daniyarkakimbekov/Workspaces/try/dec5.csv")
    
    limit = 1653    
    
    DF = DF[limit:]

    user = "hoc2023certificates1@hourofcode.kz"
    password = "Rapture9949!"
    smtp_server = "mail.hourofcode.kz"
    
    log_path = "./log.txt"
    
    email_body = """
    
Дорогой друг, тебя приветствует команда Час Кода Казахстан.

С 4 по 10 декабря мы проводим самую масштабную акцию по программированию для учащихся 5 - 11 классов в Казахстане.
Благодарим тебя за участие и успешное прохождение заданий.
В качестве подтверждения отправляем официальный именной сертификат участника, а также в знак нашей признательности вручаем тебе лимитированный ваучер на обучение в школе английского Step.

Организаторы акции:
✅ USTEM Foundation. https://firstrobotics.kz/first-kaz
✅StudySC

Партнеры:
✅Республиканский научно-практический центр «Дарын» Министерства просвещения Республики Казахстан https://daryn.kz/о-центре/
✅Step Europe s.r.o. https://steptoenglish.org/

Хочешь стать частью нашей команды?
Пиши в директ нашей официальной страницы в Instagram - @hourofcode.kz
    
    """
    email_subject = "Код Сағаты 2023 / Час Кода 2023. Сертификатw"
    
    with smtplib.SMTP_SSL(smtp_server, 465) as server:
            server.login(user, password)
            
            for i in range(271,500):
                index = limit+i
                role = str(DF["role"][index]).replace(" ", "")
                language = str(DF["language"][index]).replace(" ", "")
                
                if language == "english" or role == "teacher" or role == "volunteer":
                    pass
                
                name = str(DF["name"][index]).lower().split()
                capitalized_strings = [s.capitalize() for s in name]
                name = ' '.join(capitalized_strings)
            
                name_for_path_dirty = str(DF["name"][index])
                patterns_to_remove = ['https://www.', '/', ',', '&', '^', '%', '$', '#', '.']
                pattern = '|'.join(re.escape(p) for p in patterns_to_remove)
                name_for_path = re.sub(pattern, '', name_for_path_dirty)
                
                participant_email = str(DF["email"][index]).replace(" ", "")
                
                certificate_path = "".join(["./", language, "/", role, ".jpg"])
                voucher_path = "".join(["./", language, "/voucher.jpg"])
                
                output_path = "".join(["./certificates/",role, "/", name_for_path, ".jpeg"])
                out_voucher_path = "".join(["./certificates/",role, "/", name_for_path, "_Voucher.jpeg"])
                
                print(f"starting process for user number {i}")
                generate_certificate(certificate_path, voucher_path, output_path, out_voucher_path, name, participant_email, user)
    
    server.quit()
