# OpenCV installation

## tutorial: https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/

Note: these instructions have been tested on a Raspberry Pi 3 Model B with Raspbian Stretch

## Advanced Options > Expand Filesystem
sudo raspi-config

sudo reboot

sudo apt update && sudo apt upgrade

## install some developer tools
sudo apt install -y build-essential cmake pkg-config

## install some image I/O packages
sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

## install some video I/O packages
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcode-dev libx264-dev

## GTK dev lib is required to compile OpenCV
sudo apt install -y libgtk2.0-dev libgtk-3-dev

## some extra libs to optimize OpenCV operations
sudo apt-get install -y libatlas-base-dev gfortran

## install header files for both Python 2.7 and 3 so we can compile OpenCV with Python bindings
sudo apt-get install -y python2.7-dev python3-dev

## install pip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py

## install venv
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip

## add following lines to ~/.profile
```
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_SCRIPT=/usr/local/bin/virtualenvwrapper.sh
source /usr/local/bin/virtualenvwrapper_lazy.sh
```

## reload ~/.profile
source ~/.profile

## create virtual environment named 'cv' using python3
mkvirtualenv cv -p python3

## to stop using virtualenv
deactivate

## to use virtualenv 'cv'
source ~/.profile
workon cv

## when using virtualenv, bash promt should appear as follow
(cv) pi@nomad-rpi:~ $ 

## install NumPy
pip install numpy

## setup build for OpenCV
cd ~/opencv-3.3.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D BUILD_EXAMPLES=ON ..

## examine 'Python 3' section in cmake output
interpreter and numpy should point to the installations in the 'cv' virtualenv

## edit the CONF_SWAPSIZE variable in /etc/dphys-swapfile
CONF_SWAPSIZE=1024

## restart swap service to activate new swap space
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

## compile OpenCV
make -j4

## install OpenCV
sudo make install
sudo ldconfig

## rename the output file
cd /usr/local/lib/python3.5/site-packages/
sudo mv cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so

## create symbolic link for OpenCV bindings in 'cv' virtual environment
cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
ln -s /usr/local/lib/python3.5/site-packages/cv2.so cv2.so


# test OpenCV installation

## open new terminal
source ~/.profile
workon cv
python
>>> import cv2
>>> cv2.__version__
//output should be: '3.3.0'

# cleanup

## delete unnecessary files/folders
rm -rf opencv-3.3.0 opencv_contrib-3.3.0

## change the CONF_SWAPSIZE variable in /etc/dphys-swapfile back to 100
CONF_SWAPSIZE=100

## restart swap service to activate new swap space
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
