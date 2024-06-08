import pickle
from pathlib import Path
import streamlit_authenticator as stauth


names = ['Okore', 'Albert']
usernames = ['admin', 'Albert']
passwords = ['Auth_string', 'Albert']

hashed_passwords = stauth.utilities.hasher.Hasher(passwords).generate()

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('wb') as file:
    pickle.dump(hashed_passwords, file)