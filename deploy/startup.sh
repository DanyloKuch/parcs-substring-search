#!/bin/bash
iptables -C INPUT -s 10.0.0.0/8 -j ACCEPT 2>/dev/null || iptables -I INPUT -s 10.0.0.0/8 -j ACCEPT
iptables -C INPUT -p tcp --dport 8080 -j ACCEPT 2>/dev/null || iptables -I INPUT -p tcp --dport 8080 -j ACCEPT
ARGS=$(curl -s -H 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/attributes/parcs-args)
docker rm -f parcs >/dev/null 2>&1
docker run -d --name parcs --restart=always --network=host -e PARCS_ARGS="$ARGS" registry.hub.docker.com/hummer12007/parcs-node
