#!/bin/bash

## this requires that 
## source oe-init-build-env
## has already been done (at yocto root)
cd ../../build

bitbake-layers add-layer ../meta-helmet && echo "You have successfully added meta-helmet to the bblayers.conf"
