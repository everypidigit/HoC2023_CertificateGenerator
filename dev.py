from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(subject, body, to_email, cert_path, vouch_path):
    message = MIMEMultipart()
    message['From'] = sender_email
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
        server.sendmail(sender_email, to_email, message.as_string())
    except Exception:
        bad_emails.append(to_email)
        print(f"appended {to_email} to bad)emails")
        pass
    print(f"email sent to {to_email}")

def generate_certificate(input_image_path, voucher_path, output_image_path, output_voucher_path, text_to_add, email_address):
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
    
    
    send_email(email_subject, email_body, email_address, output_image_path, output_voucher_path)
        
if __name__ == "__main__":
    DF = pd.read_csv("/Users/daniyarkakimbekov/Workspaces/try/dec5.csv")
    
    emails = []

    for i in range(1, 51):
        emails.append(f"hoc2023certificates{i}@hourofcode.kz")
    
    limit = 1652
    
    DF = DF[limit:]
    smtp_server = 'smtp.gmail.com'
    sender_email = "daniyar@ustemrobotics.kz"  
    sender_password = "afos vsor ermk crua"
    
    global bad_emails
    bad_emails = []
    email_body = """
    
Дорогой друг тебя приветствует команда Час Кода Казахстан.

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
    email_subject = "Код Сағаты 2023 / Час Кода 2023. Сертификат. "
    with smtplib.SMTP_SSL(smtp_server, 465) as server:
        server.login(sender_email, sender_password)
        for i in range(limit,len(DF)):
            role = str(DF["role"][i]).replace(" ", "")
            language = str(DF["language"][i]).replace(" ", "")
            
            name = str(DF["name"][i]).lower().split()
            capitalized_strings = [s.capitalize() for s in name]
            name = ' '.join(capitalized_strings)
        
            name_for_path_dirty = str(DF["name"][i])
            patterns_to_remove = ['https://www.', '/', ',', '&', '^', '%', '$', '#', '.']
            pattern = '|'.join(re.escape(p) for p in patterns_to_remove)
            name_for_path = re.sub(pattern, '', name_for_path_dirty)
            
            participant_email = str(DF["email"][i]).replace(" ", "")
            
            if language == "english" or role == "teacher" or role == "volunteer":
                pass
            
            else:
                certificate_path = "".join(["./", language, "/", role, ".jpg"])
                voucher_path = "".join(["./", language, "/voucher.jpg"])
                
                output_path = "".join(["./certificates/",role, "/", name_for_path, ".jpeg"])
                out_voucher_path = "".join(["./certificates/",role, "/", name_for_path, "_Voucher.jpeg"])
                
                print(f"starting process for user number {i}")
                generate_certificate(certificate_path, voucher_path, output_path, out_voucher_path, name, participant_email)

    server.quit()
    print(bad_emails)
    print("FINISHED THE WHOLE PROCESS")