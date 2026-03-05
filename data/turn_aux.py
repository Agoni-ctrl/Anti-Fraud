import pandas as pd
"""
把 所有label为0的去掉 其余的不变 
"""
# 读取数据
df = pd.read_csv("train.csv")

# 确保 label 是整数（防止字符串类型出问题）
df["label"] = pd.to_numeric(df["label"], errors="coerce").fillna(0).astype(int)

# 过滤掉 label == 0
df_filtered = df[df["label"] != 0]

# 保存新文件
df_filtered.to_csv("train_no_label0.csv", index=False, encoding="utf-8")

print("过滤完成，已删除所有 label=0 的数据")
print("剩余数据条数：", len(df_filtered))