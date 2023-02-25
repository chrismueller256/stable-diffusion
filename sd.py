#!/usr/bin/env python3

import os
import sys
import time
import random
import re
import hashlib
import json

DIM_INC = 64
MODES = ["TXT2IMG", "IMG2IMG", "TXT2IMG_OLD"]

class Parameters:
    def __init__(self, rawJSON):
        self.dict = json.loads(rawJSON)
        self.seed = 0
        self.randomSeed = True
        self.numSamples = 3
        self.numIter = 1
        self.numSteps = 500
        self.width = DIM_INC * 16
        self.height = DIM_INC * 24
        self.mode = MODES[0]

# Params
seed = 387974712
randomSeed = True
numSamples = 3
numIter = 3
numSteps = 128
width = 64 * 8
height = 64 * 12
# width = 64 * 16
# height = 64 * 24
# width = 64 * 24
# height = 64 * 18
#1024x768

# IMG2IMG params
strength = 0.65
testMode = False

# Mode
mode = MODES[0]

# Script
scriptPath = ''
if mode == MODES[0]:
    scriptPath = "optimizedSD/optimized_txt2img.py"
if mode == MODES[1]:
    scriptPath = "optimizedSD/optimized_img2img.py"
if mode == MODES[2]:
    scriptPath = "scripts/txt2img.py"

# Model Checkpoint
checkpoints = [
    # "sd-v1-4.ckpt",
    # "v1-5-pruned-emaonly.ckpt",
    # "v1-5-pruned.ckpt",
    # "artErosAerosATribute_aerosNovae.ckpt", # Broken
    "chilloutmix_NiCkpt.ckpt",
    "deliberate_v11.ckpt",
    "dreamshaper_33.ckpt", # Versatile, Anime/Character art
    # "elldrethsLucidMix_v10.ckpt",  # Cartoony and saturated
    "uberRealisticMerge_urpmv12.ckpt", # Photorealistic people
]

# Input image for img2img
inputPath = "/mnt/c/Users/chris/Desktop/stable-diffusion-optimized/input/"
# inputImageName = "689654732_00054.png"
# inputImageName = "IMG_3723.JPG"
inputImageName = "698214922_00005.png"
inputImage = inputPath + inputImageName

# Join prompt from args
args = sys.argv
prompt = " ".join(args[1:])

# Base out dir
outDir = ''
if mode == MODES[0]:
    outDir = "/mnt/c/Users/chris/Desktop/stable-diffusion-optimized/images/"
if mode == MODES[1]:
    outDir = "/mnt/c/Users/chris/Desktop/stable-diffusion-optimized/images2images/"
if mode == MODES[2]:
    outDir = "/mnt/c/Users/chris/Desktop/stable-diffusion/images/"

# Join Prompt
rootName = re.escape("_".join(args[1:]))
if testMode:
    rootName += "_0"

# Use a truncated description and hash if prompt is too long and write it to a file
if len(rootName) > 25:
    rootName = "_".join(args[1:4]) + "_" + hashlib.md5(bytes(rootName, 'utf-8')).hexdigest()
    os.system("mkdir -p " + outDir + rootName)
    os.system("echo " + prompt + " > " + outDir + rootName + "/prompt.txt")

start = time.time()

iterations = 1

for i in range(iterations):
    # Randomize seed per iteration
    if randomSeed:
        seed = random.randint(0, 4294967295)

    for checkpoint in checkpoints:
        # Build Command
        command = ''
        command += 'python ' + scriptPath
        if mode == MODES[2]:
            command += ' --plms --skip_grid'
        else:
            command += ' --turbo'
        command += ' --ckpt ' + checkpoint
        command += ' --n_samples ' + str(numSamples)
        command += ' --n_iter ' + str(numIter)
        command += ' --ddim_steps ' + str(numSteps)
        command += ' --outdir ' + outDir + rootName + "/ckpt_" + checkpoint + "/"
        if mode == MODES[1]:
            command += inputImageName + "/"
        command += ' --seed ' + str(seed)
        command += ' --W ' + str(width)
        command += ' --H ' + str(height)
        command += ' --prompt "' + prompt + '"'
        if mode == MODES[1]:
            command += ' --strength "' + str(strength) + '"'
            command += ' --init-img "' + inputImage + '"'

        # Fire command
        os.system(command)

    # Touch the dir to bump last update
    os.system("touch " + outDir + rootName)

print('Elapsed: ' + str(time.time()-start) + 's')
