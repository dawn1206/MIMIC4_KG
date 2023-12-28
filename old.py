
import os
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from gensim.models import Word2Vec

# Load your CSV file
df = pd.read_csv(r"C:\Users\12064\Downloads\omr_detail.csv")

# Combine icd_code and icd_version into a single category label
df['icd'] = df['icd_code'].astype(str) + '_' + df['icd_version'].astype(str)

# Clean and split the omr_records and omr_values strings
df['omr_records'] = df['omr_records'].str.strip('[]').str.split('", "')
df['omr_values'] = df['omr_values'].str.strip('[]').str.split('", "')

# Remove extra quotes from each element in the list
df['omr_records'] = df['omr_records'].apply(lambda x: [item.strip('"') for item in x])
df['omr_values'] = df['omr_values'].apply(lambda x: [item.strip('"') for item in x])
# Combine records and values into sentences
sentences = [record + value for record, value in zip(df['omr_records'], df['omr_values'])]

# Define the Word2Vec model filename
model_filename = './word2vec.model'

# Check if model is already saved
if os.path.exists(model_filename):
    # Load the Word2Vec model
    model = Word2Vec.load(model_filename)
else:
    # Train Word2Vec model
    model = Word2Vec(sentences, vector_size=10, min_count=1, workers=4)
    # Save the model for later use
    model.save(model_filename)

# Generate embeddings for each record-value pair in each sentence
df['embeddings'] = [[model.wv[word] for word in sentence] for sentence in sentences]

# Prepare embeddings data
X_filtered = pd.DataFrame(df['embeddings'].tolist())
# 初始化一个与 df['embeddings'] 相同形状的空列表
X_filtered_list = []

# 遍历 'embeddings' 列中的每个元素
for item in df['embeddings']:
    if item is None:
        # 如果元素是 None，则替换为长度为10的零向量
        X_filtered_list.append(np.zeros(10, dtype=np.float32))
    else:
        # 如果元素不是 None，确保它是一个 ndarray
        X_filtered_list.append(np.array(item, dtype=np.float32))

# 将列表转换为 DataFrame
# 用0填充 NaN（由 None 产生的）
# Convert the list of arrays to a 2D NumPy array


y_filtered = df['icd']
# Encode the labels
le = LabelEncoder()
y_encoded = le.fit_transform(df['icd'])
# # Split data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(
#     X_filtered, y_filtered, test_size=0.1, random_state=42, stratify=y_filtered
# )

# Initialize the XGBoost classifier
xgb_model = XGBClassifier(objective='multi:softprob', eval_metric='mlogloss', use_label_encoder=False,n_estimators=1000)

# Train the model
xgb_model.fit(X_filtered_list, y_encoded)

# Predict on the test set
y_pred = xgb_model.predict(X_filtered_list)

# Calculate the accuracy score
accuracy = accuracy_score(y_encoded, y_pred)
print(f'Accuracy: {accuracy}')
