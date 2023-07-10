#!/usr/bin/env bash
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
