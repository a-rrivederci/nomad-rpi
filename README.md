# nomad-rpi

Nomad modules for Raspberry Pi

## NOMAD :robot:

**Nomad** is the terrestrial agent of the Triple-N system. It is an explorer rover enabled with an object detecting trained model which can be controlled remotely.

---  

## Setup

### Raspberry Pi

Tested with Raspberry Pi 3 Model B

1. `sudo raspi-config` and reboot
    - change user password
    - set Hostname (Network Options)
    - connect to WiFi (Network Options)
    - enable camera (Interfacing Options)
    - set Memory Split to 16 MB (Advanced Options)
2. clone this repository: `git clone https://github.com/attackle/nomad.git` and `cd nomad`
3. `pip3 install -r requirements.txt`
4. `sudo apt install vlc libav-tools`
5. create script to livestream: `cd ~` then
    - `echo "raspivid -t 0 -vf -hf -w 640 -h 480 -fps 15 -b 1000000 -o - | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264" > stream.sh`
    	- `-t 0 `: no timeout (stream indefinitely)
    	- `-vf`: vertical flip (flip video vertically)
    	- `-hf1`: horizontal flip (flip video horizontally)
    	- `-w 640 -h 480`: video size 640x480 px
    	- `-fps 15`: frames per second
    	- `-b 1000000`: bit rate
    	- `-o -`: output to STDIN
    	- `access=http`: livestream can be accessed via HTTP
    	- `dst=:8090`: destination is localhost port 8090
    - `chmod a+x stream.sh`

## Execution

### Raspberry Pi
From the home directory (`cd ~` to go there):
- `./stream.sh` to start livestream
- `cd ~/nomad/nomadBrain && python3 nomadBrain.py`
