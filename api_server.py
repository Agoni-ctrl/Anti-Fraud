from flask import Flask, request, jsonify
from flask_cors import CORS
from dashscope import Generation
import os

app = Flask(__name__)
CORS(app)  # 允许Vue前端跨域访问

# 从环境变量读取API Key（安全！）
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")

if not DASHSCOPE_API_KEY:
    print("⚠️ 警告: 未设置 DASHSCOPE_API_KEY 环境变量")
    print("请先运行: set DASHSCOPE_API_KEY=你的新Key")

# 反诈助手的系统提示词
SYSTEM_PROMPT = """你是一个专业的AI反诈助手，专门帮助用户识别诈骗行为、分析可疑信息、提供防骗建议。

你的职责包括：
1. 识别各类诈骗手段（冒充公检法、刷单诈骗、杀猪盘、AI换脸等）
2. 分析用户遇到的可疑情况
3. 提供具体的防范建议和应对措施
4. 引导用户拨打96110反诈专线

回答要求：
- 简洁明了，重点突出
- 如果检测到高风险情况，请明确提醒用户
- 提供具体的行动建议
- 保持专业、友善的语气"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        history = data.get('history', [])
        
        # 构建消息列表
        messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        
        # 添加最近10条历史消息（让AI记住上下文）
        for msg in history[-10:]:
            if msg.get('content'):
                messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        # 调用通义千问API
        response = Generation.call(
            model="qwen-plus",
            messages=messages,
            api_key=DASHSCOPE_API_KEY,
            result_format='message',
            temperature=0.7,
            max_tokens=2000
        )
        
        # 检查API调用是否成功
        if response.status_code == 200:
            ai_reply = response.output.choices[0].message.content
            
            # 检测用户消息的风险等级
            risk_level = detect_risk_level(user_message)
            
            return jsonify({
                'success': True,
                'reply': ai_reply,
                'riskLevel': risk_level
            })
        else:
            return jsonify({
                'success': False,
                'error': f'API错误: {response.status_code}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def detect_risk_level(message):
    """检测消息的风险等级"""
    high_keywords = ['转账', '汇款', '验证码', '安全账户', '共享屏幕', '保证金']
    medium_keywords = ['链接', '刷单', '兼职', '投资', '贷款', '中奖']
    
    for kw in high_keywords:
        if kw in message:
            return 'high'
    for kw in medium_keywords:
        if kw in message:
            return 'medium'
    return None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)