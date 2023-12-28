import pandas as pd
import torch
import joblib
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset

# 加载保存的模型和分词器
model_path = r'./results/checkpoint-55000'
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(r"../bert")

# 加载LabelEncoder
label_encoder_path = "label_encoder.pkl"  # 指定之前保存LabelEncoder的路径
label_encoder = joblib.load(label_encoder_path)

# 加载您的数据
df = pd.read_csv(r"C:\Users\12064\Downloads\omr_detail.csv")

# 将OMR记录和值组合成句子
df['sentences'] = df['omr_records'] + ' ' + df['omr_values']

# 使用分词器处理句子
encodings = tokenizer(df['sentences'].tolist(), padding=True, truncation=True, max_length=256, return_tensors='pt')

# 创建数据加载器
test_dataset = TensorDataset(encodings['input_ids'], encodings['attention_mask'])
test_loader = DataLoader(test_dataset, batch_size=2)


# 测试模型
model.eval()
with torch.no_grad():
    for i, batch in enumerate(test_loader):
        inputs, masks = batch
        outputs = model(inputs, attention_mask=masks)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)
        decoded_predictions = label_encoder.inverse_transform(predictions.numpy())

        # 打印输入数据和对应的预测结果
        print(f"Batch {i+1}:")
        for j in range(inputs.size(0)):
            sentence = tokenizer.decode(inputs[j], skip_special_tokens=True)
            print(f"Input Sentence {j+1}: {sentence}")
            print(f"Predicted Label {j+1}: {decoded_predictions[j]}")
        print("\n")