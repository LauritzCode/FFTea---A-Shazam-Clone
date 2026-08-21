import sys
import os


src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, src_dir)

from add_song import import_folder
from database import list_titles

folder_to_add = os.path.join(src_dir, "..", "music", "odyssey_soundtrack")

import_folder(folder_to_add)

print(list_titles())
