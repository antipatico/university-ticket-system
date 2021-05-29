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
python3 -m pip install --upgrade pip wheel
python3 -m pip install -r requirements.txt
cat <<EOF

Project dependencies installed under 'venv'!
Enter the virtualenv using 'source ./venv/bin/activate'
You can populate the db using with some test data using './manage.py populatedb'
WARNING: the populatedb command will create some local users and an administrator account.

NOTE: to create a local administrator account use './manage.py createsuperuser'
NOTE: if you are running in production remember to run './manage.py collectstatic'
EOF
