#!/bin/bash

# Script to push container image with retry logic until success
# Usage: ./push_with_retry.sh

IMAGE_NAME="instavm/open-skills:latest"
MAX_ATTEMPTS=100
ATTEMPT=1
INITIAL_WAIT=5
MAX_WAIT=60

echo "Starting container image push with retry logic..."
echo "Image: $IMAGE_NAME"
echo "Will retry until successful"
echo ""

while true; do
    echo "----------------------------------------"
    echo "Attempt #$ATTEMPT ($(date '+%Y-%m-%d %H:%M:%S'))"
    echo "----------------------------------------"

    if container image push "$IMAGE_NAME"; then
        echo ""
        echo "✓ SUCCESS! Image pushed successfully on attempt #$ATTEMPT"
        exit 0
    else
        EXIT_CODE=$?
        echo ""
        echo "✗ Push failed with exit code $EXIT_CODE"

        # Calculate wait time with exponential backoff
        WAIT_TIME=$((INITIAL_WAIT * (ATTEMPT > 3 ? 2 : 1)))
        if [ $WAIT_TIME -gt $MAX_WAIT ]; then
            WAIT_TIME=$MAX_WAIT
        fi

        echo "Waiting ${WAIT_TIME} seconds before retry..."
        sleep $WAIT_TIME

        ATTEMPT=$((ATTEMPT + 1))
    fi
done
