from PIL import Image, ImageDraw, ImageFont
import pandas as pd

def generate_certificate(input_image_path, output_image_path, text_to_add):
    initImage = Image.open(input_image_path)
    draw = ImageDraw.Draw(initImage)

    myFont = ImageFont.truetype('./freemono/FreeMono.ttf', 120)
    
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

    initImage.save(output_image_path)

if __name__ == "__main__":
    DF = pd.read_csv("/Users/daniyarkakimbekov/Workspaces/HoC2023_dataWorks/cleaned_data.csv")
    DF = DF[400:410]
    
    for i in range(400, 410):
        print(i)
        
        # getting data so that we can build paths for certificates
        role = str(DF["role"][i]).replace(" ", "")
        language = str(DF["language"][i]).replace(" ", "")
        
        # some names are written badly, but they should be nice in the certificates
        # some code to take each name and firstly lowercase it, then capitalize name and surname
        name = str(DF["name"][i]).lower().split()
        capitalized_strings = [s.capitalize() for s in name]
        name = ' '.join(capitalized_strings)
    
        # modifying names so that we won't get shitty paths that might interfere with file extensions
        name_for_path = str(DF["name"][i]).replace(".", " ").replace("/", " ").replace("https://www.", " ").replace(",", " ").replace(" ", "")
        
        
        email = str(DF["email"][i]).replace(" ", "")
        
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
            # creating an empty string and then appending to this empty string words
            # usually, paths look like "./folder/folder/file"
            # so we take the role and name from the data, append it to ./certificates, and then append .jpg at the end 
            # final path should look something like this: ./certificates/daniyar.kakimbekov.jpg
            output_path = "".join(["./certificates/",role, "/", name_for_path, ".jpg"])
            
            # we pass correct certficate path and the correct output path to the function
            # on top of that, we pass the name that we got from the data
            generate_certificate(certificate_path, output_path, name)

    print("FINISHED GENERATING CERTIFICATES")