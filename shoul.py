# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

# ===================== 环境配置 =====================
# 中文字体设置（适配 Ubuntu/Windows 环境，若 Ubuntu 下依然乱码，可改为 'DejaVu Sans'）
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ===================== 数据模拟区 =====================
# 模拟训练轮次（20轮）
epochs = np.arange(1, 21)

# 使用对数增长函数模拟真实的收敛过程 (1 - e^-x)
# 通过调整系数，使最终第20轮的数据精准对齐你的要求
def generate_convergence_data(target, start_val, epochs, noise_level=0.005):
    # 基础收敛曲线
    data = target - (target - start_val) * np.exp(-0.25 * (epochs - 1))
    # 叠加微小随机噪声，增加真实感
    np.random.seed(42) # 固定随机种子，保证每次运行结果一致
    noise = np.random.normal(0, noise_level, len(epochs))
    # 确保最后几轮非常平稳并接近目标值
    data = np.where(epochs > 15, target - (target - data) * 0.5, data)
    return np.clip(data + noise, 0, target)

# 根据你的要求设置目标值
# Text -> 1.0, Image -> 0.98, Video -> 0.95, Audio -> 0.90
text =  generate_convergence_data(1.00, 0.70, epochs)
image = generate_convergence_data(0.98, 0.68, epochs)
video = generate_convergence_data(0.95, 0.72, epochs) # 视频起始略高，符合 MRDF 预训练优势
audio = generate_convergence_data(0.90, 0.65, epochs)

# ===================== 绘图区 =====================
plt.figure(figsize=(10, 6), dpi=300)

# 绘制收敛曲线
plt.plot(epochs, text,  label='Text ',  color='#1E40AF', linewidth=2.5, marker='o', markersize=6, markevery=2)
plt.plot(epochs, image, label='Image ', color='#10B981', linewidth=2.5, marker='s', markersize=6, markevery=2)
plt.plot(epochs, video, label='Video ', color='#EF4444', linewidth=2.5, marker='D', markersize=6, markevery=2)
plt.plot(epochs, audio, label='Audio ', color='#F59E0B', linewidth=2.5, marker='^', markersize=6, markevery=2)

# 图形美化
plt.xlabel('Epochs（训练轮次）', fontsize=12, fontweight='bold')
plt.ylabel('F1-score', fontsize=12, fontweight='bold')
plt.title('多模态防诈模型训练收敛曲线对比', fontsize=15, pad=20, fontweight='bold')

# 设置坐标轴范围
plt.ylim(0.6, 1.05)
plt.xticks(np.arange(0, 21, 2))

# 细节装饰
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True, shadow=True, fontsize=10)
plt.axhline(y=1.0, color='gray', linestyle=':', alpha=0.3) # 1.0 参考线

plt.tight_layout()

# 保存图像
plt.savefig('train_convergence_curve.png', dpi=300)
print("✅ 收敛曲线图已生成：train_convergence_curve.png")
plt.show()