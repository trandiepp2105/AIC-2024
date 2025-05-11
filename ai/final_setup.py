from scripts.create_database_data import *


if __name__ == '__main__':
    root = r'C:\Users\hokha\OneDrive\Desktop\storage'
    database_folder = os.path.join(root, 'database')
    database__nextframe_folder = os.path.join(root, 'database_nextframe')
    description_folder = os.path.join(root, 'de_embeddings')
    embeddings_folder = os.path.join(root, 'embeddings')
    objects_folder = os.path.join(root, 'objects')
    ocr_embeddings_folder = os.path.join(root, 'ocr_embeddings')
    csv_folder = os.path.join(root, 'csv')
    caption_folder = os.path.join(root, 'captions')
    num_processes = 6
    max_frames = 5
    create_database_data(csv_folder, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, database_folder, caption_folder, num_processes=num_processes)
    create_database_data_nextframe(csv_folder, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, database__nextframe_folder, caption_folder, max_frames=max_frames, num_processes=num_processes)