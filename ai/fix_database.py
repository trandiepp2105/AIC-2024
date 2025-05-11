import numpy as np
import pickle
import os
from multiprocessing import Pool    


def fix_data(pkl_path, out_folder, batch_size=5000):
    print(f'Processing {pkl_path}')
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    # with open(to_path, 'wb') as f:
    #     pickle.dump(data, f)
    for i in range(0, len(data[0]), batch_size):
        with open(os.path.join(out_folder, os.path.basename(pkl_path).replace('.pkl', f'_{i}.pkl')), 'wb') as f:
            pickle.dump([x[i:i + batch_size] for x in data], f)
    print(f'Processed {pkl_path}')

def folder_fix(folder_path, to_folder=None, batch_size=3500):
    list_args = []
    for file in os.listdir(folder_path):
        if file.endswith('.pkl'):
            list_args.append((os.path.join(folder_path, file), to_folder, batch_size))
    with Pool(6) as p:
        p.starmap(fix_data, list_args)

if __name__ == '__main__':
    if not os.path.exists(r"C:\Users\hokha\OneDrive\Desktop\storage\database_fix"):
        os.makedirs(r"C:\Users\hokha\OneDrive\Desktop\storage\database_fix")
    if not os.path.exists(r"C:\Users\hokha\OneDrive\Desktop\storage\database_nextframe_fix"):
        os.makedirs(r"C:\Users\hokha\OneDrive\Desktop\storage\database_nextframe_fix")
    folder_fix(r"C:\Users\hokha\OneDrive\Desktop\storage\database", r"C:\Users\hokha\OneDrive\Desktop\storage\database_fix")
    folder_fix(r"C:\Users\hokha\OneDrive\Desktop\storage\database_nextframe", r"C:\Users\hokha\OneDrive\Desktop\storage\database_nextframe_fix")

