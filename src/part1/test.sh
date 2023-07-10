#!/usr/bin/env bash
echo "9 Clients"
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py
sleep 5

echo ""
echo 8 Clients"
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py
sleep 5

echo ""
echo "7 Clients"
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py
sleep 5

echo ""
echo "6 Clients"
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py
sleep 5

echo ""
echo "5 Clients"
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py
sleep 5

echo ""
echo "4 Clients"
Python3 client.py &
Python3 client.py &
Python3 client.py &
Python3 client.py
sleep 5

echo ""
echo "3 Clients"
Python3 client.py &
Python3 client.py &
Python3 client.py
sleep 5

echo ""
echo "2 Clients"
Python3 client.py &
Python3 client.py
sleep 5

echo ""
echo "1 Clients"
Python3 client.py

return
