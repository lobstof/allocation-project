#!/bin/bash
fileid="1-usXUQ-AkHZOBjtv1RuOMUOK-j0l8-pU"
filename="cdnyoutube.tar"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}


