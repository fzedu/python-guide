#!/usr/bin/env bash

_prepare()
{
    set -xeo pipefail

    #   project root
    ROOT="$(cd "$(dirname "$0")/.."; pwd;)"

    #   environments
    ENV_PATH="${ROOT}/environments/jekyll.yml"
    ENV_NAME=$(cat "${ROOT}/environments/jekyll.yml" | grep "name:" | cut -d' ' -f2)
    GEMFILE="${ROOT}/environments/Gemfile"

    #   mamba
    export MAMBA_NO_BANNER=1

    #   search for mamba because it's better
    if ( hash mamba > /dev/null 2>&1 ); then
        TOOL=mamba

    elif ( hash conda > /dev/null 2>&1 ); then
        TOOL=conda

    else
        echo "Cannot find 'mamba' or 'conda' to create environment"
        exit 1

    fi
}


case $1 in
    build)
        _prepare
        ${TOOL} env create --quiet --file ${ENV_PATH}
        ${TOOL} run --name ${ENV_NAME} --no-capture-output \
            bundle install --gemfile="${GEMFILE}"
        ;;
    
    run)
        _prepare
        ${TOOL} run --name ${ENV_NAME} --no-capture-output ${ROOT}/scripts/gen_pages.py
        ${TOOL} run --name ${ENV_NAME} --no-capture-output \
            bundle exec --gemfile=${GEMFILE} jekyll serve --source ${ROOT}
        ;;

    remove)
        _prepare
        ${TOOL} env remove --name ${ENV_NAME}
        ;;

    *)
        cat <<- EOF
Usage: $(basename "$0") [build|run|remove]

Commands:
    build   Build environment and install all dependencies.
    run     Run main executable.
    remove  Remove environment and all dependencies.
EOF
        ;;
esac


unset _prepare MAMBA_NO_BANNER