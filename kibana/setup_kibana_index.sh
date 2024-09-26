#!/bin/sh

sleep 100

curl -XPOST -D- "http://kibana:5601/api/saved_objects/index-pattern" \
    -H "Content-Type: application/json" \
    -H "kbn-version: 6.1.0" \
    -d '{"attributes":{"title":"logstash-*","timeFieldName":"@timestamp"}}' && \
    
echo "\r\nIndex pattern created."
