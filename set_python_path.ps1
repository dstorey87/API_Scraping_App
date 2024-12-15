$PythonPath = "C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe"
$VenvPath = ".\venv"

# Check Python installation
if (Test-Path $PythonPath) {
    Write-Host "Python found at: $PythonPath"
} else {
    Write-Error "Python not found at: $PythonPath"
    exit 1
}

# Remove existing venv
if (Test-Path $VenvPath) {
    Remove-Item -Recurse -Force $VenvPath
    Write-Host "Removed existing virtual environment"
}

# Create new venv
& $PythonPath -m venv $VenvPath
Write-Host "Created new virtual environment"

# Activate and install dependencies
& "$VenvPath\Scripts\activate.ps1"
python -m pip install --upgrade pip
pip install pytest torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118

Write-Host "Environment setup complete"