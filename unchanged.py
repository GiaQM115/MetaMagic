with open('results/taglist.txt', 'r') as infile:
	all_tags = map(str.rstrip, infile.readlines()[1::])

with open('results/edited_tags.txt', 'r') as infile:
	edited_tags = set()
	for line in [l.rstrip() for l in infile.readlines()]:
		if line[0:7] == "Updated" or line[0] == "-":
			continue
		edited_tags.add(line)

unchanged = []
for tag in all_tags:
	if not tag in edited_tags:
		unchanged.append(tag)

with open('results/Exiftool_tags.txt', 'r') as exif_in:
	with open('results/PDFtk_tags.txt', 'r') as pdf_in:
		attempted = list(map(str.rstrip, exif_in.readlines()))
		for t in map(str.rstrip, pdf_in):
			attempted.append(t)

tried_but_no = set()
for tag in attempted:
	if not tag in edited_tags:
		tried_but_no.add(tag)

with open('results/unchanged_tags.txt', 'w') as outfile:
	outfile.write(f"{len(unchanged)} tags remained unchanged\n")
	for tag in unchanged:
		outfile.write(f"{tag}\n")
	outfile.write("-"*50)
	outfile.write("\nUnchanged but Attempted:\n")
	for tag in tried_but_no:
		outfile.write(f"{tag}\n")
	outfile.write("-"*50)
	outfile.write("\nImageMagick Only Tags:\n")
	for tag in set(unchanged).symmetric_difference(set(tried_but_no)):
		outfile.write(f"{tag}\n")
