<template>
  <div class="parent-child-page">
    <div v-if="!selectedRole" class="role-selection">
      <h2 class="role-selection-title">请选择您的身份</h2>
      <div class="role-cards">
        <div class="role-card parent-card" @click="selectRole('parent')">
          <div class="card-icon">
            <img src="/家长.jpg" alt="家长" class="role-image">
          </div>
          <h3 class="card-title">我是家长</h3>
          <p class="card-description">了解育儿相关骗局，保护家庭财产安全</p>
          <div class="card-features">
            <span class="feature-tag">育儿补贴诈骗</span>
            <span class="feature-tag">防骗指南</span>
          </div>
        </div>
        
        <div class="role-card child-card" @click="selectRole('child')">
          <div class="card-icon">
            <img src="/孩子.jpg" alt="孩子" class="role-image">
          </div>
          <h3 class="card-title">我是孩子</h3>
          <p class="card-description">学习识别针对学生的骗局，保护自己</p>
          <div class="card-features">
            <span class="feature-tag">学生专属骗局</span>
            <span class="feature-tag">游戏诈骗</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="page-layout">
      <aside class="sidebar">
        <div class="sidebar-header">
          <h2 class="sidebar-title">亲子反诈小课堂</h2>
        </div>
        <nav class="sidebar-nav">
          <div class="nav-section">
            <h4 class="nav-section-title">视频学习</h4>
            <ul class="nav-list">
              <li
                v-for="(video, index) in filteredVideos"
                :key="index"
                class="nav-item"
                :class="{ active: currentVideoIndex === index && !showQuiz }"
                @click="selectVideo(index)"
              >
                <span class="nav-icon"><font-awesome-icon icon="video" /></span>
                <span class="nav-text">{{ video.title }}</span>
              </li>
            </ul>
          </div>

          <div class="nav-section">
            <h4 class="nav-section-title">防骗小测试</h4>
            <ul class="nav-list">
              <li
                class="nav-item"
                :class="{ active: showQuiz }"
                @click="startQuiz"
              >
                <span class="nav-icon"><font-awesome-icon icon="bullseye" /></span>
                <span class="nav-text">开始测试</span>
              </li>
            </ul>
          </div>
          
          <div class="nav-section">
            <button class="back-btn" @click="backToSelection">
              <span class="back-icon"><font-awesome-icon icon="arrow-left" /></span>
              <span>返回选择</span>
            </button>
          </div>
        </nav>
      </aside>

      <main class="main-content">
        <div v-if="!showQuiz">
          <div class="content-header">
            <h1 class="page-title">{{ currentVideo.title }}</h1>
          </div>

          <div class="video-section">
            <VideoPlayer :video-url="currentVideo.url" />
          </div>
          
          <div class="knowledge-section">
            <h3 class="knowledge-title">知识点</h3>
            <p class="knowledge-text">{{ currentVideo.knowledge }}</p>
          </div>
          
          <div class="interaction-image">
            <img src="/亲子互动.jpg" alt="亲子互动" class="interaction-img">
          </div>
        </div>

        <div v-else class="quiz-section">
          <QuizComponent :quizzes="filteredQuizzes" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import VideoPlayer from './components/VideoPlayer.vue'
import QuizComponent from './components/QuizComponent.vue'

const selectedRole = ref(null)
const currentVideoIndex = ref(0)
const showQuiz = ref(false)

const videos = [
  {
    title: '锚定学生的专属骗局',
    url: '/videos/parent-child/xuesheng.mp4',
    knowledge: '学生群体是诈骗分子的重点目标。常见骗局包括：兼职刷单诈骗、游戏充值诈骗、冒充好友借钱、虚假中奖诈骗等。学生社会经验不足，容易轻信他人。家长要教育孩子不轻信陌生人的承诺，不向陌生账户转账，遇到可疑情况及时告知家长或老师。',
    role: 'child'
  },
  {
    title: '育儿补贴新型骗局',
    url: '/videos/parent-child/yuer.mp4',
    knowledge: '育儿补贴诈骗是针对家长的新型骗局。骗子冒充政府工作人员，声称可以领取育儿补贴，诱导家长提供银行卡信息或支付手续费。记住：政府补贴会通过官方渠道发放，不会要求提供银行卡密码或支付费用。遇到此类情况，请拨打官方电话核实。',
    role: 'parent'
  },
  {
    title: '免费领取游戏皮肤诈骗',
    url: '/videos/parent-child/youxi.mp4',
    knowledge: '游戏皮肤诈骗主要针对青少年游戏玩家。骗子以"免费领取稀有皮肤"为诱饵，诱导玩家扫码或点击链接，窃取游戏账号或钱财。家长要教育孩子：天下没有免费的午餐，不要轻信"免费领取"的广告，不要扫描不明二维码或点击陌生链接。',
    role: 'child'
  }
]

