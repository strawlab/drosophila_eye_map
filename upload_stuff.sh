# This script is probably only useful to Andrew Straw when performing
# maintainence of the package.  It will regenerate the webpage, the
# .zip file, and attempt to upload them to Andrew's website.

echo "This file is outdated and therefore broken."
echo "copy the README.txt file into work-webste/input-code/projects/drosophila_eye_map/README.txt and run ./build.sh"
exit 1

# generate index.html from README.txt
rst2html --stylesheet=../../default.css --link-stylesheet -g -d -s README.txt index.html

VERSION=0.2

# generate the .zip file
rm -rf tmp
mkdir tmp
bzr export tmp/drosophila_eye_map-$VERSION
cd tmp
zip -9 -r drosophila_eye_map-$VERSION.zip drosophila_eye_map-$VERSION
cd ..

# upload the files
rsync -avzP index.html code.astraw.com:/var/websites/code.astraw.com/projects/drosophila_eye_map/
rsync -avzP tmp/drosophila_eye_map-$VERSION.zip code.astraw.com:/var/websites/code.astraw.com/projects/drosophila_eye_map/download/
