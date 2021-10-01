#!/bin/bash

# This file will contain content needed to prepare the environment needed to start the lab01.

LAB01_REPOS="/home/student/labs/csau/section04/lab01/repos"

if [[ -d "$LAB01_REPOS" ]]; then
  echo "Erasing LAB01 REPOS DIR"
  rm -rf $LAB01_REPOS
fi

LAB01_REMOTE="/home/student/git/backups.git"

if [[ -d "$LAB01_REMOTE" ]]; then
  echo "Erasing LAB01_REMOTE DIR"
  rm -rf $LAB01_REMOTE
fi

# Copy bare repo from the original source into /home/student/git
cp -r /opt/ntc/csau/repos/labs/csau/section04/lab01/backups.git /home/student/git
