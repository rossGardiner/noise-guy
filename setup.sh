wget https://noise-guy.s3.eu-west-2.amazonaws.com/noise-sources.tar.xz
tar -xf noise-sources.tar.xz
rm noise-sources.tar.xz

wget https://noise-guy.s3.eu-west-2.amazonaws.com/gtzan.tar.xz
tar -xf genres.tar.xz
rm gtzan.tar.gz

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt


