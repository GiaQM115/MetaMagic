import subprocess
import os
import sys

if len(sys.argv) != 2:
	print("USAGE: python3 scrub.py path/to/files")
	exit()

def _parsePDFtk(tag_list):
	if len(tag_list) == 0:
		return set()
	if tag_list[-1] == "Done.  Input errors, so no output created.":
		return ''
	tags = set()
	for line in tag_list:
		if line[0:4] == "Info":
			parts = line.lstrip().rstrip().split(":")
			if parts[0] == "InfoKey":
				tags.add(parts[1][1:])
		else:
			try:
				tags.add(line[0:line.index(":")])
			except:
				pass
	return tags


def _parseImageMagick(tag_list):
	tags = set()
	return tags


def _parseExiftool(tag_list):
	tags = set()
	for line in tag_list:
		try:
			tags.add(line[0:line.index(":")].rstrip())
		except:
			pass
	return tags

def _pdftk(name, tags):
	global data_dir
	global pdftk_change_keys
	try:
		subprocess.getoutput(f'pdftk {data_dir}{name} dump_data output pdftk_out.txt')
		with open('pdftk_out.txt', 'r') as infile:
			outfile = open('pdftk_scrub.txt', 'w')
			change_found = False
			for line in infile:
				for key in pdftk_change_keys:
					if line == f"InfoKey: {key}\n":
						change_found = True
						break
				if change_found and line[0:9] == "InfoValue":
						outfile.write("InfoValue: \n")
						change_found = False
						continue
				outfile.write(line)
			outfile.close()
		os.remove('pdftk_out.txt')
						
		subprocess.getoutput(f'pdftk {data_dir}{name} update_info pdftk_scrub.txt output {data_dir}pdftk_scrubbed/{name}')
		os.remove('pdftk_scrub.txt')
		ret = subprocess.getoutput(f'pdftk {data_dir}pdftk_scrubbed/{name} dump_data')
	except:
		ret = None
		print(f'Error scrubbing {name} with PDFtk')
	return ret


def _exiftool(name, tags):
	global data_dir
	try:
		out = subprocess.getoutput(f'exiftool -all= {data_dir}{name}')
		if "Error" in out:
			ret = None
		else:
			ret = subprocess.getoutput(f'exiftool -u {data_dir}{name}')
	except:
		ret = None
	finally:
		try:
			os.rename(f'{data_dir}{name}_original', f'{data_dir}{name}')
		except:
			pass
		return ret

def _imagemagick(name, tags):
	return None


def edit_metadata(tool, filename, metadata):
	global tag_dict
	global switcher
	global switcher2
	func = switcher.get(tool)
	edited = func(filename, tag_dict.get(tool))
	if edited == None:
		return set()
	taglist = []
	for line in metadata:
		if "Error" not in line and "Done" not in line and line not in edited:
			taglist.append(line)
	func = switcher2.get(tool)
	tags = func(taglist)
	return tags


data_dir = sys.argv[1]
data = []

with open('results/display_data.txt', 'r') as infile:
	tmp = []
	for line in infile.readlines():
		if line == "\n":
			if len(tmp) > 0:
				data.append(tmp)
			tmp = []
			continue
		tmp.append(line.rstrip().lstrip())


switcher = {
	'Exiftool': _exiftool,
	'ImageMagick': _imagemagick,
	'PDFtk': _pdftk
}

switcher2 = {
	'Exiftool': _parseExiftool,
	'ImageMagick': _parseImageMagick,
	'PDFtk': _parsePDFtk
}

tag_dict = {
	'Exiftool': list(),
	'ImageMagick': list(),
	'PDFtk': list()
}

edited_tags_dict = {
	'Exiftool': set(),
	'ImageMagick': set(),
	'PDFtk': set()
}

pdftk_change_keys = ['Title', 'Author', 'Subject', 'Producer', 'Keywords']

try:
	os.mkdir(f'{data_dir}pdftk_scrubbed/')
except:
	pass

for tool in tag_dict.keys():
	f = open(f'results/{tool}_tags.txt', 'r')
	tag_dict[tool] = list(map(str.strip, f.readlines()))
	f.close()

for entry in data[1:]:
	tool = entry[1].split(" ")[-1]
	filename = entry[1].split(" ")[0]
	metadata = entry[3::]
	print(f'Scrubbing {tool}\'s metadata for {filename}')
	edited_tags_dict[tool].update(edit_metadata(tool, filename, metadata))

with open('results/edited_tags.txt', 'w') as outfile:
	for tool in edited_tags_dict.keys():
		outfile.write(f'Updated the following tags with {tool}\n')
		for tag in edited_tags_dict[tool]:
			outfile.write(f'{tag}\n')
		outfile.write("-"*50)
		outfile.write('\n')
