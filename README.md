# MoneyLife (provisional name: edit `config.py`)

Educational personal-finance app for Indian users, built with Python and Streamlit.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # run the calculation tests
streamlit run app.py
```

## Put it on GitHub
```bash
git init && git add . && git commit -m "MoneyLife phase 1"
# create an empty repo on github.com, then:
git branch -M main
git remote add origin https://github.com/<you>/moneylife.git
git push -u origin main
```
Deploy: share.streamlit.io -> New app -> pick the repo -> main file `app.py`.

## Status
All 21 modules are implemented as an educational prototype. Data lives in session state only (temporary, per visitor).
Not done on purpose: login, permanent storage (`data/` is ready but unwired), verified tax rules, real notifications,
real marketplace listings. See the About page and settle regulatory questions with qualified Indian counsel before launch.
