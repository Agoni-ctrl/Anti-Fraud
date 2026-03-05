import pandas as pd


"""
 把数据里面非0的标签 变为1 得到 train_bin.csv
"""
# 读取数据
df = pd.read_csv("train_aux.csv")

# 确保 label 是整数
df["label"] = pd.to_numeric(df["label"], errors="coerce").fillna(0).astype(int)

# 仅修改 label：1~10 → 1，0 保持 0
df["label"] = df["label"].apply(lambda x: 1 if 1 <= x <= 10 else 0)

# 保存新文件
df.to_csv("binary_train.csv", index=False, encoding="utf-8")

print("转换完成，type 列未做任何修改")