Description: This script extracts Aadhaar and extracts Pan information from the image uploaded by consumer. The result is returned
as a json object.

Installation
This library requires Python 3.6+ to run. As well as you also need to install tesseract on your system. If you have Linux based system just run:

use this line for Linux
sudo apt install tesseract-ocr

for windows use 

download tesseract software

'https://github.com/UB-Mannheim/tesseract/wiki'

Then
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

For Mac OS

install brew

 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

#install brew in tesseract

 brew install tesseract

#list tesseract

 brew list tesseract

this is list-->

/usr/local/Cellar/tesseract/4.1.1/bin/tesseract 

/usr/local/Cellar/tesseract/4.1.1/bin/tesseract this line use for code
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

Install the package.

pip install aadhar-pan-extractor
Then Import the package.

from aadhar_pan_extractor import Pan_Info_Extractor,Aadhar_Info_Extractor
Create an instance of the extractor.

this line use only for aadhar information
extractor = Aadhar_Info_Extractor()

this line use only for pan information
extractor = Pan_Info_Extractor()
Pass the image to the extractor to get the results.

extractor.info_extractor('/content/pan test.jpeg')
This will return a result as following:

{
    "Aadhar_number": "4382 5165 5729",
    "Address": "NAN",
    "DOB": "01/01/2003",
    "Gender": "Male",
} 
