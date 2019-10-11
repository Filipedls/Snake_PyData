# Palacing Apples in Snake


### Game From
Alexander (Arekkusu304) - http://www.pygame.org/project/3314


### Packeges
pip install jupyter
pip install pipenv


### Create a virtual environment

##### With pipenv
pipenv install
pipenv shell

#### Without pipenv
virtualenv -p python3.6 venv/
source venv/bin/activate
pip install -r requirements.txt


### Setting a jupyter kernel from the virtual env
ipython kernel install --user --name=snake_pydata


### Starting the game
python start_snake.py


### Exiting the virtual environment
deactivate