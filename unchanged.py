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

with open('results/unchanged_tags.txt', 'w') as outfile:
	outfile.write(f"{len(unchanged)} tags remained unchanged\n")
	for tag in unchanged:
		outfile.write(f"{tag}\n")
