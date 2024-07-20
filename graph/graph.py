import pandas as pd
import os
import matplotlib.pyplot as plt

# Đường dẫn tới tệp CSV
csv_file = os.path.join(os.path.dirname(__file__), 'vram_and_time_usage.csv')

# Đọc tệp CSV bằng Pandas
df = pd.read_csv(csv_file)

# Tạo danh sách các mô hình
models = df['Model'].unique()

# Vẽ đồ thị thời gian theo batch size cho từng mô hình
plt.figure(figsize=(14, 7))
for model in models:
    model_data = df[df['Model'] == model]
    plt.plot(model_data['Batch Size'], model_data['Average Time (s)'], marker='o', label=model)

plt.xlabel('Batch Size')
plt.ylabel('Average Time (s)')
plt.title('Average Time vs. Batch Size for Different Models')
plt.legend()
plt.grid(True)
plt.show()

# Vẽ đồ thị VRAM theo batch size cho từng mô hình
plt.figure(figsize=(14, 7))
for model in models:
    model_data = df[df['Model'] == model]
    plt.plot(model_data['Batch Size'], model_data['Average VRAM (MB)'], marker='o', label=model)

plt.xlabel('Batch Size')
plt.ylabel('Average VRAM (MB)')
plt.title('Average VRAM vs. Batch Size for Different Models')
plt.legend()
plt.grid(True)
plt.show()

