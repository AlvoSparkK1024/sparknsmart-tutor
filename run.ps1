# Check for dependencies
Write-Host "Checking dependencies..."
pip install -r requirements.txt

# Run the application
Write-Host "Starting SPARKnSMART Energy Tutor..."
python -m streamlit run src/ui/app.py
