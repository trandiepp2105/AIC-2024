import os

def wfile(root, endswith='.mp4'):
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(endswith):
                paths.append(os.path.join(dirpath, filename))
    sorted(paths)
    return paths