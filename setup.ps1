Write-Host "Starting local setup..."
python -m venv backend\.venv
& backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
Write-Host "Backend dependencies installed."
Write-Host "Next: start backend, frontend, and sensor simulator in separate terminals."
