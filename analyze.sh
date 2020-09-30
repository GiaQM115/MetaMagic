clear
echo Please provide the path to files:
read path_in

if [[ $path_in = */ ]] 
then
	path=$path_in
else
	path=$path_in/
fi

echo Extracting files from $path

python3 display_data.py $path
python3 parse_tags.py
python3 scrub.py $path
python3 unchanged.py

echo Analysis complete. See results/ for full results.

head -n 1 results/taglist.txt
head -n 1 results/unchanged_tags.txt
