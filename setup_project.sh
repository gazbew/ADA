#!/bin/bash
# Setup script for the ADA project, handling both backend and frontend installations

echo "Setting up ADA project..."

# Install backend dependencies
echo "Installing backend dependencies..."
python install_dependencies.py

# Install frontend dependencies
echo "Moving to frontend directory for npm install..."
cd client/ada-online
if [ -f "package.json" ]; then
    echo "Found package.json, running npm install..."
    npm install
else
    echo "Error: package.json not found in client/ada-online directory."
    exit 1
fi

echo "Frontend setup complete. Returning to root directory."
cd ../..

echo "Project setup complete. Backend and frontend dependencies installed."