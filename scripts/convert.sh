#!/usr/bin/env bash

ROOT="$(cd "$(dirname "$0")/.."; pwd;)"

set -xeo pipefail

for note in $(ls "$ROOT/notes/"*.ipynb | xargs); do
    jupyter nbconvert --to html $note
done
