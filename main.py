from __future__ import print_function
from wand.image import Image
import sys, os.path

'''
PDF to GIF converter for Gadfly Legal Technologies
by Joe Romano

First, load the venv (source /venv/bin/activate)
Usage: python main.py [path to pdf to convert] [name for AWS remote subdirectory] [output location]
AWS Path for us: https://s3.amazonaws.com/lease-pilot-production/casto/signage_criteria
'''

################################################################################

def main(argv):
    converting_file = argv[0]
    remote_path = argv[1]

    print("Currently converting file: ", converting_file)

    # generate a subdirectory for the gifs to live in
    subdirectory = converting_file[:-4]
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass

    with Image(filename = converting_file, resolution=200) as pdf:

        # generate the template file
        generate_haml(subdirectory, remote_path, len(pdf.sequence))

        # give info on what we're doing
        print("Saving " + str(len(pdf.sequence)) + " pages, [width=" +
            str(pdf.width) + ", height=" + str(pdf.height) + "]")

        # loop through each page in the PDF
        for page in pdf.sequence:
            print("Currently on page:", page.index + 1)
            # initialize an image of the right size
            converted = Image(width = page.width, height=page.height)
            # copy in the page of the PDF to this image
            converted.composite(page, top=0, left=0)
            # save the image as a gif
            converted.format = "gif"
            savepath = os.path.join(subdirectory, str(page.index + 1) + ".gif")
            converted.save(filename=savepath)

################################################################################

# generate the HAML file that loads all images
def generate_haml(building_template_url, remote_path, pages):

    # set up the directory
    haml_templates = "haml_templates"
    try:
        os.mkdir(haml_templates)
    except Exception:
        pass

    # open files and fill them in
    with open(os.path.join(haml_templates, building_template_url + ".html.haml"), "w") as outf:
        for i in range(pages):
            outf.write("%img.embedded-page{ 'src': \"" + remote_path + "/" +
                building_template_url + "/" + str(i) + ".gif\" }\n")
            outf.write("<br style=\"page-break-before:always\"/>\n")
        outf.write("\n%p{ 'ng-show': 'false' } !!FULL_IMAGE_STYLE_SECTION!!")

################################################################################

if __name__ == "__main__":
    main(sys.argv[1:])
