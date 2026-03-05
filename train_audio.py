# ===================== 【必须放在最开头！导入transformers之前先设置国内镜像】 =====================
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
# 限制单线程内存碎片，优化Windows内存分配
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
# ==================================================================================================

import torch
import numpy as np
from datasets import Dataset, Audio
from transformers import (
    AutoFeatureExtractor,
    AutoModelForAudioClassification,
    TrainingArguments,
    Trainer,
)
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    roc_auc_score,
)
import gc

# 手动垃圾回收，释放闲置内存
gc.enable()

# ===================== 1. 配置 =====================
model_name = "Zeyadd-Mostaffa/Deepfake-Audio-Detection-v1"

train_audio_dir = "./LA/ASVspoof2019_LA_train/flac"
dev_audio_dir = "./LA/ASVspoof2019_LA_dev/flac"

train_protocol = "./LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
dev_protocol = "./LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.dev.trl.txt"


# ===================== 2. 数据加载 =====================
def load_asv_spoof_data(protocol_path, audio_dir):
    audio_paths = []
    labels = []

    if not os.path.exists(protocol_path):
        raise FileNotFoundError(f"协议文件不存在: {protocol_path}")
    if not os.path.exists(audio_dir):
        raise FileNotFoundError(f"音频目录不存在: {audio_dir}")

    with open(protocol_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue

            file_id = parts[1]
            label_str = parts[-1]

            full_path = os.path.join(audio_dir, f"{file_id}.flac")

            if os.path.exists(full_path):
                audio_paths.append(full_path)
                labels.append(0 if label_str == "bonafide" else 1)

    print(f"\n加载完成: {len(audio_paths)} 条数据")
    print(f"REAL: {labels.count(0)}")
    print(f"FAKE: {labels.count(1)}")

    ds = Dataset.from_dict({"audio": audio_paths, "label": labels})
    ds = ds.cast_column("audio", Audio(sampling_rate=16000))

    return ds


print("加载训练集...")
train_dataset = load_asv_spoof_data(train_protocol, train_audio_dir)
gc.collect()

print("加载验证集...")
dev_dataset = load_asv_spoof_data(dev_protocol, dev_audio_dir)
gc.collect()


# ===================== 3. 预处理（彻底移除attention_mask，无报错） =====================
print("加载音频特征提取器...")
feature_extractor = AutoFeatureExtractor.from_pretrained(
    model_name,
    trust_remote_code=True,
    local_files_only=False
)


def preprocess_function(examples):
    audio_arrays = [x["array"] for x in examples["audio"]]

    # 不再处理attention_mask，只保留核心的input_values
    inputs = feature_extractor(
        audio_arrays,
        sampling_rate=16000,
        max_length=160000,
        truncation=True,
        padding=True
    )

    inputs["labels"] = examples["label"]
    return inputs


print("预处理训练集...")
encoded_train = train_dataset.map(
    preprocess_function,
    batched=True,
    batch_size=2,
    writer_batch_size=50,
    remove_columns=["audio"],
    keep_in_memory=False,
    cache_file_name="./train_cache.arrow",
    num_proc=1
)
# 删除冗余列，避免混淆
encoded_train = encoded_train.remove_columns(["label"])
del train_dataset
gc.collect()

print("预处理验证集...")
encoded_dev = dev_dataset.map(
    preprocess_function,
    batched=True,
    batch_size=2,
    writer_batch_size=50,
    remove_columns=["audio"],
    keep_in_memory=False,
    cache_file_name="./dev_cache.arrow",
    num_proc=1
)
encoded_dev = encoded_dev.remove_columns(["label"])
del dev_dataset
gc.collect()

# 核心修改：只保留数据集里真实存在的列，彻底去掉attention_mask
encoded_train.set_format("torch", columns=["input_values", "labels"])
encoded_dev.set_format("torch", columns=["input_values", "labels"])


# ===================== 4. 加载模型 =====================
print("加载模型...")
model = AutoModelForAudioClassification.from_pretrained(
    model_name,
    num_labels=2,
    ignore_mismatched_sizes=True,
    trust_remote_code=True,
    local_files_only=False
)

model.config.label2id = {"REAL": 0, "FAKE": 1}
model.config.id2label = {0: "REAL", 1: "FAKE"}
gc.collect()


# ===================== 5. 评估指标 =====================
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    probs = torch.softmax(torch.tensor(logits), dim=1).numpy()
    preds = np.argmax(probs, axis=1)

    acc = accuracy_score(labels, preds)
    recall = recall_score(labels, preds)
    precision = precision_score(labels, preds, zero_division=0)
    f1 = f1_score(labels, preds, zero_division=0)

    try:
        auc = roc_auc_score(labels, probs[:, 1])
    except:
        auc = 0.0

    return {
        "accuracy": round(acc, 4),
        "auc": round(auc, 4),
        "recall": round(recall, 4),
        "precision": round(precision, 4),
        "f1": round(f1, 4),
    }


# ===================== 6. 训练参数（内存优化） =====================
training_args = TrainingArguments(
    output_dir="./asv_spoof_results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    warmup_steps=500,
    weight_decay=0.01,
    logging_steps=20,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,
    fp16=torch.cuda.is_available(),
    report_to="none",
    save_total_limit=2,
    dataloader_pin_memory=False,
    dataloader_num_workers=0
)


# ===================== 7. Trainer =====================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_train,
    eval_dataset=encoded_dev,
    tokenizer=feature_extractor,
    compute_metrics=compute_metrics,
)

print("\n开始训练...")
trainer.train()
gc.collect()

print("\n保存模型...")
save_path = "./my_antifraud_audio_model"
os.makedirs(save_path, exist_ok=True)
model.save_pretrained(save_path)
feature_extractor.save_pretrained(save_path)

print("\n最终评估结果:")
results = trainer.evaluate()
print(results)