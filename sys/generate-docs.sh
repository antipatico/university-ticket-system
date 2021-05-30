#!/usr/bin/env bash
set -e
set -u
cd docs
grip CONTRIBUTE.md --export --title="QATicket Development Guide"
pandoc CONTRIBUTE.html --pdf-engine=xelatex -s -o ../DevelopmentGuide.pdf
grip USAGE.md --export --title="QATicket User Guide"
pandoc USAGE.html -s -o ../UserGuide.pdf
rm USAGE.html CONTRIBUTE.html