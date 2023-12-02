from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(subject, body, to_email, attachment_path):
    sender_email = "everypidigit@gmail.com"  
    sender_password = "lili qgkh zlnr apsy"
    smtp_server = 'smtp.gmail.com'  

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    with open(attachment_path, 'rb') as attachment:
        image = MIMEImage(attachment.read(), _subtype='jpeg', name='HourOfCode2023_certificate.jpg')
    message.attach(image)

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL(smtp_server, 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()

def generate_certificate(input_image_path, output_image_path, text_to_add, email_address):
    initImage = Image.open(input_image_path)
    draw = ImageDraw.Draw(initImage)
    myFont = ImageFont.truetype('./font/FreeMono.ttf', 120)
    
    # the location for printing is chosen as absolute pixels, so gotta make some wraparound so that
    # everything's printed beautifully
    # location for printing text is chosen based on the length of the name:
    # shorter names will be printed closer to the absolute center, etc
    if len(text_to_add) < 7:
        draw.text((2200, 1390), text_to_add, font=myFont, fill=(255, 0, 0))
        
    elif len(text_to_add) > 6 and len(text_to_add) < 10:
        draw.text((2150, 1390), text_to_add, font=myFont, fill=(255, 0, 0))
        
    elif len(text_to_add) > 9 and len(text_to_add) < 13: 
        draw.text((2050, 1390), text_to_add, font=myFont, fill=(255, 0, 0))
        
    elif len(text_to_add) > 12:
        draw.text((1850, 1390), text_to_add, font=myFont, fill=(255, 0, 0))

    # saving the generated image
    initImage.save(output_image_path)
    
    
    # NOT SENDING ANYTHING TO EMAILS AS OF NOW
    # GOTTA FINALIZE THE EMAIL BODY TEXT
    # sending the generated image to the correct email address
    # send_email(email_subject, email_body, email_address, output_image_path)
        
if __name__ == "__main__":
    DF = pd.read_csv("/Users/daniyarkakimbekov/Workspaces/HoC2023_DataAnalytics/cleaned_data.csv")
    DF = DF[0:30]
    
    email_body = "Құрметті дос, Дорогой участник, благодарим тебя за прохождение Часа Кода!/n Твой сертификат прикреплён к данному письму!"
    email_subject = "Код Сағаты 2023 / Час Кода 2023. Сертификат. "
    
    for i in range(len(DF)):
        # getting data so that we can build paths for certificates
        role = str(DF["role"][i]).replace(" ", "")
        language = str(DF["language"][i]).replace(" ", "")
        
        # some names are written badly, but they should be nice in the certificates
        # some code to take each name and firstly lowercase it, then capitalize name and surname
        name = str(DF["name"][i]).lower().split()
        capitalized_strings = [s.capitalize() for s in name]
        name = ' '.join(capitalized_strings)
    
        # modifying names so that we won't get shitty paths that might interfere with file extensions
        name_for_path_dirty = str(DF["name"][i])
        patterns_to_remove = ['https://www.', '/', ',', '&', '^', '%', '$', '#', '.']
        pattern = '|'.join(re.escape(p) for p in patterns_to_remove)
        name_for_path = re.sub(pattern, '', name_for_path_dirty)
        
        # archived for now
        # name_for_path = str(DF["name"][i]).replace(".", " ").replace("/", " ").replace("https://www.", " ").replace(",", " ").replace(" ", "")
        
        # taking the email to send the certificate to it
        participant_email = str(DF["email"][i]).replace(" ", "")
        
        # pass english certificates or teacher/volunteer certificates
        if language == "english" or role == "teacher" or role == "volunteer":
            pass
        
        else:
            # building path to get the correct certificate template:
            # creating an empty string and then appending to this empty string words
            # usually, paths look like "./folder/folder/file"
            # here, we have a rigid folder structure. we have only Kazakh and Russian folders
            # we take the language we got from the data, append it to ./, then append a slach, then append the role we got from the data, then append the .jpg
            # final path shoud look something like this: ./kazakh/student.jpg
            certificate_path = "".join(["./",language, "/",role, ".jpg"])
            
            # building the correct output path and final filename:
            # final path should look something like this: ./certificates/daniyarkakimbekov.jpeg
            output_path = "".join(["./certificates/",role, "/", name_for_path, ".jpeg"])
            
            # we pass correct certficate path and the correct output path to the function
            # on top of that, we pass the name that we got from the data
            # generate_certificate(certificate_path, output_path, name, participant_email)
            
            # the actual email sending is not done now for testing purposes
            # we can also implement sending a Kazakh/Russian email based on the registration data.
            # gotta pass the language data in here, then save it as some variable inside generate_certificate, then pass this variable to the send_email
            # generate_certificate(certificate_path, output_path, name, "everypidigit@gmail.com")

    print("FINISHED THE WHOLE PROCESS")