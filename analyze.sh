echo Please provide the path to files:
read path

echo Extracting files from $path

python3 display_data.py $path
python3 parse_tags.py
python3 scrub.py $path

echo Analysis complete. See results/
