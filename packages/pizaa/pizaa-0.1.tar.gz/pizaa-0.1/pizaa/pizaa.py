from PIL import Image, ImageDraw
import os, shutil

class ITAA:
	def itaa(image, output=None,mode='save', rescale = (32, 32), inverse = False, enlarge = False):
		path = ''.join(image.split('.')[:-1])
		if output == None:
			output = f'{path}_ascii.txt'
		
		pallete = [ '.', '\'', '"', '-', '=', '+', '!', '?', '$', '%', '&', 'b', 'Y', 'Q', 'E', 'R', 'B', 'U', 'P', 'O', 'G',  'M', '#', 'W', '@', '@' ]
		
		if inverse:
			pallete = pallete[::-1]
		
		out = []
		
		with Image.open(image) as img:
			img = img.resize(rescale)
			w = img.size[0]
			h = img.size[1]
			pix = img.load()
			for y in range(h):
				for x in range(w):
					col = pix[x, y]
					mid = (col[0] + col[1] + col[2]) // 3
					color = round(mid // 10)
					# print(f'{color}|{mid}|{col}')
					sym = pallete[color]
					if enlarge:
						sym = sym * 2
					out.append(sym)
				out.append('\n')
		if mode == 'save':
			with open(output, 'w') as file:
				file.write(''.join(out))
				return
		return ''.join(out)
	
	def restore_grayscale(text, output = 'grayscale.png'):
		pallete = [ '.', '\'', '"', '-', '=', '+', '!', '?', '$', '%', '&', 'b', 'Y', 'Q', 'E', 'R', 'B', 'U', 'P', 'O', 'G',  'M', '#', 'W', '@', '@' ]
		data = []
		for sym in text:
			if sym != '\n':
				color = pallete.index(sym) * 10
				data.append((color, color, color))
		sx = len(text.splitlines()[0])
		sy = len(text.splitlines())
		with Image.new('RGB', (sx, sy)) as img:
			img.putdata(data)
			img.save(output)
		

if __name__ == '__main__':
	while 1:
		print(ITAA.itaa(input('img >>> '), rescale = (int(input()), int(input())), mode='', enlarge = int(input('Enlarge? >>> '))))