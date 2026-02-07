# Create and activate virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Upgrade pip and install requirements
python3.9 -m pip install --upgrade pip
python3.9 -m pip install -r requirements.txt

# Run Django commands
python3.9 manage.py migrate
python3.9 manage.py collectstatic --noinput
