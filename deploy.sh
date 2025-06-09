#!/bin/bash

# Start the backend server
echo "Starting backend server..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
python main.py &
BACKEND_PID=$!

# Start the frontend development server
echo "Starting frontend server..."
cd ../frontend
npm install
npm start &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Set up trap to catch termination signal
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 