import pickle
import os
from tqdm import tqdm

def wfile(folder, ext = '.pkl'):
    files = []
    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(ext):
                files.append(os.path.join(root, filename))
    return files

def get_n(folder):
    files = wfile(folder, '.pkl')
    n = 0
    for file in tqdm(files):
        with open(file, 'rb') as f:
            data = pickle.load(f)
            # print([k[0] if type(k[0]) == str else type(k[0]) for k in data])
            n += len(data[0])
    return n

if __name__ == '__main__':
    folder = r"C:\Users\hokha\OneDrive\Desktop\results\database"
    print(f'Folder: {folder} has {get_n(folder)} embeddings')
    folder_nextframe = r"C:\Users\hokha\OneDrive\Desktop\results\database_nextframe"
    print(f'Folder: {folder_nextframe} has {get_n(folder_nextframe)} embeddings')