const quizzes = [
  {
    question: '孩子在放学路上，陌生人说"我是你爸爸的朋友，他让我来接你"，孩子应该？',
    options: ['立即跟陌生人走', '问清楚爸爸的名字', '拒绝并立即告诉老师或家长', '给陌生人打电话确认'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '孩子应该拒绝陌生人的接送要求，立即告诉老师或家长。不要轻信陌生人的话，更不能跟随陌生人离开。',
    role: 'child'
  },
  {
    question: '孩子在网上玩游戏，有人告诉他"充值100元送稀有皮肤"，孩子应该？',
    options: ['立即充值获取皮肤', '先充值试试', '告诉家长并拒绝', '用零花钱偷偷充值'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '遇到游戏充值诱惑要告诉家长，不要轻信陌生人的承诺。正规游戏不会通过私聊渠道进行充值活动。',
    role: 'child'
  },
  {
    question: '收到"育儿补贴"短信，要求点击链接填写银行卡信息领取，你应该？',
    options: ['立即点击领取', '先填写看看', '通过官方渠道核实', '转发给朋友一起领'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '政府补贴会通过官方渠道发放，不会要求点击不明链接或提供银行卡信息。遇到此类情况要核实真伪。',
    role: 'parent'
  },
  {
    question: '孩子收到同学发来的消息"急需用钱，请转账500元"，孩子应该？',
    options: ['立即转账帮助同学', '先打电话确认', '先转一部分试试', '询问其他同学是否知道'],
    correct: 1,
    selected: null,
    answered: false,
    explanation: '收到转账要求要打电话确认，可能是账号被盗或冒充。不要轻信网络消息，涉及金钱要格外谨慎。',
    role: 'child'
  },
  {
    question: '有人邀请孩子参加"免费游戏活动"，还能领取"稀有皮肤"，孩子应该？',
    options: ['立即参加领取皮肤', '先去看看情况', '拒绝并告诉家长', '叫上朋友一起去'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '"免费领取"往往是诈骗的诱饵。不要贪图小便宜，遇到可疑情况要告诉家长，保护自己的财产安全。',
    role: 'child'
  }
]

const filteredVideos = computed(() => {
  if (!selectedRole.value) return []
  return videos.filter(video => video.role === selectedRole.value)
})

const filteredQuizzes = computed(() => {
  if (!selectedRole.value) return []
  return quizzes.filter(quiz => quiz.role === selectedRole.value || !quiz.role)
})

const currentVideo = computed(() => {
  if (filteredVideos.value.length === 0) {
    return { title: '', knowledge: '', url: '' }
  }
  return filteredVideos.value[currentVideoIndex.value]
})

const selectRole = (role) => {
  selectedRole.value = role
  currentVideoIndex.value = 0
  showQuiz.value = false
}

const backToSelection = () => {
  selectedRole.value = null
  currentVideoIndex.value = 0
  showQuiz.value = false
}

const selectVideo = (index) => {
  currentVideoIndex.value = index
  showQuiz.value = false
}

const startQuiz = () => {
  showQuiz.value = true
}
</script>

<style scoped>
.parent-child-page {
  min-height: 100vh;
  background: #f0f9ff;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
}

/* 页面头部 */
.page-header {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  border-bottom: 2px solid #90caf9;
}

.page-main-title {
  font-size: 32px;
  color: #0d47a1;
  margin-bottom: 8px;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  font-size: 16px;
  color: #1976d2;
  margin-bottom: 24px;
  font-weight: 500;
}

.illustration-container {
  max-width: 600px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.illustration {
  width: 100%;
  height: auto;
  display: block;
}

/* 侧边栏头�?*/
.sidebar-header {
  padding: 24px 16px 16px;
  border-bottom: 2px solid #e0f2fe;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
}

.sidebar-title {
  font-size: 20px;
  color: #0d47a1;
  font-weight: 700;
  text-align: center;
  margin: 0;
}

/* 角色选择 */
.role-selection {
  padding: 40px 20px;
  max-width: 1400px;
  margin: 0 auto;
  text-align: center;
}

.role-selection-title {
  font-size: 28px;
  color: #0d47a1;
  margin-bottom: 40px;
  font-weight: 700;
  text-align: center;
}

.role-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 60px;
  margin-top: 20px;
}

.role-card {
  background: #fff;
  border-radius: 30px;
  padding: 60px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 4px solid transparent;
  position: relative;
  overflow: hidden;
  text-align: center;
}

.role-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  transition: all 0.3s ease;
}

.parent-card::before {
  background: linear-gradient(90deg, #4caf50, #81c784);
}

.child-card::before {
  background: linear-gradient(90deg, #2196f3, #64b5f6);
}

.role-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.15);
  border-color: #90caf9;
}

.card-icon {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.role-image {
  width: 120px;
  height: 120px;
  object-fit: contain;
  background: none;
}

.card-title {
  font-size: 24px;
  color: #1a237e;
  margin-bottom: 18px;
  font-weight: 600;
  text-align: center;
}

.card-description {
  color: #666;
  margin-bottom: 30px;
  text-align: center;
  line-height: 1.6;
  font-size: 16px;
}

.card-features {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.feature-tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 8px 16px;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 500;
}

.parent-card .feature-tag {
  background: #e8f5e8;
  color: #2e7d32;
}

/* 互动图片 */
.interaction-image {
  margin: 24px 0;
  text-align: center;
}

.interaction-img {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  background: none;
}

/* 视频部分 */
.video-section {
  margin: 24px 0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

/* 页面布局 */
.page-layout {
  display: flex;
  min-height: 60vh;
}

.sidebar {
  width: 280px;
  background: #fff;
  border-right: 1px solid #e0f2fe;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  box-shadow: 2px 0 8px rgba(0, 100, 178, 0.08);
}

.sidebar-nav {
  padding: 24px 16px;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-section:last-child {
  margin-bottom: 0;
}

.nav-section-title {
  font-size: 16px;
  color: #0064b2;
  font-weight: 600;
  margin-bottom: 16px;
  padding-left: 8px;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 8px;
  color: #5a7a8a;
  font-size: 16px;
  background: #f8fbfe;
  border: 1px solid #e0f2fe;
}

.nav-item:hover {
  background: #e0f2fe;
  color: #2a5a6a;
  transform: translateX(4px);
}

.nav-item.active {
  background: linear-gradient(135deg, #64b5f6, #2196f3);
  color: #fff;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

.nav-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.nav-text {
  flex: 1;
}

/* 返回按钮 */
.back-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border: 2px solid #e0f2fe;
  border-radius: 10px;
  background: #fff;
  color: #0064b2;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: #f8fbfe;
  border-color: #90caf9;
  transform: translateX(-2px);
}

.back-icon {
  font-size: 16px;
}

.main-content {
  flex: 1;
  padding: 32px 40px;
  background: #fff;
}

.content-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 24px;
  color: #0d47a1;
  margin-bottom: 16px;
  font-weight: 700;
}

.knowledge-section {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  border-left: 4px solid #2196f3;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.15);
}

.knowledge-title {
  font-size: 18px;
  color: #1565c0;
  margin-bottom: 12px;
  font-weight: 600;
}

.knowledge-text {
  color: #455a64;
  line-height: 1.6;
  font-size: 16px;
}

.video-section {
  margin-bottom: 24px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(33, 150, 243, 0.15);
  max-width: 80%;
  margin: 0 auto;
}

.quiz-section {
  padding: 0;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .page-header {
    padding: 30px 16px;
  }
  
  .page-main-title {
    font-size: 28px;
  }
  
  .role-selection {
    padding: 30px 16px;
  }
  
  .role-cards {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .page-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
    border-right: none;
    border-bottom: 1px solid #e0f2fe;
  }

  .main-content {
    padding: 24px 20px;
  }

  .page-title {
    font-size: 22px;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 20px 12px;
  }
  
  .page-main-title {
    font-size: 24px;
  }
  
  .role-selection {
    padding: 20px 12px;
  }
  
  .role-card {
    padding: 20px;
  }
  
  .main-content {
    padding: 20px 16px;
  }
  
  .knowledge-section {
    padding: 16px 20px;
  }
}
</style>