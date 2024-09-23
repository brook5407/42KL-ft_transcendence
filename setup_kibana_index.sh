#!/bin/sh

until $(curl --output /dev/null --silent --head --fail http://kibana:5601/api/status); do
    printf '.'
    sleep 5
done

curl -XPOST -D- "http://kibana:5601/api/saved_objects/index-pattern" \
    -H "Content-Type: application/json" \
    -H "kbn-version: 6.1.0" \
    -d '{"attributes":{"title":"logstash-*","timeFieldName":"@timestamp"}}' && \
echo "Index pattern created."
