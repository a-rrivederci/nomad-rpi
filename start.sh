#!/bin/bash
# modprobe v4l2_common && python brain.py &
# raspivid -t 0 -vf -hf -w 640 -h 480 -fps 15 -b 1000000 -o - | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264

# Start the nomad-rpi program
python3 -m brain
