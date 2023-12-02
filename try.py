from PIL import Image, ImageDraw, ImageFont

def generate_certificate(input_image_path, output_image_path, text_to_add):
    # Open the image
    image = Image.open(input_image_path)

    # Get a drawing context on the image
    draw = ImageDraw.Draw(image)

    # Choose a font and size
    font = ImageFont.load_default()  # Use the default PIL font
    font = font.font_variant(size=font_size)  # Set the font size

    # Choose text color
    text_color = (255, 255, 255)  # RGB color tuple (white in this case)

    # Choose text position
    text_position = (1700, 1480)  # (x, y) coordinates

    # Add text to the image
    draw.text(text_position, text_to_add, font=font, fill=text_color)

    # Save the modified image
    image.save(output_image_path)

if __name__ == "__main__":
    input_image_path = "./certificatesRu/volunteerRu.jpg"  # Replace with your input image path
    output_image_path = "output_certificate.jpg"  # Replace with your desired output image path
    text_to_add = "John Doe"  # Replace with the desired text
    font_size = 36

    generate_certificate(input_image_path, output_image_path, text_to_add)
