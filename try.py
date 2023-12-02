from PIL import Image, ImageDraw, ImageFont

def generate_certificate(input_image_path, output_image_path, text_to_add):
    # Open the image
    image = Image.open(input_image_path)

    # Get a drawing context on the image
    draw = ImageDraw.Draw(image)

    # Choose a font and size
    myFont = ImageFont.truetype('./freemono/FreeMono.ttf', 65)
    draw.text((1700, 1480), text_to_add, font=myFont, fill=(255, 0, 0))

    image.save(output_image_path)

if __name__ == "__main__":
    input_image_path = "./certificatesRu/volunteerRu.jpg"  # Replace with your input image path
    output_image_path = "output_certificate.jpg"  # Replace with your desired output image path
    text_to_add = "APCHIIIASJDOIASHDOIAHS AOSIHDASIODH"  # Replace with the desired text
    font_size = 36

    generate_certificate(input_image_path, output_image_path, text_to_add)
