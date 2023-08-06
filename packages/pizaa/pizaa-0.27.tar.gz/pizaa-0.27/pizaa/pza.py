from PIL import Image, ImageDraw
import os, shutil

class ITAA:
	def _itaa(image, output=None,mode='save', rescale = (32, 32), inverse = False, enlarge = False):
		'''An older version of itaa function, with old 25 color pallete
		:Input:
			image -> str, image
			output -> str, output file name. If None, f'{image}_ascii.txt'
			mode -> str, if not 'save', will return output = 'save'
			rescale -> tuple[int, int], final image size = (32, 32)
			inverse -> bool, reverse colors = False
			enlarge -> bool, double symbols = False
			
		:Returns:
			if mode != 'save':
				img
			else:
				None
		
		:Usage:
			>>> ITAA._itaa("test.png", enlarge = True, mode = "", rescale = (25, 25))
@@@@@@@@@@@@@@@@UU$$--......--$$UU@@@@@@@@@@@@@@@@
@@@@@@@@@@@@WW??..................??WW@@@@@@@@@@@@
@@@@@@@@@@@@&&..OOMM""..............&&@@@@@@@@@@@@
@@@@@@@@@@@@!!''WW@@==..............!!@@@@@@@@@@@@
@@@@@@@@@@@@!!..----................!!@@@@@@@@@@@@
@@@@@@@@@@@@EE&&%%%%&&&&++..........!!@@@@@@@@@@@@
@@WW&&!!!!!!????????????--..........??EE!!!!&&WW@@
@@??................................$$%%......??@@
UU..................................%%$$........UU
$$..................................YY++........$$
""................................''RR''........""
............................""++RR$$............
..............!!QQEEEEEEEEEEEEEEYY++..............
............$$EE==''..............................
""........''RR..................................""
$$........++YY..................................$$
UU........$$%%..................................UU
@@??......%%$$................................??@@
@@WW&&!!!!EE??..........--????????????!!!!!!&&WW@@
@@@@@@@@@@@@!!..........++&&&&%%%%&&EE@@@@@@@@@@@@
@@@@@@@@@@@@!!................----..!!@@@@@@@@@@@@
@@@@@@@@@@@@!!..............==@@WW''!!@@@@@@@@@@@@
@@@@@@@@@@@@&&..............""MMOO..&&@@@@@@@@@@@@
@@@@@@@@@@@@WW??..................??WW@@@@@@@@@@@@
@@@@@@@@@@@@@@@@UU$$--......--$$UU@@@@@@@@@@@@@@@@
			 '''
		path = ''.join(image.split('.')[:-1])
		if output == None:
			output = f'{path}_ascii.txt'
		
		pallete = ( '.', '\'', '"', '-', '=', '+', '!', '?', '$', '%', '&', 'b', 'Y', 'Q', 'E', 'R', 'B', 'U', 'P', 'O', 'G',  'M', '#', 'W', '@', '@' )
		
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
		
	def itaa(image, output=None,mode='save', rescale = (32, 32), inverse = False, enlarge = False, use_spaces = False):
		'''Itaa function, with 51 color pallete
		:Input:
			image -> str, image
			output -> str, output file name. If None, f'{image}_ascii.txt'
			mode -> str, if not 'save', will return output = 'save'
			rescale -> tuple[int, int], final image size = (32, 32)
			inverse -> bool, reverse colors = False
			enlarge -> bool, double symbols = False
			use_spaces -> bool, use spaces instead of dots = False
			
		:Returns:
			if mode != 'save':
				img
			else:
				None
		
		:Usage:
			>>> ITAA.itaa("test.png", enlarge = True, mode = "", rescale = (25, 25))
			WWWWWWWWWWWWWWWWAAaa;;,,  ,,;;ssPPWWWWWWWWWWWWWWWW
WWWWWWWWWWWWKKcc,,,,              ccKKWWWWWWWWWWWW
WWWWWWWWWWWWoo  YYQQ::              ooWWWWWWWWWWWW
WWWWWWWWWWWW~~::KKWW--              ~~WWWWWWWWWWWW
WWWWWWWWWWWW~~  ;;--                ==WWWWWWWWWWWW
WWWWWWWWWWWWwwoouuuuoooo--          ==WWWWWWWWWWWW
WWKKkk========cccccccccc--          ==ww====kkKKWW
WWcc                                aayy      ccWW
PP                                  uuaa        PP
aa                                  bb--        aa
::                                ::$$::        ::
                    ,,,,,,,,::::--??aa
              ==mm++++++++++++++LL**
            ssww--::,,,,,,,,
::        ::$$,,                                ::
aa        --bb                                  aa
PP        aayy                                  PP
WWcc      yyaa                                ccWW
WWKKkk====ww==          --cccccccccc========kkKKWW
WWWWWWWWWWWW==          --oooouuuuoowwWWWWWWWWWWWW
WWWWWWWWWWWW==                --;;  ~~WWWWWWWWWWWW
WWWWWWWWWWWW~~              --WWKK::~~WWWWWWWWWWWW
WWWWWWWWWWWWoo              ::QQOO  ooWWWWWWWWWWWW
WWWWWWWWWWWWKKcc              ,,,,ccKKWWWWWWWWWWWW
WWWWWWWWWWWWWWWWPPss;;,,  ,,;;aaAAWWWWWWWWWWWWWWWW'''
		path = ''.join(image.split('.')[:-1])
		if output == None:
			output = f'{path}_ascii.txt'
		
		pallete = '.,::::;----*~==casyuokpdbLnmw+?$%VAP&COYSUQDGNKM#@WW'
		#print(len(pallete))
		
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
					color = round(mid // 5)
					# print(f'{color}|{mid}|{col}')
					sym = pallete[color]
					if use_spaces and sym == '.':
						sym = ' '
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
		'''A function, that restores grayscale from text:
			:Input:
				text -> str, text
				output -> str, output file = "grayscale.png"
			:Returns:
				None'''
		pallete = '.,::::;----*~==casyuokpdbLnmw+?$%VAP&COYSUQDGNKM#@WW'
		data = []
		for sym in text:
			if sym != '\n':
				color = pallete.find(sym) * 10
				data.append((color, color, color))
		sx = len(text.splitlines()[0])
		sy = len(text.splitlines())
		with Image.new('RGB', (sx, sy)) as img:
			img.putdata(data)
			img.save(output)
		

if __name__ == '__main__':
	while 1:
		print(ITAA.itaa(input('img >>> '), rescale = (int(input()), int(input())), mode='', enlarge = int(input('Enlarge? >>> ')), inverse = int(input('Reverse >>> ')), use_spaces=True))