#!/bin/sh

# install script

SRC_PATH=$(cd "$(dirname "$0")";pwd)

cd $SRC_PATH

[ -d tmp ] || mkdir tmp

SRC_PATH_ENCODED=${SRC_PATH//\//\\\/}

sed -e "s/{DIR}/${SRC_PATH_ENCODED}/g" run.sh.template > run.sh