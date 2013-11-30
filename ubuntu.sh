apt-get install python3 python3-pyqt4 python3-pip
pip3 install selenium,BeautifulSoup4
sudo mkdir -p /opt/sonot
_dir=`pwd`
cp -r _dir /opt/sonot/
sudo chmod 755 /opt/sonot/stackoverflow-notifications/sonot.py
sudo cp sonot /usr/bin/sonot