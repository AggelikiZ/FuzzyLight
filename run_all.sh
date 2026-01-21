#!/bin/bash

# Ορισμός του μοντέλου
MODEL="FuzzyLight"
TIMESTAMP=$(date +"%m_%d_%H_%M")

echo "Starting automated runs for all cities..."

# # 1. HANGZHOU
# echo "---------------------------------------"
# echo "Running HANGZHOU..."
# python run_fuzzylight.py -hangzhou -mod $MODEL -memo "docker_run_hz_all"
# echo "Hangzhou finished."

# # 1. HANGZHOU
# echo "---------------------------------------"
# echo "Running HANGZHOU..."
# python run_fuzzylight.py -hangzhou -mod $MODEL -memo "docker_run_seg8" -segments 8
# echo "Hangzhou finished."

# # 1. HANGZHOU
# echo "---------------------------------------"
# echo "Running HANGZHOU..."
# python run_fuzzylight.py -hangzhou -mod $MODEL -memo "docker_run_seg16" -segments 16
# echo "Hangzhou finished."

# # 1. HANGZHOU
# echo "---------------------------------------"
# echo "Running HANGZHOU..."
# python run_fuzzylight.py -hangzhou -mod $MODEL -memo "docker_run_seg24" -segments 24
# echo "Hangzhou finished."




# 2. JINAN
echo "---------------------------------------"
echo "Running JINAN..."
python run_fuzzylight.py -jinan -mod $MODEL -memo "docker_run_jn_all"
echo "Jinan finished."

# 3. NEW YORK
# echo "---------------------------------------"
# echo "Running NEW YORK..."
# python run_fuzzylight.py -newyork -mod $MODEL -memo "docker_run_nw_stage_2"
# echo "New York finished."

# echo "---------------------------------------"
# echo "All cities have been processed!"