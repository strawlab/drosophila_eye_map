# This script is probably only useful to Andrew Straw when performing
# maintainence of the package.  It will regenerate the .zip file and
# attempt to upload it to Andrew's website.

echo "Andrew: copy the README.txt file into ~/src/astraw-private-repo/work-website/input-code/drosophila_eye_map/README.txt"

VERSION=0.4

git archive --format=zip -v --prefix=drosophila_eye_map-$VERSION/ release-$VERSION > ../drosophila_eye_map-$VERSION.zip

# upload the files
rsync -avzP ../drosophila_eye_map-$VERSION.zip code.astraw.com:/var/websites/code.astraw.com/drosophila_eye_map/download/
