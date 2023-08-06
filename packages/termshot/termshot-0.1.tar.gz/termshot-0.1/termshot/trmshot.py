from PIL import Image, ImageDraw
import json, sys

class IncorrectRegion(Exception):
	pass

class ANSIMatrix:
	'''A matrix with ansi color codes used while printing images'''
	def __init__(self, dots):
		self.scale = (len(dots[0]), len(dots))
		self.dots = dots
		self.uds = False
		if self.dots[0][0] == '  ' or self.dots[0][0]:
			self.uds = True
		else:
			if self.dots[0][0].split('m')[1].startswith('  '):
				self.uds = True
	
	def get_img(self):
		'''Function that returns you a string with ansi "pixels"
		:Input:
			self
		:Returns:
			out -> str, image to print'''
		out = []
		for line in self.dots:
			out.append(''.join(line))
		return '\n'.join(out)
	
	def copy(self, region):
		'''Returns ANSIMatrix of region
		:Input:
			self
			region -> tuple(int, int, int, int), region to copy
		:Returns:
			cut -> ANSIMatrix'''
		
		cut = []
		line = []
		
		for y in range(region[1], region[3]):
			for x in range(region[0], region[2]):
				line.append(self.dots[y][x])
			cut.append(line)
			line = []
	
		return ANSIMatrix(cut)
	
	def paste(self, region, position):
		'''Pastes region to position on self
		:Input:
			region -> ANSIMatrix, region to paste
			position -> tuple(int, int), position to paste'''
		
		px = position[0]
		py = position[1]
		
		for y in range(region.scale[1]):
			for x in range(region.scale[0]):
				rg = region.dots[y][x]
				if rg == ' ' or rg == '  ':
					continue
				self.dots[py + y][px + x] = rg
	
	def point(pos, color):
		if isinstance(color, (tuple, list)):
			color = rgb2ansi(color)
		space = ' '
		if self.uds:
			space = '  '
		self.dots[y][x] = f'\u001b[48;5;{color}m{space}\u001b[48;5;0m'
	
	def add_text(self, position, boxlength, text):
		i = 0
		y = position[1]
		while i != len(text):
			for x in range(boxlength):
				try:
					_ = text[i] 
				except:
					break
				if self.uds:
					self.dots[y][x] = self.dots[y][x].replace('  ', text[i] + ' ')
					i += 1
				else:
					self.dots[y][x] = self.dots[y][x].replace(' ', text[i])
			y += 1
	
	def clear_text(self):
		space = ' '
		if self.uds:
			space = '  '
		for y in range(self.scale[1]):
			for x in range(self.scale[0]):
				px = self.dots[y][x]
				try:
					clor = px.split('m')[0].split(';')[2]
					self.dots[y][x] = f'\u001b[48;5;{clor}m{space}\u001b[48;5;0m'
				except:
					self.dots[y][x] = space

# Colors:
# 0 - full black
# 15 - full white
# 232 - 255 - grays
# total: 26
# rgb divider: 9.8 (255 / 26)

# f'\u001b[48;5;{code}m'

def rgb2ansi(rgb, a=0):
	'''Converts RGB color to nearest ANSI one
	:Input:
		rgb -> tuple(int, int, int), RGB value to convert
	:Returns:
		number -> int, ANSI value'''
	if a:
		return 0
	number = 16 + 36 * round(rgb[0] / 51) + 6 * round(rgb[1] / 51) + round(rgb[2] / 51)
	return number

def gray(img, rescale = (None, None), use_double_spaces=True, allow_15 = True, debug=False, inverse=False):
	'''A grayscale print function. Prints monochrome version of img with size rescale to terminal
	:Input:
		img -> str, image
		rescale -> tuple(int, int), scale. If part is None, original one. = (None, None)
		use_double_spaces -> bool, use 2 spaces instead of 1. = True
		allow_15 -> bool, allow full white (15). = True
	
	:Returns:
		img'''
		
	if use_double_spaces:
		space = '  '
	else:
		space = ' '
	
	pallete = (0, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 255, 15)
	if not allow_15:
		pallete = (0, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 255, 255)
	if inverse:
		pallete = pallete[::-1]
	#	print(pallete)
	out = []
	with Image.open(img) as image:
		_rescale = rescale
	
		if _rescale[0] == None:
			_rescale = (image.size[0], _rescale[1])
		if _rescale[1] == None:
			_rescale = (_rescale[0], image.size[1])
		
		rescale = _rescale
		image = image.resize(rescale)
		px = image.load()
		if debug:
			nm = Image.new('RGB', image.size)
			br = ImageDraw.Draw(nm)
		for y in range(image.size[1]):
			for x in range(image.size[0]):
				color = px[x, y]
				mid = (color[0] + color[1] + color[2]) // 3
				if debug:
					br.point((x, y), (mid, mid, mid))
				code = round(mid / 9.8)
				code = pallete[code]
				out.append(f'\u001b[48;5;{code}m{space}\u001b[48;5;0m')
			out.append('\n')
		if debug:
			nm.save('debug_grayscale_.png')
			nm.close()
			del br
	return ANSIMatrix(out)

def colored(img, use_double_spaces=True, rescale=(None, None)):
	'''A colored image printer.
	:Input:
		img -> str, image
		use_double_spaces -> bool, use double spaces. = True
		rescale -> tuple(int/None, int/None), if None will use original size. = (None, None)
	:Returns:
		out -> ANSIMatrix'''
	if use_double_spaces:
		space ='  '
	else:
		space = ' '
		
	out = []
	line = []
	
	with Image.open(img) as pic:
		_rescale = rescale
		if _rescale[0] == None:
			_rescale = (image.size[0], _rescale[1])
		if _rescale[1] == None:
			_rescale = (_rescale[0], image.size[1])
		
		rescale = _rescale
		
		pic = pic.resize(rescale)
		
		px = pic.load()
		
		for y in range(pic.size[1]):
			for x in range(pic.size[0]):
				color = px[x, y]
				if len(color) == 3:
					line.append(f'\u001b[48;5;{rgb2ansi(color)}m{space}\u001b[48;5;0m')
				else:
					a = color[3] == 0
					if rgb2ansi(color, a) == 0:
						line.append(space)
					else:
						line.append(f'\u001b[48;5;{rgb2ansi(color)}m{space}\u001b[48;5;0m')
			out.append(line)
			line = []
		
	return ANSIMatrix(out)

def dump(matrix, output):
	'''Used to dump ANSIMatrix object into output file
	:Input:
		matrix -> ANSIMatrix, matrix to dump
		output -> str, output filename
	:Returns:
		None'''
	colors = []
	linec = []
	for line in matrix.dots:
		for sym in line:
			linec.append(sym.split('m')[0].split(';')[2])
		colors.append(linec)
		linec = []
	d = {}
	d['vals'] = colors
	
	with open(output, 'w') as file:
		json.dump(d, file)

def load(file):
	with open(file, 'r') as arc:
		jon = json.load(arc)
	out = []
	line = []
	for ln in jon['vals']:
		for val in ln:
			line.append(f'\u001b[48;5;{val}m  \u001b[48;5;0m')
		out.append(line)
		line = []
	return ANSIMatrix(out)

if __name__ == '__main__':
	print(colored(sys.argv[1], use_double_spaces=True, rescale=(int(sys.argv[2]), int(sys.argv[3]))).get_img())