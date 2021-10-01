#!/bin/bash

# This file will contain content needed to prepare the environment needed to start the lab02.

LAB02_REPOS="/home/student/labs/csau/section04/lab02/repos"

if [[ -d "$LAB02_REPOS" ]]; then
  echo "Erasing LAB02 REPOS DIR"
  rm -rf $LAB02_REPOS
fi

LAB02_REMOTE="/home/student/git/scripts.git"

if [[ -d "$LAB02_REMOTE" ]]; then
  echo "Erasing LAB02_REMOTE DIR"
  rm -rf $LAB02_REMOTE
fi

# Copy bare repo from the original source into /home/student/git
cp -r /opt/ntc/csau/repos/labs/csau/section04/lab02/scripts.git /home/student/git

