# ===================== 环境与依赖配置（一键导入，功能明确） =====================
import pandas as pd
import torch
import warnings
import numpy as np
import os
from torch.utils.data import DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    get_linear_schedule_with_warmup
)
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)
from torch.utils.data import Dataset
from tqdm import tqdm   # 现在由你掌控

# 基础设置
warnings.filterwarnings('ignore')
torch.manual_seed(42)

# ===================== 核心配置（集中管理，修改方便） =====================
PATH_CONFIG = {
    "bin_train": "data/train_bin.csv",
    "bin_val": "data/val_bin.csv",
    "aux_train": "data/train_aux.csv",
    "aux_val": "data/val_aux.csv",
    "bin_model_save": "./scam_bin_model",
    "aux_model_save": "./scam_aux_model"
}

MODEL_CONFIG = {
    "model_name": "hfl/chinese-roberta-wwm-ext",
    "max_len": 128,
    "batch_size": 4,
    "epochs": 20,
    "lr": 2e-5,
    "early_stop_patience": 4
}

LABEL_MAP = {
    "bin": {0: "正常文本", 1: "诈骗文本"},
    "aux": {
        1: "冒充公检法诈骗",
        2: "兼职刷单诈骗",
        3: "网络贷款诈骗",
        4: "投资理财诈骗",
        5: "冒充电商客服诈骗",
        6: "中奖抽奖诈骗",
        7: "注销校园贷/征信诈骗",
        8: "虚假求助/情感诈骗",
        9: "低价商品交易诈骗",
        10: "荐股/内幕交易诈骗"
    }
}

# ===================== 数据集封装（标准化，适配PyTorch） =====================
class ScamDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx]).strip()
        label = int(self.labels[idx])
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_attention_mask=True,
            return_token_type_ids=False
        )
        
        return {
            "input_ids": torch.tensor(encoding["input_ids"], dtype=torch.long),
            "attention_mask": torch.tensor(encoding["attention_mask"], dtype=torch.long),
            "labels": torch.tensor(label, dtype=torch.long)
        }

# ===================== 评估指标（分任务定义） =====================
def compute_bin_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=-1)
    
    metrics = {
        "准确率": round(accuracy_score(labels, preds), 4),
        "精准率": round(precision_score(labels, preds, zero_division=0), 4),
        "召回率": round(recall_score(labels, preds, zero_division=0), 4),
        "F1值": round(f1_score(labels, preds, zero_division=0), 4)
    }
    
    try:
        probs = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)
        metrics["AUC值"] = round(roc_auc_score(labels, probs[:, 1]), 4)
    except:
        metrics["AUC值"] = 0.5
    
    return metrics

def compute_aux_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=-1)
    
    return {
        "准确率": round(accuracy_score(labels, preds), 4),
        "精准率": round(precision_score(labels, preds, average="weighted", zero_division=0), 4),
        "召回率": round(recall_score(labels, preds, average="weighted", zero_division=0), 4),
        "F1值": round(f1_score(labels, preds, average="weighted", zero_division=0), 4)
    }

