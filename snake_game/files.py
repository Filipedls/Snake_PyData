import signal, os, sys
import pickle
from .config import model_file_name, file_name


file = open(file_name, 'a+')

# Add header if the file is empty
if os.stat(file_name).st_size == 0:
    file.write("status|time_secs|score|moves_to_apple|apple_pos|snake_pos|snake_dir|other\n")

def close_file(signal = None, frame = None):
    file.flush()
    file.close()
    sys.exit()

# Making sure the files get closed when the game closes
signal.signal(signal.SIGINT, close_file)


# Model's pickle
with open(model_file_name, 'rb') as f:
    regr = pickle.load(f)
