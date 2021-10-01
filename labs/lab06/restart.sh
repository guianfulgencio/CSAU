#!/bin/bash

# This file will contain content needed to prepare the environment needed to start the lab03.

LAB03_REPOS="/home/student/labs/csau/section04/lab03/repos"

if [[ -d "$LAB03_REPOS" ]]; then
  echo "Erasing LAB03 REPOS DIR"
  rm -rf $LAB03_REPOS
fi

LAB03_REMOTE="/home/student/git/inventory.git"

if [[ -d "$LAB03_REMOTE" ]]; then
  echo "Erasing LAB03_REMOTE DIR"
  rm -rf $LAB03_REMOTE
fi

# Copy bare repo from the original source into /home/student/git
cp -r /opt/ntc/csau/repos/labs/csau/section04/lab03/inventory.git /home/student/git

