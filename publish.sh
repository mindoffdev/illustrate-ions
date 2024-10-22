#!/bin/bash
# Run the Python file
python imagecompress-inator.py  # Assuming script.py is in the same folder as the shell script

# Git commands
git add .
git commit -m "Auto commit: $(date +"%Y-%m-%d %H:%M:%S")"
git push
