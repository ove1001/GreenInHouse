#!/bin/bash

TEMP_DIR="$(mktemp -d)"

# Install
cp -R * "${TEMP_DIR}"
pushd "${TEMP_DIR}"
pip3 install .
popd

rm -R "${TEMP_DIR}"

# Create admin:admin user
dms2223auth-create-admin
