from PIL import Image
import os
import re
import pytesseract

# Tesseractの実行ファイルのパスを設定（必要に応じて変更）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# 現在のフォルダのパスを取得
current_folder = os.getcwd()

# .jpg ファイルをリストアップ
jpg_files = [f for f in os.listdir(current_folder) if f.lower().endswith('.jpg')]
# 正規表現パターン
pattern = r"Screenshot_\d{4}(\d{2})(\d{2})_(\d{2})(\d{2})\d{2}\.jpg"
formatted_time=""
collecttxt =""

for jpg_file in jpg_files:
	image_path = jpg_file
	image = Image.open(image_path)
	match = re.search(pattern, image_path)
	if match:
		month = match.group(1)
		day = match.group(2)
		hour = match.group(3)
		minute = match.group(4)
		formatted_time = f"{month}-{day} {hour}--{minute}"
	else:
		print("No match found")
	crop_box = (1400, 760, 1700, 810)
	cropped_image = image.crop(crop_box)
	gray_image = cropped_image.convert("L")
	# OCRを実行
	text = pytesseract.image_to_string(gray_image, lang='eng')
	print(text)
	output_path = formatted_time+".jpg"
	gray_image.save("tmp/"+output_path)
	collecttxt = collecttxt +formatted_time +"\t" +  text 


collecttxt=re.sub('pt', '', collecttxt)
collecttxt=re.sub('--', ':', collecttxt)
collecttxt=re.sub('^$', '', collecttxt)
f = open("all.txt", 'w')
f.write(collecttxt)
f.close()
