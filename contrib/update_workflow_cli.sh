#!/bin/bash

if [ -n "${CI_COMMIT_TAG}" ]; then
    version=$(curl -Ls https://github.com/drycc/workflow-cli/releases|grep /drycc/workflow-cli/releases/tag/ | sed -E 's/.*\/drycc\/workflow-cli\/releases\/tag\/(v[0-9\.]{1,}(-rc.[0-9]{1,})?)".*/\1/g' | head -1)
    sed -i "s/xtermPodImageTag: canary/xtermPodImageTag: ${version#v}/g" charts/manager/values.yaml
fi