<template>
  <div class="ai-assistant">
    <!-- 背景装饰 -->
    <div class="bg-decoration"></div>
    
    <!-- 入口页面 - 简洁版 -->
    <transition name="zoom-out">
      <div v-if="!conversationStarted" class="landing-page">
        <!-- 柔和线条装饰 -->
        <div class="line-decoration line-1"></div>
        <div class="line-decoration line-2"></div>
        <div class="line-decoration line-3"></div>
        <div class="line-decoration line-4"></div>
        <div class="circle-decoration circle-1"></div>
        <div class="circle-decoration circle-2"></div>
        
        <div class="landing-content">
          <!-- Logo 靠上 -->
          <div class="logo-wrapper">
            <i class="fa-brands fa-hornbill"></i>
            <span class="logo-text">Anti-Fraud</span>
          </div>
          
          <!-- 标题区 - 扩写版 -->
          <div class="title-section">
            <h1 class="main-title">
              <span class="title-line">AI反诈助手</span>
              <span class="title-line gradient-text">让骗局无处遁形</span>
            </h1>
            <p class="subtitle">
              基于先进大模型技术，实时识别诈骗话术、AI换脸、钓鱼链接
            </p>
            <p class="subtitle-desc">
              守护您的数字财产安全
            </p>
          </div>
          
          <!-- 开始对话按钮 居中 -->
          <div class="cta-section">
            <button class="start-btn" @click="startConversation">
              <span>开始对话</span>
              <i class="fas fa-arrow-right"></i>
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    <!-- 对话界面 -->
    <transition name="zoom-in">
      <div v-if="conversationStarted" class="chat-page">
        <div class="chat-container">
          <!-- 左侧边栏 -->
          <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
            <div class="sidebar-header">
              <button class="collapse-btn" @click="toggleSidebar">
                <i :class="sidebarCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
              </button>
              <button class="new-chat-btn" @click="startNewChat" v-if="!sidebarCollapsed">
                <i class="fas fa-plus"></i>
                <span>新对话</span>
              </button>
            </div>
            
            <div class="history-list" v-if="!sidebarCollapsed">
              <div class="history-section">
                <div class="section-title">今天</div>
                <div 
                  v-for="chat in todayChats" 
                  :key="chat.id"
                  class="history-item"
                  :class="{ active: currentChatId === chat.id }"
                  @click="switchChat(chat.id)"
                >
                  <i class="fas fa-comment"></i>
                  <span class="history-title">{{ chat.title }}</span>
                  <button class="delete-btn" @click.stop="deleteChat(chat.id)">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </div>
              </div>
              
              <div class="history-section" v-if="previousChats.length">
                <div class="section-title">更早</div>
                <div 
                  v-for="chat in previousChats" 
                  :key="chat.id"
                  class="history-item"
                  :class="{ active: currentChatId === chat.id }"
                  @click="switchChat(chat.id)"
                >
                  <i class="fas fa-comment"></i>
                  <span class="history-title">{{ chat.title }}</span>
                  <button class="delete-btn" @click.stop="deleteChat(chat.id)">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </div>
              </div>
              
              <div v-if="chatHistory.length === 0" class="empty-history">
                <i class="fas fa-message"></i>
                <p>暂无对话记录</p>
              </div>
            </div>
            
            <div class="sidebar-footer" v-if="!sidebarCollapsed">
              <!-- 返回首页按钮 -->
              <button class="back-home-btn" @click="backToLanding">
                <i class="fas fa-arrow-left"></i>
                <span>返回首页</span>
              </button>
              <div class="footer-note">
                <i class="fas fa-shield-alt"></i>
                <span>反诈专线: 96110</span>
              </div>
            </div>
          </aside>
          
          <!-- 主对话区域 -->
          <main class="chat-main">
            <div class="messages-container" ref="messagesContainer">
              <div v-if="messages.length === 0" class="welcome-section">
                <div class="welcome-icon">
                  <i class="fa-brands fa-hornbill"></i>
                </div>
                <h2 class="welcome-title">AI反诈助手</h2>
                <p class="welcome-desc">您好，我是您的专属反诈助手，可以帮您识别诈骗套路、分析可疑信息</p>
                
                <div class="quick-questions">
                  <div class="quick-title">常见问题</div>
                  <div class="questions-grid">
                    <div 
                      v-for="question in quickQuestions" 
                      :key="question.id"
                      class="question-card"
                      @click="sendQuickQuestion(question.text)"
                    >
                      <i :class="question.icon"></i>
                      <span>{{ question.text }}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-else class="message-list">
                <div 
                  v-for="(message, index) in messages" 
                  :key="index"
                  class="message-wrapper"
                  :class="message.role"
                >
                  <!-- 右侧：去掉用户头像，只保留AI头像 -->
                  <div class="message-avatar" v-if="message.role === 'assistant'">
                    <i class="fa-brands fa-hornbill"></i>
                  </div>
                  <div class="message-content" :class="{ 'user-message': message.role === 'user' }">
                    <div class="message-bubble" :class="message.role">
                      <div v-html="formatMessage(message.content)" class="message-text"></div>
                      
                      <div v-if="message.riskLevel" class="risk-card" :class="message.riskLevel">
                        <div class="risk-header">
                          <i :class="getRiskIcon(message.riskLevel)"></i>
                          <span class="risk-title">{{ getRiskTitle(message.riskLevel) }}</span>
                        </div>
                        <div class="risk-content">{{ getRiskMessage(message.riskLevel) }}</div>
                        <div class="risk-actions">
                          <button class="risk-btn" @click="callEmergency">
                            <i class="fas fa-phone-alt"></i>拨打96110
                          </button>
                          <button class="risk-btn secondary" @click="reportFraud">
                            <i class="fas fa-flag"></i>举报
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="message-time" :class="{ 'user-time': message.role === 'user' }">{{ formatTime(message.timestamp) }}</div>
                  </div>
                </div>
                
                <div v-if="isTyping" class="message-wrapper assistant">
                  <div class="message-avatar">
                    <i class="fa-brands fa-hornbill"></i>
                  </div>
                  <div class="message-content">
                    <div class="typing-indicator">
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="input-container">
              <div class="input-wrapper">
                <textarea
                  ref="inputTextarea"
                  v-model="inputMessage"
                  @keydown.enter.prevent="sendMessage"
                  @input="autoResize"
                  placeholder="描述您遇到的情况，或直接输入问题..."
                  rows="1"
                  class="message-input"
                ></textarea>
                <button 
                  class="send-btn" 
                  @click="sendMessage"
                  :disabled="!inputMessage.trim() || isTyping"
                >
                  <i class="fas fa-paper-plane"></i>
                </button>
              </div>
              <div class="input-footer">
                <div class="input-tips">
                  <i class="fas fa-shield-alt"></i>
                  <span>本对话内容加密存储，仅用于反诈咨询</span>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'AIAssistant',
  data() {
    return {
      conversationStarted: false,
      sidebarCollapsed: false,
      currentChatId: null,
      chatHistory: [],
      messages: [],
      inputMessage: '',
      isTyping: false,
      
      quickQuestions: [
        { id: 1, text: '如何识别冒充公检法诈骗？', icon: 'fas fa-gavel' },
        { id: 2, text: '收到陌生链接怎么办？', icon: 'fas fa-link' },
        { id: 3, text: '刷单兼职是诈骗吗？', icon: 'fas fa-money-bill-wave' },
        { id: 4, text: 'AI换脸视频通话怎么核实？', icon: 'fas fa-video' },
        { id: 5, text: '对方让我下载会议软件共享屏幕...', icon: 'fas fa-desktop' },
        { id: 6, text: '96110是什么电话？', icon: 'fas fa-phone' }
      ]
    }
  },
  computed: {
    todayChats() {
      return this.chatHistory.filter(chat => {
        const today = new Date().toDateString();
        const chatDate = new Date(chat.timestamp).toDateString();
        return chatDate === today;
      });
    },
    previousChats() {
      return this.chatHistory.filter(chat => {
        const today = new Date().toDateString();
        const chatDate = new Date(chat.timestamp).toDateString();
        return chatDate !== today;
      });
    }
  },
  mounted() {
    this.loadChatHistory();
    if (this.chatHistory.length === 0) {
      this.startNewChat();
    } else {
      this.switchChat(this.chatHistory[0].id);
    }
  },
  methods: {
    startConversation() {
      this.conversationStarted = true;
      setTimeout(() => {
        this.$refs.inputTextarea?.focus();
      }, 500);
    },
    
    backToLanding() {
      this.conversationStarted = false;
    },
    
    loadChatHistory() {
      const saved = localStorage.getItem('anti_fraud_chat_history');
      if (saved) {
        this.chatHistory = JSON.parse(saved);
      }
    },
    
    saveChatHistory() {
      localStorage.setItem('anti_fraud_chat_history', JSON.stringify(this.chatHistory));
    },
    
    saveCurrentChat() {
      if (this.currentChatId && this.messages.length > 0) {
        const index = this.chatHistory.findIndex(chat => chat.id === this.currentChatId);
        if (index !== -1) {
          this.chatHistory[index].messages = [...this.messages];
          this.chatHistory[index].title = this.messages[0]?.content?.substring(0, 30) || '新对话';
          this.chatHistory[index].timestamp = Date.now();
        }
        this.saveChatHistory();
      }
    },
    
    startNewChat() {
      if (this.currentChatId && this.messages.length > 0) {
        this.saveCurrentChat();
      }
      
      const newChat = {
        id: Date.now(),
        title: '新对话',
        messages: [],
        timestamp: Date.now()
      };
      this.chatHistory.unshift(newChat);
      this.currentChatId = newChat.id;
      this.messages = [];
      this.saveChatHistory();
      
      this.$nextTick(() => {
        this.$refs.inputTextarea?.focus();
      });
    },
    
    switchChat(chatId) {
      if (this.currentChatId && this.messages.length > 0) {
        this.saveCurrentChat();
      }
      
      const chat = this.chatHistory.find(c => c.id === chatId);
      if (chat) {
        this.currentChatId = chatId;
        this.messages = chat.messages || [];
        this.scrollToBottom();
      }
    },
    
    deleteChat(chatId) {
      this.chatHistory = this.chatHistory.filter(chat => chat.id !== chatId);
      this.saveChatHistory();
      
      if (this.currentChatId === chatId) {
        if (this.chatHistory.length > 0) {
          this.switchChat(this.chatHistory[0].id);
        } else {
          this.startNewChat();
        }
      }
    },
    
    clearChat() {
      if (confirm('确定要清空当前对话吗？')) {
        this.messages = [];
        this.saveCurrentChat();
      }
    },
    
    sendQuickQuestion(text) {
      this.inputMessage = text;
      this.sendMessage();
    },
    
    async sendMessage() {
      const content = this.inputMessage.trim();
      if (!content || this.isTyping) return;
      
      // 添加用户消息
      const userMessage = {
        role: 'user',
        content: content,
        timestamp: Date.now()
      };
      this.messages.push(userMessage);
      this.inputMessage = '';
      this.autoResize();
      this.scrollToBottom();
      
      this.isTyping = true;
      
      try {
        const response = await fetch('http://localhost:5005/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: content,
            history: this.messages.filter(m => m.role !== 'assistant' || m.content !== '').map(m => ({
              role: m.role,
              content: m.content
            }))
          })
        });
        
        if (!response.ok) {
          throw new Error(`API请求失败: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
          this.isTyping = false;
          
          const aiMessage = {
            role: 'assistant',
            content: '',
            timestamp: Date.now()
          };
          this.messages.push(aiMessage);
          this.scrollToBottom();
          
          const fullText = data.reply;
          let currentText = '';
          const chars = fullText.split('');
          
          for (let i = 0; i < chars.length; i++) {
            currentText += chars[i];
            this.messages[this.messages.length - 1].content = currentText;
            await this.delay(30);
            this.scrollToBottom();
          }
          
          this.messages[this.messages.length - 1].riskLevel = data.riskLevel || this.detectRiskLevel(content);
          this.saveCurrentChat();
        } else {
          throw new Error(data.error || '未知错误');
        }
        
      } catch (error) {
        console.error('API调用失败:', error);
        this.isTyping = false;
        const errorMessage = {
          role: 'assistant',
          content: '抱歉，服务暂时不可用，请稍后再试。如有紧急情况，请直接拨打96110。',
          timestamp: Date.now()
        };
        this.messages.push(errorMessage);
      }
    },
    
    detectRiskLevel(message) {
      const highRiskKeywords = ['转账', '汇款', '验证码', '安全账户', '共享屏幕', '保证金'];
      const mediumRiskKeywords = ['链接', '刷单', '兼职', '投资', '贷款', '中奖'];
      
      for (const keyword of highRiskKeywords) {
        if (message.includes(keyword)) return 'high';
      }
      for (const keyword of mediumRiskKeywords) {
        if (message.includes(keyword)) return 'medium';
      }
      return null;
    },
    
    getRiskIcon(level) {
      const icons = { high: 'fas fa-exclamation-triangle', medium: 'fas fa-exclamation-circle', low: 'fas fa-info-circle' };
      return icons[level] || icons.low;
    },
    
    getRiskTitle(level) {
      const titles = { high: '高风险预警', medium: '中风险提示', low: '温馨提示' };
      return titles[level] || titles.low;
    },
    
    getRiskMessage(level) {
      const messages = {
        high: '检测到您描述的情况存在较高诈骗风险，请立即停止操作，不要转账或提供验证码！',
        medium: '您描述的情况疑似诈骗，请提高警惕，核实对方身份后再做决定。',
        low: '请保持警惕，如有疑问可咨询官方渠道确认。'
      };
      return messages[level] || messages.low;
    },
    
    formatMessage(content) {
      let formatted = content.replace(/\n/g, '<br>');
      formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      return formatted;
    },
    
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    },
    
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    
    autoResize() {
      const textarea = this.$refs.inputTextarea;
      if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
      }
    },
    
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },
    
    callEmergency() {
      window.location.href = 'tel:96110';
    },
    
    reportFraud() {
      window.open('https://www.12321.cn/', '_blank');
    },
    
    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  },
  beforeDestroy() {
    if (this.currentChatId && this.messages.length > 0) {
      this.saveCurrentChat();
    }
  }
};
</script>

<style scoped>
.ai-assistant {
  min-height: calc(100vh - 100px);
  position: relative;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow: hidden;
}

/* ===== 入口页面背景 - 柔和配色 + 线条装饰 ===== */
.landing-page {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, #DFF1FB 0%, #A5D0F2 50%, #FBF8E7 100%);
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 柔和线条装饰 */
.line-decoration {
  position: absolute;
  background: rgba(165, 208, 242, 0.4);
  border-radius: 100%;
}

.line-1 {
  top: 10%;
  left: -5%;
  width: 300px;
  height: 300px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: floatLine 20s ease-in-out infinite;
}

.line-2 {
  bottom: 15%;
  right: -3%;
  width: 400px;
  height: 400px;
  border: 1.5px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: floatLine 25s ease-in-out infinite reverse;
}

.line-3 {
  top: 40%;
  left: 15%;
  width: 150px;
  height: 150px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: floatLine 15s ease-in-out infinite;
}

.line-4 {
  bottom: 30%;
  left: 20%;
  width: 200px;
  height: 200px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  animation: floatLine 18s ease-in-out infinite reverse;
}

/* 圆形光晕装饰 */
.circle-decoration {
  position: absolute;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent);
  border-radius: 50%;
  filter: blur(40px);
}

.circle-1 {
  top: -100px;
  right: -100px;
  width: 400px;
  height: 400px;
  animation: pulse 8s ease-in-out infinite;
}

.circle-2 {
  bottom: -80px;
  left: -80px;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(165, 208, 242, 0.5), transparent);
  animation: pulse 10s ease-in-out infinite reverse;
}

@keyframes floatLine {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  50% {
    transform: translate(30px, 20px) rotate(10deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

.landing-content {
  text-align: center;
  max-width: 700px;
  padding: 2rem;
  position: relative;
  z-index: 2;
  animation: fadeInScale 0.8s ease;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Logo区域 */
.logo-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 60px;
  animation: fadeInDown 0.6s ease;
}

.logo-wrapper i {
  font-size: 52px;
  color: #3182ce;
  filter: drop-shadow(0 4px 8px rgba(49, 130, 206, 0.2));
}

.logo-text {
  font-size: 26px;
  font-weight: 600;
  background: linear-gradient(135deg, #1a4b7a, #3182ce);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* 标题区 - 扩写版 */
.title-section {
  margin-bottom: 60px;
  animation: fadeInUp 0.6s ease 0.1s both;
}

.main-title {
  font-size: 56px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 24px;
}

.title-line {
  display: block;
}

.gradient-text {
  background: linear-gradient(135deg, #2c5282, #4299ff, #63b3ed);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-size: 52px;
  margin-top: 8px;
}

.subtitle {
  font-size: 18px;
  color: #2c5f7b;
  margin-bottom: 12px;
  line-height: 1.5;
  font-weight: 500;
}

.subtitle-desc {
  font-size: 15px;
  color: #4a7c9c;
  margin-bottom: 0;
  letter-spacing: 0.3px;
}

/* CTA区域 - 按钮居中 */
.cta-section {
  animation: fadeInUp 0.6s ease 0.2s both;
}

.start-btn {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 14px 42px;
  background: linear-gradient(135deg, #3182ce, #4299ff);
  border: none;
  border-radius: 48px;
  color: white;
  font-size: 18px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(49, 130, 206, 0.3);
}

.start-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 28px rgba(49, 130, 206, 0.4);
}

.start-btn i {
  font-size: 16px;
  transition: transform 0.3s ease;
}

.start-btn:hover i {
  transform: translateX(5px);
}

/* 动画 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===== 过渡动画 ===== */
.zoom-out-enter-active,
.zoom-out-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.zoom-out-enter-from {
  opacity: 0;
  transform: scale(1.1);
}

.zoom-out-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.zoom-in-enter-active,
.zoom-in-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.zoom-in-enter-from {
  opacity: 0;
  transform: scale(0.95);
}

.zoom-in-leave-to {
  opacity: 0;
  transform: scale(1.05);
}

/* ===== 对话页面样式 ===== */
.chat-page {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, #f5f9ff 0%, #eef3fc 100%);
  z-index: 2;
  overflow: hidden;
}

.chat-container {
  display: flex;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 16px 16px 16px;
  gap: 16px;
}

/* 侧边栏 - 优化颜色为浅蓝透明 */
.sidebar {
  width: 280px;
  background: rgba(165, 208, 242, 0.2);
  backdrop-filter: blur(12px);
  border-radius: 0 0 24px 24px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(66, 153, 225, 0.2);
  border-top: none;
  margin-top: 0;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  padding: 20px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(66, 153, 225, 0.15);
}

.collapse-btn {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  border: none;
  background: rgba(66, 153, 225, 0.15);
  color: #4299ff;
  cursor: pointer;
  transition: all 0.2s;
}

.collapse-btn:hover {
  background: rgba(66, 153, 225, 0.25);
}

/* 新对话按钮 - 浅蓝透明风格 */
.new-chat-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(66, 153, 225, 0.2);
  border: 1px solid rgba(66, 153, 225, 0.3);
  border-radius: 40px;
  color: #3182ce;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.new-chat-btn:hover {
  background: rgba(66, 153, 225, 0.3);
  transform: translateY(-1px);
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.history-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 12px;
  font-weight: 500;
  color: #7c9ac0;
  margin-bottom: 12px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 4px;
}

.history-item:hover {
  background: rgba(66, 153, 225, 0.12);
}

.history-item.active {
  background: rgba(66, 153, 225, 0.2);
  border-left: 3px solid #4299ff;
}

.history-title {
  flex: 1;
  font-size: 14px;
  color: #3a6b8f;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.delete-btn {
  opacity: 0;
  background: none;
  border: none;
  color: #9bb7d4;
  cursor: pointer;
  padding: 4px;
}

.history-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: #e53e3e;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(66, 153, 225, 0.15);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.back-home-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  background: rgba(66, 153, 225, 0.15);
  border: none;
  border-radius: 12px;
  color: #4299ff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.back-home-btn:hover {
  background: rgba(66, 153, 225, 0.25);
  transform: translateY(-1px);
}

.footer-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
  color: #7c9ac0;
}

/* 主对话区域 */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(8px);
  border-radius: 0 0 24px 24px;
  border: 1px solid rgba(66, 153, 225, 0.15);
  border-top: none;
  overflow: hidden;
  margin-top: 0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
}

.welcome-section {
  text-align: center;
  padding: 60px 20px;
  max-width: 600px;
  margin: 0 auto;
}

.welcome-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: linear-gradient(145deg, #4299ff, #3182ce);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(66, 153, 225, 0.25);
}

.welcome-icon i {
  font-size: 40px;
  color: white;
}

.welcome-title {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #1e4a7a, #4299ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 12px;
}

.welcome-desc {
  font-size: 14px;
  color: #7c9ac0;
  margin-bottom: 32px;
}

.quick-title {
  font-size: 13px;
  font-weight: 500;
  color: #6b8cae;
  margin-bottom: 12px;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.question-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: white;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #e2edf7;
  font-size: 13px;
}

.question-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(66, 153, 225, 0.12);
  border-color: #4299ff;
}

.question-card i {
  color: #4299ff;
  font-size: 14px;
}

/* 消息样式 - 去掉用户头像 */
.message-wrapper {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  animation: fadeInUp 0.3s ease;
}

.message-wrapper.user {
  justify-content: flex-end;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(66, 153, 225, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-avatar i {
  font-size: 18px;
  color: #4299ff;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.message-content.user-message {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.message-bubble.assistant {
  background: white;
  border: 1px solid #eef2f8;
}

.message-bubble.user {
  background: rgba(66, 153, 225, 0.15);
  border: 1px solid rgba(66, 153, 225, 0.2);
  color: #2c5f7b;
}

.message-text {
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
}

.message-time {
  font-size: 11px;
  color: #a0b8d0;
  margin-top: 6px;
  margin-left: 8px;
}

.message-time.user-time {
  text-align: right;
  margin-right: 8px;
  margin-left: 0;
}

/* 风险卡片 */
.risk-card {
  margin-top: 12px;
  padding: 10px;
  border-radius: 10px;
  background: #fff5f0;
  border-left: 3px solid #f59e0b;
}

.risk-card.high {
  background: #fff0f0;
  border-left-color: #e53e3e;
}

.risk-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.risk-header i {
  font-size: 14px;
}

.risk-card.high .risk-header i {
  color: #e53e3e;
}

.risk-title {
  font-weight: 600;
  font-size: 12px;
}

.risk-card.high .risk-title {
  color: #e53e3e;
}

.risk-content {
  font-size: 12px;
  color: #4a5568;
  margin-bottom: 8px;
}

.risk-actions {
  display: flex;
  gap: 8px;
}

.risk-btn {
  padding: 4px 10px;
  background: #e53e3e;
  border: none;
  border-radius: 16px;
  color: white;
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.risk-btn.secondary {
  background: #e2e8f0;
  color: #4a5568;
}

/* 打字指示器 - 依次跳动效果 */
.typing-indicator {
  display: flex;
  gap: 6px;
  padding: 12px 16px;
  align-items: center;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #90cdf4;
  animation: typingBounce 1.2s infinite ease-in-out;
  opacity: 0.6;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingBounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* 输入区域优化 - 自动调整高度 */
.input-container {
  padding: 16px 24px 20px;
  border-top: 1px solid rgba(66, 153, 225, 0.1);
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.2s ease;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  background: white;
  border-radius: 24px;
  padding: 8px 12px;
  border: 1px solid #e2edf7;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  transform: translateY(0);
  will-change: auto;
}

.input-wrapper:focus-within {
  border-color: #4299ff;
  box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.1);
  transform: translateY(0);
}

.message-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  padding: 8px 0;
  resize: none;
  font-family: inherit;
  max-height: 200px;
  min-height: 40px;
  background: transparent;
  line-height: 1.5;
  overflow-y: auto;
}

.message-input:focus {
  outline: none;
  box-shadow: none;
}

.send-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #4299ff;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
  align-self: flex-end;
  margin-bottom: 4px;
}

.send-btn:hover:not(:disabled) {
  background: #3182ce;
  transform: scale(1.02);
}

.send-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.send-btn:active {
  transform: scale(0.98);
}

.input-footer {
  margin-top: 10px;
  padding: 0 8px;
}

.input-tips {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #9bb7d4;
}

/* 响应式 */
@media (max-width: 768px) {
  .main-title {
    font-size: 40px;
  }
  
  .gradient-text {
    font-size: 36px;
  }
  
  .subtitle {
    font-size: 16px;
  }
  
  .sidebar {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 10;
    margin: 0;
    border-radius: 0;
  }
  
  .sidebar.collapsed {
    transform: translateX(-100%);
    width: 0;
  }
  
  .chat-container {
    padding: 0 8px 8px 8px;
  }
  
  .messages-container {
    padding: 16px;
  }
  
  .questions-grid {
    grid-template-columns: 1fr;
  }
  
  .message-content {
    max-width: 85%;
  }
}
</style>