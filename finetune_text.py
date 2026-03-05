import pandas as pd
import torch
import warnings
import numpy as np
warnings.filterwarnings('ignore')  

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
    EarlyStoppingCallback  
)
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
)
from torch.utils.data import Dataset
import os

label2type = {
    0: "normal",
    1: "fake_public_security",
    2: "fake_part_time",
    3: "fake_loan",
    4: "fake_investment",
    5: "fake_after_sale",
    6: "fake_lottery",
    7: "fake_credit",
    8: "fake_beg",
    9: "fake_trade",
    10: "fake_stock"
}

type2cn = {
    "normal": "正常文本",
    "fake_public_security": "冒充公检法诈骗",
    "fake_part_time": "兼职刷单诈骗",
    "fake_loan": "网络贷款诈骗",
    "fake_investment": "投资理财诈骗",
    "fake_after_sale": "冒充电商客服诈骗",
    "fake_lottery": "中奖抽奖诈骗",
    "fake_credit": "注销校园贷/征信诈骗",
    "fake_beg": "虚假求助/情感诈骗",
    "fake_trade": "低价商品交易诈骗",
    "fake_stock": "荐股/内幕交易诈骗"
}
model_name = "bert-base-chinese"  # 基础模型
max_len = 128  
batch_size = 8  
epochs = 8  # 训练轮数
learning_rate = 2e-5  # 学习率
output_dir = "./results_multi"  # 训练结果保存目录
model_save_dir = "./scam_multi_model"  # 最终模型保存目录

