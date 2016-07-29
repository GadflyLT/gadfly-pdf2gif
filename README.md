# gadfly-pdf2gif
Python script to convert multipage PDF into multi-GIF files.  Provided a PDF file, it will output one GIF file per page, and a HAML file with the images included and the proper tag for the .NET converter service.

# Setup
This script uses Python 2.7 and Wand (based on ImageMagick).

    brew install python
    pip install Wand

# How to use
## Single file

    python main.py <path to pdf to convert> <name for AWS remote subdirectory> <output location>
    
Example:

    python main.py stone_creek_village.pdf https://s3.amazonaws.com/lease-pilot-production/casto/signage_criteria ~/Desktop/output/

##Multi-file
The following bash script is recommended.

    for file in <directory>/*
      do python main.py "$file" <AWS remote> <output folder>
    done
