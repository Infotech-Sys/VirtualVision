from pytesseract import Output
from PIL import ImageFont, ImageDraw, Image  
import pytesseract
import argparse
import cv2

min_conf=1
path='/home/sri/VirtualVision/data/sample/eye.jpg'
img = Image.open(path)  
draw = ImageDraw.Draw(img)  
font = ImageFont.truetype("braille.ttf", 15)  
# load the input image, convert it from BGR to RGB channel ordering,
# and use Tesseract to localize each area of text in the input image
image = cv2.imread(path)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
# loop over each of the individual text localizations
for i in range(0, len(results["text"])):
	# extract the bounding box coordinates of the text region from
	# the current result
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]
	

	conf = int(results["conf"][i])
	
	if conf > min_conf:
		if w > 10 and w <200:
			cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,255), -1)
cv2.imwrite('output.png',image)
img = Image.open('output.png')  
draw = ImageDraw.Draw(img)  
font = ImageFont.truetype("braille.ttf", 15)  
for i in range(0, len(results["text"])):
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]
	text = results["text"][i]
	conf = int(results["conf"][i])
	if conf > min_conf:
		print("Confidence: {}".format(conf))
		print("Text: {}".format(text))
		print("")
		text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
		if w > 10 and w <200 and len(text) > 2:
			draw.text((x,y), "world", font=font,fill='#000000')
img.save("output.png")
cv2.imshow("Image", image)
cv2.imshow('img',cv2.imread('output.png'))
while True:
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()
