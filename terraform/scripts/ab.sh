#!/bin/bash

# Variables
LB_ENDPOINT="http://34.110.204.159/api/sobel"
CONCURRENCY=1000
NUM_REQUESTS=10000000

# Run Apache Bench to generate traffic
ab -n $NUM_REQUESTS -c $CONCURRENCY $LB_ENDPOINT