# ===================== 模型训练（手动循环 + tqdm） =====================
def train_model(task_type):
    """
    手动训练循环，使用 tqdm 显示进度
    """
    # 1. 任务参数适配
    if task_type == "bin":
        train_path = PATH_CONFIG["bin_train"]
        val_path = PATH_CONFIG["bin_val"]
        model_save_path = PATH_CONFIG["bin_model_save"]
        num_labels = 2
        compute_metrics = compute_bin_metrics
        task_name = "二分类（正常/诈骗）"
    elif task_type == "aux":
        train_path = PATH_CONFIG["aux_train"]
        val_path = PATH_CONFIG["aux_val"]
        model_save_path = PATH_CONFIG["aux_model_save"]
        num_labels = 10
        compute_metrics = compute_aux_metrics
        task_name = "辅助分类（10类诈骗）"
    else:
        raise ValueError("task_type仅支持bin/aux")

    # 2. 加载数据
    print(f"\n{'='*60}")
    print(f"开始训练 {task_name} 模型 | 加载原始数据集")
    print(f"{'='*60}")
    train_df = pd.read_csv(train_path, encoding="utf-8")
    val_df = pd.read_csv(val_path, encoding="utf-8")
    print(f"✅ 数据加载完成 | 训练集：{len(train_df)}条 | 验证集：{len(val_df)}条")

    # 3. 加载分词器和模型
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CONFIG["model_name"])
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_CONFIG["model_name"],
        num_labels=num_labels,
        ignore_mismatched_sizes=True
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # 4. 构建数据集
    train_texts = train_df["text"].tolist()
    val_texts = val_df["text"].tolist()
    
    if task_type == "bin":
        train_labels = train_df["label"].tolist()
        val_labels = val_df["label"].tolist()
    else:
        train_labels = [l-1 for l in train_df["label"].tolist()]
        val_labels = [l-1 for l in val_df["label"].tolist()]
    
    train_dataset = ScamDataset(train_texts, train_labels, tokenizer, MODEL_CONFIG["max_len"])
    val_dataset = ScamDataset(val_texts, val_labels, tokenizer, MODEL_CONFIG["max_len"])

    # 5. 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=MODEL_CONFIG["batch_size"], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=MODEL_CONFIG["batch_size"], shuffle=False)

    # 6. 优化器和学习率调度器
    optimizer = torch.optim.AdamW(model.parameters(), lr=MODEL_CONFIG["lr"], weight_decay=0.01)
    total_steps = len(train_loader) * MODEL_CONFIG["epochs"]
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(0.1 * total_steps),
        num_training_steps=total_steps
    )

    # 7. 训练准备
    best_f1 = 0.0
    patience_counter = 0
    best_model_state = None

    print(f"\n🚀 开始训练 {task_name} | 共{MODEL_CONFIG['epochs']}轮 | 设备：{device}")
    
    for epoch in range(1, MODEL_CONFIG["epochs"] + 1):
        # ========== 训练阶段 ==========
        model.train()
        total_loss = 0
        # 使用 tqdm 包装训练数据加载器
        pbar = tqdm(train_loader, desc=f"Epoch {epoch}/{MODEL_CONFIG['epochs']} [训练]", leave=False)
        for batch in pbar:
            # 将数据移到设备
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            # 前向传播
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()

            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()

            # 更新 tqdm 后置信息
            pbar.set_postfix({"loss": f"{loss.item():.4f}", "lr": f"{scheduler.get_last_lr()[0]:.2e}"})

        avg_train_loss = total_loss / len(train_loader)

        # ========== 验证阶段 ==========
        model.eval()
        all_logits = []
        all_labels = []
        with torch.no_grad():
            for batch in tqdm(val_loader, desc=f"Epoch {epoch}/{MODEL_CONFIG['epochs']} [验证]", leave=False):
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)

                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits.cpu().numpy()
                all_logits.append(logits)
                all_labels.append(labels.cpu().numpy())

        all_logits = np.concatenate(all_logits, axis=0)
        all_labels = np.concatenate(all_labels, axis=0)

        # 计算验证指标
        metrics = compute_metrics((all_logits, all_labels))
        val_f1 = metrics["F1值"]

        if task_type == "bin":
            print(f"\nEpoch {epoch} | 训练损失: {avg_train_loss:.4f} | "
                f"ACC: {metrics['准确率']:.4f} | Precision: {metrics['精准率']:.4f} | "
                f"Recall: {metrics['召回率']:.4f} | F1: {metrics['F1值']:.4f} | AUC: {metrics['AUC值']:.4f}")
        else:  # aux
            print(f"\nEpoch {epoch} | 训练损失: {avg_train_loss:.4f} | "
                f"ACC: {metrics['准确率']:.4f} | Precision: {metrics['精准率']:.4f} | "
                f"Recall: {metrics['召回率']:.4f} | F1: {metrics['F1值']:.4f}")
        # ========== 保存最优模型 ==========
        if val_f1 > best_f1:
            best_f1 = val_f1
            patience_counter = 0
            best_model_state = model.state_dict().copy()  # 深拷贝
            print(f"🔥 发现更优模型，F1={best_f1:.4f}，已保存")
        else:
            patience_counter += 1
            print(f"⏳ F1未提升，早停计数: {patience_counter}/{MODEL_CONFIG['early_stop_patience']}")

        # 早停判断
        if patience_counter >= MODEL_CONFIG["early_stop_patience"]:
            print(f"🛑 早停触发，停止训练")
            break

    # 8. 保存最优模型
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
    os.makedirs(model_save_path, exist_ok=True)
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    print(f"\n✅ {task_name} 最优模型已保存至：{model_save_path} (最佳F1={best_f1:.4f})")
    
    return model, tokenizer

