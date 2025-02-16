docker compose up db -d

conda env create -f environment.yml

conda activate papers-chat
python3 scripts/app.py
conda deactivate