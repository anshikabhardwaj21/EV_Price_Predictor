# EV_Price_Predictor
# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
# For linux/MAC
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
