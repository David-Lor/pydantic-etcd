#!/bin/bash

set -ex

docker run --rm \
    --name=etcd_testing \
    -p 127.0.0.1:2379:2379 \
    -e ALLOW_NONE_AUTHENTICATION=yes \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/timezone:/etc/timezone:ro \
    bitnami/etcd
