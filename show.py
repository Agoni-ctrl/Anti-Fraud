# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

# ===================== 全局样式配置（贴合参考图简约商务风）=====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Heiti TC', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['xtick.bottom'] = False
plt.rcParams['ytick.left'] = False

# 自定义圆角柱状图绘制函数（保留你习惯的圆角，也可以把radius设为0改成参考图的直角）
def draw_rounded_bar(ax, x, height, width, color, radius=0.03):
    left = x - width / 2
    right = x + width / 2
    bottom = 0
    top = height
    bar = FancyBboxPatch(
        (left, bottom), right - left, top - bottom,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color,
        edgecolor="none",
        linewidth=0
    )
    ax.add_patch(bar)
    return bar

# ===================== 核心配置区 =====================
# 1. 基础分类
modalities = ['文本', '图片', '音频', '视频']       
categories = ['AUC', 'ACC', 'Precision', 'Recall', 'F1-score']  

# 2. 数据矩阵（替换成你的真实数据即可）
data = np.array([
    [92, 90, 88, 94],  # AUC
    [89, 87, 85, 91],  # ACC
    [87, 84, 86, 89],  # Precision
    [88, 85, 87, 90],  # Recall
    [87, 86, 86, 90]   # F1-score
])

# 3. 【核心修改】参考图同款商务配色（低饱和、高级感、区分度拉满，完全不刺眼）
colors = [
    '#3D70C8',  # 主深蓝色（参考图Accuracy同款）
    '#F07F30',  # 暖橙色（参考图Matched同款）
    '#A8A8A8',  # 中性灰（参考图Mismatched同款）
    '#6B90D0',  # 浅蓝（同色系延伸，不突兀）
    '#BEBEBE'   # 浅灰（同色系延伸，协调统一）
]

# 4. 样式配置
fig_size = (16, 7)        
bar_width = 0.18           
round_radius = 0.03        # 想要参考图的直角柱子，把这个值改成0即可
y_max = 100                
y_ticks = [0, 20, 40, 60, 80, 100] 

# ===================== 绘图逻辑（贴合参考图风格优化）=====================
fig, ax = plt.subplots(figsize=fig_size, facecolor='white')
ax.set_facecolor('white')
x = np.arange(len(modalities))  

# 循环绘制柱子+顶部数值标注
for cat_idx in range(len(categories)):
    x_offset = (cat_idx - len(categories)/2 + 0.5) * bar_width
    current_x = x + x_offset
    current_heights = data[cat_idx]
    current_color = colors[cat_idx]
    
    for i in range(len(modalities)):
        h = current_heights[i]
        if h <= 0:
            continue
        # 绘制柱子
        draw_rounded_bar(ax, current_x[i], h, bar_width, current_color, radius=round_radius)
        # 【修改】参考图同款：顶部数值用深黑色，清晰醒目，和柱子颜色分离
        ax.text(
            current_x[i], h + y_max * 0.01,
            f'{int(h)}',
            ha='center', va='bottom',
            fontsize=20, fontweight='medium',
            color='#333333'  # 深黑色，和参考图一致
        )

# 坐标轴配置（贴合参考图风格）
ax.set_ylabel('指标数值 (%)', fontsize=20, loc='top', color='#555555')
ax.set_ylim(0, y_max * 1.05)
ax.set_yticks(y_ticks)
ax.tick_params(axis='y', labelsize=18, colors='#555555')

ax.set_xticks(x)
ax.set_xticklabels(modalities, fontsize=20, color='#333333')
ax.set_xlim(-0.5, len(modalities)-0.5)

# 【修改】参考图同款：横向浅灰色实线网格，放在柱子底层
ax.yaxis.grid(True, linestyle='-', color='#E0E0E0', linewidth=1, zorder=0)
ax.set_axisbelow(True)

# 边框控制（仅保留底部浅灰线，和参考图一致）
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#CCCCCC')
ax.spines['bottom'].set_linewidth(1)

# 底部图例（简洁风格，和参考图对齐）
handles = [plt.matplotlib.patches.Patch(color=colors[i], label=categories[i]) for i in range(len(categories))]
ax.legend(
    handles=handles,
    loc='lower center',
    bbox_to_anchor=(0.5, -0.22),
    ncol=len(categories),
    frameon=False,
    fontsize=19,
    handletextpad=0.5
)

# 【可选】添加参考图同款大标题，取消注释即可使用
# ax.set_title('多模态反诈助手各模态性能指标对比', fontsize=24, color='#555555', pad=25)

# 保存与显示
plt.tight_layout()
plt.savefig('多模态指标性能对比.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('多模态指标性能对比.pdf', bbox_inches='tight', facecolor='white')
plt.show()