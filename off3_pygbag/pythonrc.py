# pythonrc.py - Optional initialization file for pygame-web
# This file is loaded before the main application starts

import sys
import os

# Set up any global configurations for the web environment
print("Chain Reaction Game - Web Version Loading...")

# Configure pygame for web
import pygame
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)

# Any other initialization can go here
