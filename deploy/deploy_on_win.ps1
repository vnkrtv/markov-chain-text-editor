python -m venv venv
Write-Host "Created virtual environment..."
.\venv\Scripts\activate

Write-Host "Start loading requirements..."
pip install --no-cache-dir -r requirements.txt
Write-Host "Successfully loaded requirements..."

$env:FLASK_APP=wsgi.py
flask db init
flask db migrate
flask db upgrade
Write-Host "Applied database migrations..."

Write-Host "Run app with: gunicorn wsgi:app -b 0.0.0.0:5000"
