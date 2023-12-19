emails = []

for i in range(1, 51):
    emails.append("hoc2023certificates{i}@hourofcode.kz")
    
smtp_server = "smtp.gmail.com"
sender_email = "daniyar@ustemrobotics.kz"  
password = "Rapture9949!"

count = 0
    
for addr in range(0, 50):
    with smtplib.SMTP_SSL(smtp_server, 465) as server:
            server.login(emails[addr], password)
            for i in range(0,500):
                role = str(DF["role"][count+i+limit]).replace(" ", "")
                language = str(DF["language"][i]).replace(" ", "")
                
                if language == "english" or role == "teacher" or role == "volunteer":
                    pass
                
                name = str(DF["name"][i]).lower().split()
                capitalized_strings = [s.capitalize() for s in name]
                name = ' '.join(capitalized_strings)
            
                name_for_path_dirty = str(DF["name"][i])
                patterns_to_remove = ['https://www.', '/', ',', '&', '^', '%', '$', '#', '.']
                pattern = '|'.join(re.escape(p) for p in patterns_to_remove)
                name_for_path = re.sub(pattern, '', name_for_path_dirty)
                
                participant_email = str(DF["email"][i]).replace(" ", "")
                
                certificate_path = "".join(["./", language, "/", role, ".jpg"])
                voucher_path = "".join(["./", language, "/voucher.jpg"])
                
                output_path = "".join(["./certificates/",role, "/", name_for_path, ".jpeg"])
                out_voucher_path = "".join(["./certificates/",role, "/", name_for_path, "_Voucher.jpeg"])
                
                print(f"starting process for user number {i}")
                generate_certificate(certificate_path, voucher_path, output_path, out_voucher_path, name, participant_email)
            count = count + 500
server.quit()