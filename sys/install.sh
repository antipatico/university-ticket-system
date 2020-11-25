#!/usr/bin/env bash
set -e

if [ -e ./venv ]; then
  echo -e "'venv' folder/file already exists.\nContinuing will result in potential loss of data.\n\n"
  read -p "Are you sure you want to continue? (y/N) " confirm
  shopt -s nocasematch
  [[ $confirm =~ ^y(es)?$ ]] || exit 0
  shopt -u nocasematch
fi

rm -rf ./venv
python3 -m venv --prompt uts-venv ./venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt

cat <<EOF

Project dependencies installed under 'venv'!
Enter the virtualenv using 'source ./venv/bin/activate'
EOF
