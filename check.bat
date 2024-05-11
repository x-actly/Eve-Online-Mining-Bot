@echo off
pip install --upgrade pip
pip install "ruff<1" "mypy<2" "black<23" "isort<6" pytest
pip install -r requirements.txt
python -m black .
python -m ruff check . --fix
python -m isort --profile black .
python -m pytest .
python -m mypy --strict .