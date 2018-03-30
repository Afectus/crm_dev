#!/bin/bash

runuser -l babah -c 'rsync --delete-after --port=8738 -av 188.246.226.42::babah_media /home/babah/FTP'