from dashscope import Generation
import os

# 设置 API Key
# os.environ["DASHSCOPE_API_KEY"] = "sk-ba8e6bbaf3b64ff0839332fc37b88dc8"

prompt = "下面是一个文件的检测结果，请你解释一下含义：完整性分析98%，文件结构完整，无损坏痕迹；元数据分析95%，元数据一致性分析；内容一致性92%，内容逻辑自洽性；伪造痕迹检测12%，异常痕迹检测；图像分析细节：人脸特征点68个特征点匹配，光照一致性良好，边缘检测自然过渡，噪声分析符合自然图像分布。文件基本信息：文件格式JPG，文件大小1.56MB，分辨率/时长3024x4032，创建时间2026-03-01 14:23:45。真伪检测结果：AI生成检测未发现，篡改痕迹未发现，元数据一致性通过，内容逻辑自洽。深度伪造检测：未检测到明显的AI生成痕迹，人脸特征点分布自然，准确度非常准确。元数据分析：EXIF信息完整，拍摄设备与声称一致，准确度非常准确。噪声特征分析：图像噪声分布符合自然照片特征，准确度很准确。一致性校验：人脸与背景光照方向一致，阴影合理，准确度非常准确。"

response = Generation.call(
    model="qwen-plus",
    prompt=prompt,
    api_key='sk-ba8e6bbaf3b64ff0839332fc37b88dc8'
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