from __future__ import print_function, division
from wand.image import Image
import sys, os.path

'''
PDF to GIF converter for Gadfly Legal Technologies
by Joe Romano

AWS Path for us: https://s3.amazonaws.com/lease-pilot-production/casto/signage_criteria
'''

################################################################################

def main(argv):

    # informative, but simplistic, error message
    if not len(argv) == 3:
        print("ERROR: You must provide three arguments.")
        print("Usage: python main.py [path to pdf to convert] [name for AWS remote subdirectory] [output location]")
        sys.exit(1)

    # set up all our arguments
    converting_file = argv[0]
    remote_path = argv[1]
    output_location = argv[2]
    root, bldg_name = os.path.split(converting_file[:-4])
    print("\033[92m" + "[INFO] Currently converting file: ", converting_file)

    # generate a subdirectory for the gifs to live in
    subdirectory = os.path.join(output_location, bldg_name)
    makeDir(output_location)
    makeDir(subdirectory)

    with Image(filename = converting_file, resolution=200) as pdf:

        # determine the correct page type
        if abs((pdf.width / pdf.height) - 0.7727272727) < 0.02:
            page_type = "LETTER"
        elif abs((pdf.width / pdf.height) - 0.6071428571) < 0.02:
            page_type = "LEGAL"
        else:
            page_type = "UNKNOWN"

        # generate the template file
        generate_haml(bldg_name, remote_path, len(pdf.sequence), output_location, page_type)

        # give info on what we're doing
        print("\033[92m" + "[INFO] Saving " + str(len(pdf.sequence)) + " pages, [width=" +
            str(pdf.width) + ", height=" + str(pdf.height) + "], type: " + page_type)

        # loop through each page in the PDF
        for page in pdf.sequence:
            print("\033[92m" + "[INFO] Currently on page:", page.index + 1)
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
def generate_haml(building_template_url, remote_path, pages, output_location, page_type):

    # set up the directory
    haml_templates = os.path.join(output_location, "haml_templates/")
    makeDir(haml_templates)

    # open files and fill them in
    with open(os.path.join(haml_templates, building_template_url + ".html.haml"), "w") as outf:
        for i in range(pages):
            outf.write("%img.embedded-page{ 'src': \"" + remote_path + "/" +
                building_template_url + "/" + str(i + 1) + ".gif\" }\n")
            outf.write("<br style=\"page-break-before:always\"/>\n")
        outf.write("\n%p{ 'ng-show': 'false' } !!FULL_IMAGE_STYLE_SECTION_" + page_type + "!!")

################################################################################

# simple function to make a directory if it doesn't exist
def makeDir(directory):
    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
            print("\033[92m" + "[INFO] Made directory: " + directory)
        except Exception:
            print("\033[91m" + "[ERROR] Couldn't make directory: " + directory)
            sys.exit(3)
    else:
        print("\033[93m" + "[WARN] Directory already exists: " + directory)

################################################################################

if __name__ == "__main__":
    main(sys.argv[1:])
    print("\033[95m" + "CONVERSION COMPLETE")
