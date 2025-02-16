eval "$(conda shell.bash hook)"

conda activate papers-chat
echo "Activated conda env"
python3 /app/app.py
