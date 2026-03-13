from dashscope import Generation
import os

# 设置 API Key
# os.environ["DASHSCOPE_API_KEY"] = "sk-d697c74cf5b94ada91f7cc70384f14b2"

prompt = "机械学习解释一下啥意思？"

response = Generation.call(
    model="qwen-plus",
    prompt=prompt,
    api_key='sk-d697c74cf5b94ada91f7cc70384f14b2'
)

print(response.output.text)

# def generate_explanation_text(label,confidence,text):
#     prompt = f"""
#     你是一名反诈分析专家。
#     现在有一段文本推理结果如下：
#     - 诈骗类型：{label}
#     - 置信度：{confidence:.2f}
#     - 文本内容：{text}

#     请生成一段简短、自然的中文说明，包含以下三点：
#     1. 模型为什么认为这是这种诈骗；
#     2. 指出文本中具有特征性的风险点；
#     3. 给出一条防骗建议。
#     """

#     response = Generation.call(
#         model="qwen-plus",   # 如果需要更强模型可改 qwen-max 或 qwen-turbo
#         prompt=prompt,
#         temperature=0.6,
#         max_tokens=200,
#         api_key='sk-d697c74cf5b94ada91f7cc70384f14b2'
#     )

#     print(response.output.text)

# generate_explanation_text("伪造",99,"您好，我是招联金融的工作人员。请问您需要贷款吗？我们提供快速、便捷的线上贷款服务。首先，我们需要您添加我们的业务员微信号进行办理。他会询问您的相关信息并给您发送一个APP下载链接")



# def generate_explanation(label, confidence, modality, evidence=None, text=None):
#     """
#     label: 识别出的类型
#     confidence: 置信度
#     modality: 'text'/'audio'/'video'/'image'
#     evidence: 模型的判断依据（list[str]）
#     text: 可选的文本内容（OCR 或 ASR）
#     """
#     if evidence is None:
#         evidence = []

#     # 根据模态自动写 prompt
#     prompt_map = {
#         "text": f"""
#         你是一名反诈分析专家。
#         当前为文本识别任务。
#         类型：{label}，置信度：{confidence:.2f}
#         文本内容：{text}
#         请解释模型的判断依据，指出风险特征并给建议。
#         """,

#         "audio": f"""
#         你是一名反诈分析专家。
#         当前为语音诈骗识别任务。
#         类型：{label}，置信度：{confidence:.2f}
#         模型依据：{"; ".join(evidence)}
#         请解释模型判断的声音特征和潜在风险。
#         """,

#         "video": f"""
#         你是一名反诈分析专家。
#         当前为视频诈骗识别任务。
#         类型：{label}，置信度：{confidence:.2f}
#         模型依据：{"; ".join(evidence)}
#         请解释模型判断依据与视频伪造特征。
#         """,

#         "image": f"""
#         你是一名反诈分析专家。
#         当前为图像诈骗识别任务。
#         类型：{label}，置信度：{confidence:.2f}
#         模型依据：{"; ".join(evidence)}
#         请解释识别依据和视觉诈骗特征。
#         """
#     }

#     prompt = prompt_map.get(modality.lower(), prompt_map["text"])

#     response = Generation.call(
#         model="qwen-plus",
#         prompt=prompt,
#         temperature=0.6,
#         max_tokens=200,
#         api_key='sk-d697c74cf5b94ada91f7cc70384f14b2'
#     )

#     return response.output.text

# print(generate_explanation("网络贷款诈骗", 0.94, modality="text", text="低息贷款秒批，先交押金后放款"))