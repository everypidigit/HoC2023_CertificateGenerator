from PIL import Image, ImageFont, ImageDraw
import pandas as pd


# df = pd.read_excel("lists/Nauryz_contest_4th_grade.xlsx", "Статистика")

# #list of names should be in 'names' column
# imya = df['Укажите имя на английском языке.'].values.tolist()
# familiya = df['Укажите фамилию на английском языке.'].values.tolist()
# names = [" "]
# #list of ids should be in 'id' column
# ids = df['№'].values.tolist()
# #list of procents should be in 'percent' column
# procents =  df['Процент правильных ответов (%)'].values.tolist()
        
image = Image.open("./certificatesKaz/student.jpg")

draw = ImageDraw.Draw(image)
W, H = (1240,200)
# w, h = draw.textsize(17)

draw.text(xy = (1120-(1.35*W),930), text = "Arman Karmanov", fill = "black")
#choosing font 

draw.text(xy = (1700,1480), text = 'ASPODJAPOSIJDPAOSJDASOJDOPASJDOPSJDJOP', fill = "black")

#saving image in the right location
image.save("certificate.jpg")