import pytesseract
from pytesseract import Output
import PIL.Image
import cv2

green_color = (0, 255, 0)
font_size = 0.5

# Configure the AI, psm (0-13), oem(0-3), l for language
# for language must download from pytesseract GitHub
myconfig = r"--psm 11 --oem 3 -l por"

# Extract the text of all photos and print it
for n in range(1, 10):
    text = (pytesseract.image_to_string(PIL.Image.open(f"photo0{n}.jpg"), config=myconfig)).lower()
    print(f"*****PHOTO{n}\n\n{text}\n\n")

img = cv2.imread("photo07.jpg")
height, width, _ = img.shape

# Transform output data into a dictionary, some keys are important (text, conf, left, top, width and height)
data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)
print(data.keys())
print(data['text'])

# Draw rectangles bases on the confidence passed, as higher the conf, lesser the boxes
amount_boxes = len(data['text'])
for i in range(amount_boxes):
    # Filter data by confidence by 90%
    if float(data['conf'][i]) > 90:
        # Get the top left corner of the box and the size of it
        (x, y, width, height) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        # Draw the rectangle, on the img, starting at (x,y), with size (x+width, y+height)
        img = cv2.rectangle(img, (x, y), (x + width, y + height), green_color)
        # Write the text that the AI is reading, just below the img
        img = cv2.putText(img, data['text'][i], (x, y + height + 15), cv2.FONT_HERSHEY_SIMPLEX, font_size, green_color)

# Show the image and wait keeps the window open
cv2.imshow("img", img)
cv2.waitKey(0)
