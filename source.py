# Importing the Reqired Libraries
import requests
from pyunsplash import PyUnsplash
from bs4 import BeautifulSoup
import jinja2
import os
import subprocess
from PIL import Image


def ImtoPdf(CountOfImages: int, Category: str):
    current_working_dir = os.getcwd()
    # Key to access the Unsplash Api
    UNSPLASH_ACCESS_KEY = "t9W5e9-m4bq_8BGJw4BnvOMfa3NAMVqLygq2wkWj58g"
    # Using Unsplash API with python
    unsplash = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)
    photos = unsplash.photos(
        type_='random', count=CountOfImages, featured=True, query=Category)
    try:
        os.makedirs(current_working_dir + "/"+Category)
    except:
        pass
    Count = 1
    doc = ""
    for photo in photos.entries:
        print(photo.id, "/n", photo.link_download)
        print("Image Response recieved")
        im_link = "https://unsplash.com/photos/" + photo.id
        print("im_link generated")
        response1 = requests.get(im_link, allow_redirects=True)
        print("Im_link response recieved")
        print(im_link)
        soup = BeautifulSoup(response1.text, 'lxml')
        Binding_Values = soup('span', {'class': 'e6qY8'})
        image_value = []
        print(image_value)
        for tags in Binding_Values:
            image_value.append(tags.text)
        print(image_value)
        if len(image_value) > 3:
            image_value = image_value[1:3]
        else:
            image_value = image_value[0:2]
        file = Image.open(requests.get(
            photo.link_download, stream=True).raw)
        file.save(current_working_dir + "\\" +
                    Category + "\\Image"+str(Count)+".JPG")

        image_dir = current_working_dir + "/"+Category
        latex_jinja_env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath('.'))
        )
        variable1 = image_value[0]
        variable2 = image_value[1]
        template = latex_jinja_env.get_template('jinja-test.tex')
        image_dir = image_dir.replace("\\", "/")
        doc1 = template.render(base_dir=image_dir, im1="Image" +
                            str(Count)+".JPG", var1=variable1, var2=variable2)
        
        if Count == 1:
            doc = doc + doc1
        else:
            doc1 = doc1.replace("\documentclass[a4paper,landscape]{article}","")
            doc1 = doc1.replace(r"\usepackage","")
            doc1 = doc1.replace(r"\usepackage[margin=1cm]{geometry}", "")
            doc1 = doc1.replace(r"\pagestyle{empty}", "")
            doc1 = doc1.replace("{graphicx}", "")
            doc1 = doc1.replace(r"\graphicspath","")
            doc1 = doc1.replace(r"\usepackage","")
            doc1 = doc1.replace("{parskip}", "")
            doc1 = doc1.replace("[margin=1cm]{geometry}", "")
            doc1 = doc1.replace(r"\begin{document}", "")
            a1 = "{ {"+image_dir+"} }"
            doc1 = doc1.replace(a1, "")
            # doc1 = doc1.replace("\graphicspath{ {\VAR{{base_dir}} }"
            doc = doc + "\n"+doc1.strip()
        if Count % 2 != 0:
            doc = doc + "\n%"
        else:
            doc = doc + "\n"
        Count += 1
    doc = doc+ "\n"+r"\end{document}"
        # section1='Long Form', section2='Short Form'
    file = open("sample.tex", "w")
    file.write(doc)
    file.close()
    subprocess.call(
        current_working_dir+r"\Config\pdflatex "+"sample.tex"
    )


def getInput():
    CountOfImages = int(input("Enter Image Count to be fetched\n"))
    ImageCategory = str(input("Enter the image Category\n"))
    ImtoPdf(CountOfImages, ImageCategory)


getInput()