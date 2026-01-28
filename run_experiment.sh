#!/bin/bash
# Experiment runner with API key setup

echo "==================================="
echo "  Routing Experiment Runner"
echo "==================================="
echo ""

# Check if API key is set
if [ -z "$GOOGLE_API_KEY" ] && [ -z "$GOOGLE_GENAI_API_KEY" ]; then
    echo "⚠️  GOOGLE_API_KEY not set!"
    echo ""
    echo "Please set your API key:"
    echo "  export GOOGLE_API_KEY=\"your-api-key-here\""
    echo ""
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    exit 1
fi

echo "✓ API key found"
echo ""

# Set environment variables
export GOOGLE_GENAI_USE_VERTEXAI=false

# Run the experiment
python3 experiment.py --mode quick --queries 5
