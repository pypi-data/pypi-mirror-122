# genBarcode

genBarcode is a cli tool I created to simply take a string and generate barcode.

I use an application on my phone to track numerous packages. When I get the tracking on my phone it's relatively easy to just add the tracking directly. But when it's on my computer I tend to copy the tracking number and paste it into one of the many online barcode generator sites. Sometimes these sites don't make the barcode big enough, or they use some different barcode that my phone has trouble reading.

I figureed I'd just create a python tool to generate the barcode for me. This makes it so I don't have to rely on sites, or dealing with the hassle. The code uses python-barcode and supports the full gambit of formats offered by that library.

Additionally this just a fun project to improve my skills such as 
* learning more about packaging python tools
* building wheels
* uploading to pypi
* building a reliable development environment
* using poetry
* using pipx

# Installation
I highly recommend you use `pipx` to install this, as it creates the virtualenv for you and seamlessly handles the loading of the virtual environment when running this tool. If you choose not to use `pipx`, you should create a virtualenv and possibly a wrapper script to launch this in the virtualenv.

```sh
pipx install genBarcode
```

# Usage

The following is the help for the program
```
usage: genbarcode [-h] [-V] [-v] [-l] [-m METHOD] [-d DATA] [-t TRACKING]

 program description to be displayed by argparse
    ex: python genBarcode.py


optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -v, --verbose
  -l, --list-methods    Enumerate available generators and exit
  -m METHOD, --method METHOD
                        set the barcode generated type (default: code128)
  -d DATA, --data DATA  Provide data to be used to generate the barcode
  -t TRACKING, --tracking TRACKING
                        Provide tracking number to be used to generate the barcode, stub for --data
```

One of `-d` or `-t` is required. You can use either one.

# Examples

```sh
# print help/usage
genBarcode -h

# print all available barcode formats
genBarcode -l

# print all available barcode formats
genBarcode -l

# USPS sample
genBarcode -d 9400123456789999876500

# UPS sample
genBarcode --data 1Z9999999999999999

# Fedex sample
genBarcode --tracking 123456789012

# Generate isbn for 1984/George.Orwell
genBarcode -m isbn -d 9780451524935
genBarcode -m isbn13 -d 9780451524935
genBarcode -m isbn10 -d 0451524934
```

# Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tbennett6421/pythoncookie](https://github.com/tbennett6421/pythoncookie) project template.
