#!/bin/bash

version=`cat VERSION`
image=jolleon/chameleon

docker tag $image:latest $image:$version

docker push $image:latest
docker push $image:$version
