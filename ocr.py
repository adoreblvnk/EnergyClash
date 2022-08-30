from PIL import Image
import pytesseract
import config
import cv2

# blvnk
if config.ENV == "dev":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img_path = r"demo\eversource_bill.png"
# img_path = r"demo\pacific_light_bill.png"

img = cv2.imread(img_path)
img = cv2.cvtColor(img, 0, 255)
text = pytesseract.image_to_string(img, config="--psm 11")
text_slice = " ".join([text]).split()
print(text_slice)

img = Image.open(img_path)

text = pytesseract.image_to_string(img)
text_slice = " ".join([text]).split()
print(text_slice)
