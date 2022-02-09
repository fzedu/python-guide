#!/usr/bin/env bash

set -xeo pipefail

ROOT="$(cd "$(dirname "$0")/.."; pwd;)"
ENV_FILE="${ROOT}/environments/Gemfile"

gem install bundler

bundle install --gemfile=${ENV_FILE}

bundle exec --gemfile=${ENV_FILE} jekyll build
bundle exec --gemfile=${ENV_FILE} rubocop -D --config .rubocop.yml
bundle exec --gemfile=${ENV_FILE} ${ROOT}/scripts/validate-html.rb

