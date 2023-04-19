#!/bin/bash

echo “################# Starting node for this MAC #################"

java -jar selenium-server-standalone-2.53.0.jar -role node -nodeConfig StartMacDesktopNode.json