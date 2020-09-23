import os
import subprocess

data_dir = '/home/giaqm/Desktop/pentesting/metadata_lab/files'
image_types = ["png", "jpg", "jpeg", "gif", "tiff"]


def get_extension(filename):
	indices = []
	for i, c in enumerate(filename):
		if c == '.':
			indices.append(i)
	return filename[indices[-1]+1:].lower()

if not 'results' in os.listdir():
	try:
		os.mkdir('results')
	except:
		print('ERROR: could not make results directory!')
		exit()

outfile = open("display_data.txt", 'w')

print("===EXTRACTING METADATA===")
for f in os.listdir(data_dir):
	outfile.write("\n")
	outfile.write("---")
	outfile.write(f'{f} extracted with Exiftool')
	outfile.write("---")
	outfile.write(subprocess.getoutput(f'exiftool -u {data_dir}/{f}'))
	outfile.write("\n")
	if get_extension(f) in image_types:
		outfile.write("---")
		outfile.write(f'{f} extracted with ImageMagick')
		outfile.write("---")
		outfile.write(subprocess.getoutput(f'identify -verbose {data_dir}/{f}'))
		outfile.write("\n")
	elif get_extension(f) == 'pdf':
		outfile.write("---")
		outfile.write(f'{f} extracted with PDFtk')
		outfile.write("---")
		outfile.write(subprocess.getoutput(f'pdftk {data_dir}/{f} dump_data'))
		outfile.write("\n")

print("===EXTRACTION COMPLETE===")
print("File list and data in results/display_data.txt")
