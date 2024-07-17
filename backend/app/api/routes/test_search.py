import sys
import os

# Thêm thư mục gốc và thư mục ai vào sys.path
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
ai_path = os.path.join(base_path, 'ai')
scripts_path = os.path.join(ai_path, 'scripts')

sys.path.append(base_path)
sys.path.append(ai_path)
sys.path.append(scripts_path)

# Import tuyệt đối
from ai.search_index import text_search, image_search
text_search_rel, index = text_search("con cu", 10)

print(index)