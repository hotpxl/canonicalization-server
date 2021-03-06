#!/bin/bash
set -euo pipefail

file_path="$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")"
pushd "${file_path}" > /dev/null

python -m nltk.downloader -d nltk_data wordnet wordnet_ic stopwords punkt averaged_perceptron_tagger
