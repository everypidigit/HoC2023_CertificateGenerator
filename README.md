# HoC2023_CertificateGenerator

A scripy to generate and send participant certificates for Hour of Code 2023.

Simple instruction below, but better contact me @everypidigit lol.

### How to use:

1. Open generate_certificates.py
2. Insert correct path to the .csv file in the 55th line of code:

   - DF = pd.read_csv("path_to_your_file")
3. If necessary, change the email settings in the send_email function:

   - sender_email ="everypidigit@gmail.com"
   - sender_password ="lili qgkh zlnr apsy"
   - smtp_server ='smtp.gmail.com'
4. Run python generate_certificates.py
5. Enjoy!
