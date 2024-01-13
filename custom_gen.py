from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import re

def generate_certificate(input_image_path, output_image_path, name):
    try:
        initCertificateImage = Image.open(input_image_path)
        drawCertificate = ImageDraw.Draw(initCertificateImage)
        
    except Exception as e:
        print(e)
        pass
    
    certificateFont = ImageFont.truetype('./font/FreeMono.ttf', 80)
    longCertificateFont = ImageFont.truetype('./font/FreeMono.ttf', 25)
    intermediateCertificateFont = ImageFont.truetype('./font/FreeMono.ttf', 70)
    
    if len(name) < 7:
        drawCertificate.text((2200, 1420), name, font=certificateFont, fill=(255, 0, 0))
        
    elif len(name) > 6 and len(name) < 10:
        drawCertificate.text((2150, 1420), name, font=certificateFont, fill=(255, 0, 0))
        
    elif len(name) > 9 and len(name) < 13: 
        drawCertificate.text((2050, 1420), name, font=certificateFont, fill=(255, 0, 0))
        
    elif len(name) > 12 and len(name) < 20:
        drawCertificate.text((1870, 1420), name, font=certificateFont, fill=(255, 0, 0))
        
    elif len(name) >= 20 and len(name) < 26:
        drawCertificate.text((1800, 1420), name, font=certificateFont, fill=(255, 0, 0))
        
    elif len(name) >= 26 and len(name) < 33:
        drawCertificate.text((1740, 1420), name, font=certificateFont, fill=(255, 0, 0))
        
    elif len(name) >= 33 and len(name) < 40:
        drawCertificate.text((1660, 1420), name, font=intermediateCertificateFont, fill=(255, 0, 0))
        
    elif len(name) >= 40:
        drawCertificate.text((1590, 1465), name, font=longCertificateFont, fill=(255, 0, 0))

    original_width, original_height = initCertificateImage.size
    new_width = int(original_width * 0.3)
    new_height = int(original_height * 0.3)    
    initCertificateImage = initCertificateImage.resize((new_width, new_height))
    
    try:
        initCertificateImage.save(output_image_path)
    except Exception:
        print("huh2")
        pass
        
if __name__ == "__main__":
    DF = pd.read_csv("/Users/daniyarkakimbekov/Workspaces/HoC2023_CertificateGenerator/specialData/Margulan9jan.csv")
    
    for i in range(0,len(DF)):
            
            cert_name = str(DF["name"][i]).lower().split()
            capitalized_strings = [s.capitalize() for s in cert_name]
            cert_name = ' '.join(capitalized_strings)
        
            name_for_path_dirty = str(DF["name"][i])
            patterns_to_remove = ['https://www.', '/', ',', '&', '^', '%', '$', '#', '.']
            pattern = '|'.join(re.escape(p) for p in patterns_to_remove)
            name_for_path = re.sub(pattern, '', name_for_path_dirty)
            
            certificate_path = "./templates/kazakh/volunteer.jpg"
            
            output_path = "".join(["./certificates/volunteer/", name_for_path, ".jpeg"])
            
            print(f"starting process for user number {i} name {cert_name}")
            generate_certificate(certificate_path, output_path, cert_name)

