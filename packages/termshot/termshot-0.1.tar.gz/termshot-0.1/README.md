Termshot is a easy-to-use python image to terminal printer, that allows you to edit already converted images (like copy, paste).

Classes:
ANSIMatrix: class that has ansi "pixels", that has been recieved from converter.

Functions:
ANSIMatrix.copy(self, region): returns another ANSIMatrix, that contains pixels from copied area of parent image
ANSIMatrix.paste(self, region, position): pastes region (ANSIMatrix) to given position.
ANSIMatrix.get_img(self): returns ready-to-print string of ansi "pixels".
colored(img, rescale, use_double_spaces): converts image from file to colored ANSIMatrix.
gray(img, rescale, use_double_spaces, allow_15, debug, inverse): like colored, but returns grayscale ANSIMatrix.
dump(matrix, output): dumps matrix to output file.
load(file): loads matrix from file.

Github page: 
None
