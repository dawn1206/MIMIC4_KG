import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
import joblib

class BertClassifier:
    def __init__(self, model_path, tokenizer_path, label_encoder_path):
        # 在初始化时加载模型、分词器和LabelEncoder
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        self.label_encoder = joblib.load(label_encoder_path)

        # 将模型设置为评估模式
        self.model.eval()

    def predict(self, data):

        # 使用分词器处理句子
        encodings = self.tokenizer(data, padding=True, truncation=True, max_length=256, return_tensors='pt')

        # 创建数据加载器
        test_dataset = TensorDataset(encodings['input_ids'], encodings['attention_mask'])
        test_loader = DataLoader(test_dataset, batch_size=1)

        # 进行预测
        predictions = []
        with torch.no_grad():
            for batch in test_loader:
                inputs, masks = batch
                outputs = self.model(inputs, attention_mask=masks)
                logits = outputs.logits
                batch_predictions = torch.argmax(logits, dim=-1)
                decoded_batch_predictions = self.label_encoder.inverse_transform(batch_predictions.numpy())
                predictions.extend(decoded_batch_predictions)

        return predictions

# 使用方法
# classifier = BertClassifier(model_path, tokenizer_path, label_encoder_path)
# predictions = classifier.predict(data)
