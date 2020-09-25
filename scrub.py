import subprocess

def _parsePDFtk(tag_list):
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
	for line in tag_list:
		if ":" in line:
			for i in range(0,len(line)-2):
				if line[i] == ":" and line[i+1] == " ":
					tags.add(line[0:i])
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
	return f"pdftk: {name}"


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
		return ret

def _imagemagick(name, tags):
	global data_dir
	return f"imagemagick: {name}"


def edit_metadata(tool, filename, metadata):
	global tag_dict
	global switcher
	global switcher2
	func = switcher.get(tool)
	edited = func(filename, tag_dict.get(tool))
	if edited == None:
		return "No edits made"
	taglist = []
	for line in metadata:
		if "Error" not in line and "Done" not in line and line not in edited:
			taglist.append(line)
	func = switcher2.get(tool)
	tags = func(taglist)
	print("-"*50)
	print(f'Scrubbed with {tool}:')
	for tag in tags:
		print(f'\t{tag}')


data_dir = '/home/giaqm/Desktop/pentesting/metadata_lab/files/'
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

for tool in tag_dict.keys():
	f = open(f'results/{tool}_tags.txt', 'r')
	tag_dict[tool] = list(map(str.strip, f.readlines()))
	f.close()

for entry in data[1:]:
	tool = entry[1].split(" ")[-1]
	filename = entry[1].split(" ")[0]
	metadata = entry[3::]
	edit_metadata(tool, filename, metadata)
