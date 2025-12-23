#!/bin/bash
# start.sh



echo "Running metadata ingestion..."
python Metadata.py
sleep 30
#uvicorn Data_API:app --reload --port 8000 &

# !!!!!!!!!! for Docker we shouldn't write --reload!!!!!!!!!!!
uvicorn Data_API:app --host 0.0.0.0 --port 8000 &



#uvicorn Prediction_API:app --reload --port 8001 &

# !!!!!!!!!! for Docker we shouldn't write --reload!!!!!!!!!!!
uvicorn Prediction_API:app --host 0.0.0.0 --port 8001 &


#if you write this for Docker, add these:

wait -n

exit $?
