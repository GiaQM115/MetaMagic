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

outfile = open("results/display_data.txt", 'w')

print("===EXTRACTING METADATA===")
for f in os.listdir(data_dir):
	outfile.write("\n")
	outfile.write("---\n")
	outfile.write(f'{f} extracted with Exiftool\n')
	outfile.write("---\n")
	outfile.write(subprocess.getoutput(f'exiftool -u {data_dir}/{f}\n'))
	outfile.write("\n")
	if get_extension(f) in image_types:
		outfile.write("\n---\n")
		outfile.write(f'{f} extracted with ImageMagick\n')
		outfile.write("---\n")
		outfile.write(subprocess.getoutput(f'identify -verbose {data_dir}/{f}\n'))
		outfile.write("\n")
	elif get_extension(f) == 'pdf':
		outfile.write("\n---\n")
		outfile.write(f'{f} extracted with PDFtk\n')
		outfile.write("---\n")
		outfile.write(subprocess.getoutput(f'pdftk {data_dir}/{f} dump_data\n'))
		outfile.write("\n")

outfile.close()

print("===EXTRACTION COMPLETE===")
print("File list and data in results/display_data.txt")