# ===================== 推理函数（串联双模型，结果易读） =====================
def predict_scam(text, temperature=0.4):
    """
    推理流程：
    1. 二分类判断是否诈骗
    2. 诈骗文本→辅助分类细分类型
    3. 返回带置信度的结构化结果
    """
    # 加载最优模型
    bin_tokenizer = AutoTokenizer.from_pretrained(PATH_CONFIG["bin_model_save"])
    bin_model = AutoModelForSequenceClassification.from_pretrained(PATH_CONFIG["bin_model_save"])
    bin_model.eval()
    
    aux_tokenizer = AutoTokenizer.from_pretrained(PATH_CONFIG["aux_model_save"])
    aux_model = AutoModelForSequenceClassification.from_pretrained(PATH_CONFIG["aux_model_save"])
    aux_model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    bin_model.to(device)
    aux_model.to(device)

    # 第一步：二分类推理
    with torch.no_grad():
        bin_encoding = bin_tokenizer(
            text, truncation=True, padding="max_length", max_length=MODEL_CONFIG["max_len"], return_tensors="pt"
        )
        bin_encoding = {k: v.to(device) for k, v in bin_encoding.items()}
        bin_logits = bin_model(**bin_encoding).logits / temperature
        bin_pred = torch.argmax(bin_logits, dim=1).item()
        bin_prob = round(torch.softmax(bin_logits, dim=1)[0][bin_pred].item(), 4)
        bin_result = LABEL_MAP["bin"][bin_pred]

    # 第二步：辅助分类推理（仅诈骗文本）
    if bin_pred == 1:
        with torch.no_grad():
            aux_encoding = aux_tokenizer(
                text, truncation=True, padding="max_length", max_length=MODEL_CONFIG["max_len"], return_tensors="pt"
            )
            aux_encoding = {k: v.to(device) for k, v in aux_encoding.items()}
            aux_logits = aux_model(**aux_encoding).logits / temperature
            aux_pred = torch.argmax(aux_logits, dim=1).item() + 1  # 标签偏移回1~10
            aux_prob = round(torch.softmax(aux_logits, dim=1)[0][aux_pred-1].item(), 4)
            aux_result = LABEL_MAP["aux"][aux_pred]
        return {
            "输入文本": text,
            "是否诈骗": bin_result,
            "二分类置信度": bin_prob,
            "诈骗细分类型": aux_result,
            "细分类型置信度": aux_prob
        }
    else:
        return {
            "输入文本": text,
            "是否诈骗": bin_result,
            "二分类置信度": bin_prob,
            "诈骗细分类型": "无",
            "细分类型置信度": 0.0
        }

# ===================== 主函数（训练+测试，流程清晰） =====================
if __name__ == "__main__":
    # 1. 训练双模型
    train_model("bin")
    train_model("aux")

    # 2. 测试推理
    print(f"\n{'='*60}")
    print("测试推理效果（基于最优模型）")
    print(f"{'='*60}")
    test_texts = [
        "您好，我是公安局的，你银行卡涉嫌洗钱，需转入安全账户",
        "亲，刷单返利，一单赚50，加QQ进群",
        "今晚加班，不回家吃饭了",
        "内幕股票，三天涨停，快买",
        "宝宝情人节快乐",
        "只要在拉取十个用户，就能返利"
    ]
    
    for text in test_texts:
        result = predict_scam(text)
        print(f"\n📝 {result}")