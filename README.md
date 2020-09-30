# Welcome to MetaMagic
**MetaMagic** is a command line tool that utilizes 3 free, cross-platform, open-source tools to view, analyze and edit the metadata in various files.
---
## Contents
* **analyze.sh**: driver for execution
* **display_data.py**: extract metadata from files and save output to results directory
* **parse_tags.py**: compile all extracted tags, alphabetize, and remove duplicates
* **scrub.py**: attempt to scrub metadata from files
* **unchanged.py**: create report on tags that remained unchanged during scrubbing

## Usage
`./analyze.sh`
The driver will prompt you for input as needed

## Tool Man Pages
* [PDFtk](https://linux.die.net/man/1/pdftk)
* [ExifTool](https://linux.die.net/man/1/exiftool)
* [ImageMagick](https://linux.die.net/man/1/imagemagick)
