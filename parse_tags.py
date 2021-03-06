
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
	tags_by_file("PDFtk", tags)
	return tags


def _parseImageMagick(tag_list):
	tags = set()
	for line in tag_list:
		if ":" in line:
			for i in range(0,len(line)-2):
				if line[i] == ":" and line[i+1] == " ":
					tags.add(line[0:i])
	tags_by_file("ImageMagick", tags)
	return tags


def _parseExiftool(tag_list):
	tags = set()
	for line in tag_list:
		try:
			tags.add(line[0:line.index(":")].rstrip())
		except:
			pass
	tags_by_file("Exiftool", tags)
	return tags


def parser(tool, tags, fname):
	global switcher
	func = switcher.get(tool)
	try:
		ret = func(tags)
	except:
		ret = f"Error in tag parsing for {fname} from {tool}"
	return ret


def tags_by_file(tool, tags):
	global switcher2
	tagset = switcher2.get(tool)
	try:
		tagset.update(tags)
	except:
		print(f"Could not update tags for {tool}")

files = []
with open('results/display_data.txt', 'r') as infile:
	tmp = []
	for line in infile.readlines():
		if line == "\n":
			if len(tmp) > 0:
				files.append(tmp)
			tmp = []
			continue
		tmp.append(line.rstrip().lstrip())
switcher = {
	'PDFtk' : _parsePDFtk,
	'ImageMagick': _parseImageMagick,
	'Exiftool': _parseExiftool
}

switcher2 = {
	'PDFtk' : set(),
	'ImageMagick': set(),
	'Exiftool': set()
}

all_tags = set()
for t in files:
	tool = t[1].split(" ")[-1]
	f = t[1].split(" ")[0]
	all_tags.update(parser(tool, t, f))


tags_final = []
for t in all_tags:
	try:
		n = float(t)
		continue
	except ValueError:
		tags_final.append(t)

with open("results/taglist.txt", "w") as outfile:
	outfile.write(f"Found {len(tags_final)} unique tags from 3 tools.\n")
	for t in sorted(tags_final, key=str.casefold):
		outfile.write(f"{t.lstrip()}\n")

for k in switcher2.keys():
	f = open(f'results/{k}_tags.txt', 'w')
	for tag in switcher2.get(k):
		f.write(f"{tag}\n")
	f.close()

print("List of tags written to results/taglist.txt")
