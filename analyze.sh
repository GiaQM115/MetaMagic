clear
echo Please provide the path to files:
read path_in

if [[ $path_in = */ ]] 
then
	path=$path_in
else
	path="${path_in}/"
fi

echo Create backup for files? Yes or No
echo Note: You will not be able to run cleanup without this directory
read backup

if [[ $backup -eq 'Yes' ]]
then
	backup_path=$(echo ${path_in%/} | awk 'BEGIN{FS=OFS="/"}{NF--; print}')/backup_files
	mkdir $backup_path
	cp ${path}* $backup_path
	echo Backup located at $backup_path
	ls $backup_path
fi

echo Extracting files from $path

python3 display_data.py $path
python3 parse_tags.py
python3 scrub.py $path
python3 unchanged.py

echo Analysis complete. See results/ for full results.

head -n 1 results/taglist.txt
head -n 1 results/unchanged_tags.txt

echo Run cleanup? Yes or Not
echo Note: This will revert all changed files back to their originals.
read cleanup

if [[ $cleanup -eq 'Yes' ]]
then
	rm -rf $path
	mkdir $path
	cp $backup_path/* $path
	echo Original files restored to $path
	ls $path
fi
