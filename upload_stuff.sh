# This script is probably only useful to Andrew Straw when performing
# maintainence of the package.  It will regenerate the webpage, the
# .zip file, and attempt to upload them to Andrew's website.

echo "Andrew: copy the README.txt file into ~/src/astraw-private-repo/work-website/input-code/drosophila_eye_map/README.txt"

VERSION=0.3

# generate the .zip file
rm -rf tmp
mkdir tmp
bzr export tmp/drosophila_eye_map-$VERSION
cd tmp
zip -9 -r drosophila_eye_map-$VERSION.zip drosophila_eye_map-$VERSION
cd ..

# upload the files
rsync -avzP tmp/drosophila_eye_map-$VERSION.zip code.astraw.com:/var/websites/code.astraw.com/drosophila_eye_map/download/
