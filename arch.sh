pacman -S python python-pyqt4 python-pip
pip3 install selenium
sudo mkdir -p /opt/sonot
_dir=`pwd`
cp -r $_dir /opt/sonot/
sudo cp sonot /usr/bin/sonot
sudo chmod 755 /opt/sonot/stackoverflow-notifications/sonot.py
