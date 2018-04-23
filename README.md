# nomad-rpi

Nomad modules for Raspberry Pi

## Index

1. [Setup](#setup)
2. [Testing](#testing)
3. [Execution](#execution)

&nbsp;

## Setup

Setting up the Pi
>Tested with Raspberry Pi 3 Model B

1. `sudo raspi-config`
    - change user password
    - set Hostname (Network Options)
    - connect to WiFi (Network Options)
    - enable camera (Interfacing Options)
    - set Memory Split to 16 MB (Advanced Options)
    - reboot
2. Clone this repository
```bash
git clone https://github.com/attackle/nomad-rpi.git
cd nomad-rpi
```
3. Install requirements
```bash
pip3 install -r requirements.txt
```
4. Install dependencies
```bash
sudo apt install vlc libav-tools
```
5. Create script to livestream: 
```bash
cd ~
echo "raspivid -t 0 -vf -hf -w 640 -h 480 -fps 15 -b 1000000 -o - | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264" > stream.sh
chmod a+x stream.sh
```
- `-t 0 `: no timeout (stream indefinitely)
- `-vf`: vertical flip (flip video vertically)
- `-hf1`: horizontal flip (flip video horizontally)
- `-w 640 -h 480`: video size 640x480 px
- `-fps 15`: frames per second
- `-b 1000000`: bit rate
- `-o -`: output to STDIN
- `access=http`: livestream can be accessed via HTTP
- `dst=:8090`: destination is localhost port 8090

&nbsp;

## Testing

Running unittests on the module
```bash
python3 -m unitest discover -v
```

&nbsp;

## Execution

From the home directory (`cd ~` to go there):
- `./stream.sh` to start livestream
- `cd ~/nomad-rpi && python3 brain.py`