# -------------------- 1. 数据加载（保留type列，仅text+label参与训练） --------------------
def load_data(file_path):
    """读取数据，清洗并验证格式"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件不存在：{file_path}")
    
    df = pd.read_csv(file_path, encoding="utf-8")
    
    # 必要列检查
    required_cols = ["text", "label", "type"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"数据文件缺少必要列：{col}")
    
    # 数据清洗
    df["text"] = df["text"].fillna("").astype(str)
    df["label"] = df["label"].fillna(0).astype(int)
    df["type"] = df["type"].fillna("normal").astype(str)
    
    # 过滤无效标签（仅保留0-10）
    df = df[df["label"].isin(range(11))]
    
    # 打印数据基本信息
    print(f"\n【{os.path.basename(file_path)}】数据信息：")
    print(f"总样本数：{len(df)}")
    print("类别分布：")
    type_dist = df.groupby(["label", "type"]).size().reset_index(name="样本数")
    type_dist["中文类型"] = type_dist["type"].map(type2cn)
    print(type_dist[["label", "中文类型", "样本数"]])
    
    return df

# 创建data目录（如果不存在）
os.makedirs("data", exist_ok=True)

# 加载训练集和验证集
train_df = load_data("data/train.csv")
val_df = load_data("data/val.csv")

class ScamMultiDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = int(self.labels[idx])
        
        # 文本分词（BERT标准流程）
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_attention_mask=True,
            return_token_type_ids=False,  
        )
        
        return {
            "input_ids": torch.tensor(encoding["input_ids"], dtype=torch.long),
            "attention_mask": torch.tensor(encoding["attention_mask"], dtype=torch.long),
            "labels": torch.tensor(label, dtype=torch.long)
        }

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 构建数据集
train_dataset = ScamMultiDataset(
    texts=train_df["text"].tolist(),
    labels=train_df["label"].tolist(),
    tokenizer=tokenizer,
    max_len=max_len
)
val_dataset = ScamMultiDataset(
    texts=val_df["text"].tolist(),
    labels=val_df["label"].tolist(),
    tokenizer=tokenizer,
    max_len=max_len
)

# -------------------- 3. 多分类评估指标定义 --------------------
def compute_metrics(eval_pred):
    """计算多分类核心指标"""
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)
    
    # 1. 整体指标
    acc = accuracy_score(labels, predictions)
    precision = precision_score(labels, predictions, average="weighted", zero_division=0)
    recall = recall_score(labels, predictions, average="weighted", zero_division=0)
    f1 = f1_score(labels, predictions, average="weighted", zero_division=0)
    
    # 2. 多分类AUC（One-vs-Rest）
    try:
        probs = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)
        auc = roc_auc_score(labels, probs, multi_class="ovr", average="weighted")
    except Exception as e:
        print(f"计算AUC失败：{e}")
        auc = 0.5
    
    # 3. 每类F1（用于分析）
    per_class_f1 = f1_score(labels, predictions, average=None, zero_division=0)
    
    return {
        "accuracy": round(acc, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "auc": round(auc, 4),
        "per_class_f1": [round(f, 4) for f in per_class_f1.tolist()]
    }

def analyze_model_by_type(val_df, model, tokenizer):
    """按类型分析每类的识别效果（包含正常文本的完整指标）"""
    print("\n" + "="*60)
    print("【按类型分析模型效果】")
    print("="*60)
    
    # 对验证集所有样本预测
    all_preds = []
    all_labels = []
    all_types = []
    
    model.eval()
    with torch.no_grad():
        for idx, row in val_df.iterrows():
            text = str(row["text"])
            label = int(row["label"])
            type_name = row["type"]
            
            # 推理
            encoding = tokenizer(
                text,
                truncation=True,
                padding="max_length",
                max_length=max_len,
                return_tensors="pt"
            )
            outputs = model(** encoding)
            pred_label = torch.argmax(outputs.logits, dim=1).item()
            
            all_preds.append(pred_label)
            all_labels.append(label)
            all_types.append(type_name)
    
    # 构建结果数据框
    result_df = pd.DataFrame({
        "type": all_types,
        "true_label": all_labels,
        "pred_label": all_preds
    })
    result_df["true_type_cn"] = result_df["type"].map(type2cn)
    result_df["pred_type_cn"] = result_df["pred_label"].map(label2type).map(type2cn)
    
    # 按类型计算指标（核心修改：正常文本也计算精确率/召回率/F1）
    type_metrics = []
    for type_name in result_df["type"].unique():
        type_data = result_df[result_df["type"] == type_name]
        if len(type_data) == 0:
            continue
        
        # 计算该类型的核心指标
        acc = accuracy_score(type_data["true_label"], type_data["pred_label"])
        # 核心修改：移除仅对诈骗类型计算的判断，所有类型都计算精确率/召回率/F1
        target_label = list(label2type.keys())[list(label2type.values()).index(type_name)]
        precision = precision_score(
            type_data["true_label"], 
            type_data["pred_label"], 
            average="binary", 
            pos_label=target_label,
            zero_division=0
        )
        recall = recall_score(
            type_data["true_label"], 
            type_data["pred_label"], 
            average="binary", 
            pos_label=target_label,
            zero_division=0
        )
        f1 = f1_score(
            type_data["true_label"], 
            type_data["pred_label"], 
            average="binary", 
            pos_label=target_label,
            zero_division=0
        )
        
        type_metrics.append({
            "类型": type2cn[type_name],
            "样本数": len(type_data),
            "准确率": round(acc, 4),
            "精确率": round(precision, 4),
            "召回率": round(recall, 4),
            "F1值": round(f1, 4)
        })
    
    # 打印按类型指标
    metrics_df = pd.DataFrame(type_metrics)
    print("\n各类型识别效果（含正常文本完整指标）：")
    print(metrics_df.to_string(index=False))
    
    # 打印详细分类报告
    print("\n详细分类报告：")
    y_true = result_df["true_label"]
    y_pred = result_df["pred_label"]
    target_names = [type2cn[label2type[i]] for i in range(11)]
    report = classification_report(
        y_true, y_pred, 
        target_names=target_names,
        zero_division=0,
        digits=4
    )
    print(report)
    
    return result_df

# -------------------- 5. 加载模型（多分类：num_labels=11） --------------------
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=11,  # 11分类（0-10）
    ignore_mismatched_sizes=True  # 忽略分类头权重不匹配警告
)

# -------------------- 6. 训练参数配置 --------------------
training_args = TrainingArguments(
    output_dir=output_dir,
    eval_strategy="epoch",  # 每轮验证一次
    save_strategy="epoch",  # 每轮保存一次
    learning_rate=learning_rate,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=epochs,
    weight_decay=0.01,  # 权重衰减防止过拟合
    logging_dir="./logs_multi",
    logging_steps=10,
    load_best_model_at_end=True,  # 训练结束加载最优模型
    metric_for_best_model="f1",  # 按F1选最优模型
    greater_is_better=True,  # F1越大越好
    report_to="none",  # 不使用wandb等平台
    fp16=False,  # 无GPU则关闭混合精度
    disable_tqdm=False,  # 显示训练进度条
    save_total_limit=3,  # 最多保存3个检查点
    # 移除：early_stopping_patience=2（旧版transformers不支持）
)

# 数据整理器（自动padding）
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# -------------------- 构建Trainer --------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
    data_collator=data_collator,
    # 核心修复：通过回调函数实现早停
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)

# -------------------- 7. 开始训练 --------------------
print("\n" + "="*60)
print("开始训练多分类反诈文本模型...")
print("="*60)
trainer.train()

# -------------------- 8. 保存最终模型 --------------------
os.makedirs(model_save_dir, exist_ok=True)
model.save_pretrained(model_save_dir)
tokenizer.save_pretrained(model_save_dir)
print(f"\n✅ 多分类模型已保存至：{model_save_dir}")

# -------------------- 9. 按类型分析验证集效果 --------------------
analyze_model_by_type(val_df, model, tokenizer)

# -------------------- 10. 推理函数（预测具体诈骗类型） --------------------
def predict_scam_type(text, model, tokenizer, max_len=128):
    """
    单文本多分类预测
    返回：(中文类型, 置信度, 数字标签)
    """
    model.eval()
    with torch.no_grad():
        # 分词
        encoding = tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=max_len,
            return_tensors="pt"
        )
        # 预测
        outputs = model(**encoding)
        logits = outputs.logits
        pred_label = torch.argmax(logits, dim=1).item()
        pred_type_en = label2type[pred_label]
        pred_type_cn = type2cn[pred_type_en]
        # 计算置信度
        prob = torch.softmax(logits, dim=1)[0][pred_label].item()
    
    return pred_type_cn, round(prob, 4), pred_label

# -------------------- 11. 测试推理 --------------------
print("\n" + "="*60)
print("【测试推理】")
print("="*60)
test_texts = [
    "您好，我是公安局的，你银行卡涉嫌洗钱，需转入安全账户",
    "亲，刷单返利，一单赚50，加QQ进群",
    "今晚加班，不回家吃饭了",
    "内幕股票，三天涨停，快买"
]

for text in test_texts:
    pred_type, prob, label = predict_scam_type(text, model, tokenizer, max_len)
    print(f"\n文本：{text}")
    print(f"预测类型：{pred_type}")
    print(f"置信度：{prob}")
    print(f"数字标签：{label}")

# -------------------- 12. 批量推理函数（可选） --------------------
def batch_predict(texts, model, tokenizer, max_len=128):
    """批量预测文本类型"""
    results = []
    model.eval()
    with torch.no_grad():
        for text in texts:
            pred_type, prob, label = predict_scam_type(text, model, tokenizer, max_len)
            results.append({
                "text": text,
                "pred_type": pred_type,
                "confidence": prob,
                "label": label
            })
    return pd.DataFrame(results)

print("\n🎉 多分类反诈文本模型训练完成！")
print(f"模型保存路径：{model_save_dir}")
print("后续可直接加载模型进行推理：")
print("```python")
print("from transformers import AutoTokenizer, AutoModelForSequenceClassification")
print(f"tokenizer = AutoTokenizer.from_pretrained('{model_save_dir}')")
print(f"model = AutoModelForSequenceClassification.from_pretrained('{model_save_dir}')")
print("```")