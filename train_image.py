import easyocr
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

# 创建 reader 对象，指定需要识别的语言（中文简体 + 英文）
reader = easyocr.Reader(['ch_sim', 'en'])

# 读取图片文件
result = reader.readtext('test.png')

# 提取所有文字，直接拼接（不加换行，也不加空格）
extracted_text = ''
for detection in result:
    text = detection[1]          # 识别出的文字
    extracted_text += text       # 直接拼在后面

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

if __name__=='__main__':
    result=predict_scam(extracted_text)
    print(result)    