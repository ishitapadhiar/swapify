# Swapify
SDnD Spring 2021

## Setup

**1. Clone the Git Repo:**
```
git clone https://github.com/ishitapadhiar/swapify.git
```

**2. Create the virtual environment:**
```
python -m pip install virtualenv
python -m virtualenv env --python=python3
source env/bin/activate
```

**3. Download Necessary Files:**
```
sudo pip3 install spotipy
```

**4. Run the app:**
```
flask run
Navigate to localhost:5000/
```

**5. To quit:**
```
ctrl-C (quit the app)
deactivate (quit the virtual environment)
```

**6. Troubleshooting:**
- If you are getting a  ModuleNotFoundError: No module named ‘___’, do a sudo pip3 install ___ , where the blank is the missing module
- If you are getting a flask app error, try setting the environment variable



