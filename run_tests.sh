#!/bin/bash

set -eu

function usage {
  echo "Usage: $0 [OPTION]..."
  echo "Run cloudcafe test suite(s)"
  echo ""
  echo "  -p, --pep8                  Just run PEP8 and HACKING compliance check"
  echo "  -P, --no-pep8               Don't run static code checks"
  echo "  -h, --help                  Print this usage message"
  echo "  -k <string>                 Select tests matching <string>"
  echo "  -m <mark>                   Run tests marked as <mark>. Ex: -m 'mark1 and not mark2'"
  echo ""
  exit
}

function process_options {
  i=1
  while [ $i -le $# ]; do
    case "${!i}" in
      -h|--help) usage;;
      -p|--pep8) just_pep8=1;;
      -P|--no-pep8) no_pep8=1;;
      --k)
        (( i++ ))
        select=${!i}
        ;;
      --m)
        (( i++ ))
        mark=${!i}
        ;;
        *) testrargs="$testrargs ${!i}"
    esac
    (( i++ ))
  done
}

just_pep8=0
no_pep8=0
select=
mark=
testargs=

process_options $@

LANG=en_US.UTF-8
LANGUAGE=en_US:en
LC_ALL=C

function run_tests {
  # Cleanup *pyc
  echo "Cleaning compiled files..."
  find . -type f -name "*.pyc" -delete
  echo "Running tests ..."
  if [ -n "$select" ]; then
    testargs="$testargs -k $select"
  fi
  if [ -n "$mark" ]; then
    testargs="$testargs -m $mark"
  fi
  py.test "${testargs}"

  if [ $no_pep8 -eq 0 ]; then
    run_pep8
  fi
}

function run_pep8 {
  echo "Running flake8 ..."
  flake8 .
}

if [ $just_pep8 -eq 1 ]; then
    run_pep8
    exit
fi

run_tests
