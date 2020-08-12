#!/bin/bash 
/wait-for `echo $ARCOR2_PERSISTENT_STORAGE_URL`/projects 
cd /root/data/
python3 -m http.server 8888 &
arcor2_server