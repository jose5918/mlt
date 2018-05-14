#! /bin/bash
set -e

echo "${GKE_CREDENTIALS}" | base64 -d > mltkey.json
echo "${TEST_VAR}" | base64 --d > mlttest.json
