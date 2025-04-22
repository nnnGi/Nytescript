#!/bin/zsh
source ~/.zshrc
echo "Ensure this is run at repository path"
cd .
pip install poetry
poetry self add poetry-plugin-shell
poetry shell
poetry install
pip install --editable .