#!/usr/bin/env bash
echo "5 Clients"
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 
sleep 5

echo ""
echo "4 Clients"
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 
sleep 5

echo ""
echo "3 Clients"
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 
sleep 5

echo ""
echo "2 Clients"
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 &
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 
sleep 5

echo ""
echo "1 Clients"
python3 ./client/HTTPClient.py 73.186.87.78 56893 0.5 1 
sleep 5

return
