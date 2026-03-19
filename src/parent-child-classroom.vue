<template>
  <div class="parent-child-page">
    <div class="page-layout">
      <aside class="sidebar">
        <nav class="sidebar-nav">
          <div class="nav-section">
            <h4 class="nav-section-title">视频学习</h4>
            <ul class="nav-list">
              <li
                v-for="(video, index) in videos"
                :key="index"
                class="nav-item"
                :class="{ active: currentVideoIndex === index && !showQuiz }"
                @click="selectVideo(index)"
              >
                <span class="nav-icon">🎬</span>
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
                <span class="nav-icon">🎯</span>
                <span class="nav-text">开始测试</span>
              </li>
            </ul>
          </div>
        </nav>
      </aside>

      <main class="main-content">
        <div v-if="!showQuiz">
          <div class="content-header">
            <h1 class="page-title">{{ currentVideo.title }}</h1>
            <div class="knowledge-section">
              <h3 class="knowledge-title">知识点</h3>
              <p class="knowledge-text">{{ currentVideo.knowledge }}</p>
            </div>
          </div>

          <div class="video-section">
            <VideoPlayer :video-url="currentVideo.url" />
          </div>
        </div>

        <div v-else class="quiz-section">
          <QuizComponent :quizzes="quizzes" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import VideoPlayer from './components/VideoPlayer.vue'
import QuizComponent from './components/QuizComponent.vue'

const currentVideoIndex = ref(0)
const showQuiz = ref(false)

const videos = [
  {
    title: '锚定学生的专属骗局',
    url: '/videos/parent-child/xuesheng.mp4',
    knowledge: '学生群体是诈骗分子的重点目标。常见骗局包括：兼职刷单诈骗、游戏充值诈骗、冒充好友借钱、虚假中奖诈骗等。学生社会经验不足，容易轻信他人。家长要教育孩子不轻信陌生人的承诺，不向陌生账户转账，遇到可疑情况及时告知家长或老师。'
  },
  {
    title: '育儿补贴新型骗局',
    url: '/videos/parent-child/yuer.mp4',
    knowledge: '育儿补贴诈骗是针对家长的新型骗局。骗子冒充政府工作人员，声称可以领取育儿补贴，诱导家长提供银行卡信息或支付"手续费"。记住：政府补贴会通过官方渠道发放，不会要求提供银行卡密码或支付费用。遇到此类情况，请拨打官方电话核实。'
  },
  {
    title: '免费领取游戏皮肤诈骗',
    url: '/videos/parent-child/youxi.mp4',
    knowledge: '游戏皮肤诈骗主要针对青少年游戏玩家。骗子以"免费领取稀有皮肤"为诱饵，诱导玩家扫码或点击链接，窃取游戏账号或钱财。家长要教育孩子：天下没有免费的午餐，不要轻信"免费领取"的广告，不要扫描不明二维码或点击陌生链接。'
  }
]

const quizzes = [
  {
    question: '孩子在放学路上，陌生人说"我是你爸爸的朋友，他让我来接你"，孩子应该？',
    options: ['立即跟陌生人走', '问清楚爸爸的名字', '拒绝并立即告诉老师或家长', '给陌生人打电话确认'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '孩子应该拒绝陌生人的接送要求，立即告诉老师或家长。不要轻信陌生人的话，更不能跟随陌生人离开。'
  },
  {
    question: '孩子在网上玩游戏，有人告诉他"充值100元送稀有皮肤"，孩子应该？',
    options: ['立即充值获取皮肤', '先充值试试', '告诉家长并拒绝', '用零花钱偷偷充值'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '遇到游戏充值诱惑要告诉家长，不要轻信陌生人的承诺。正规游戏不会通过私聊渠道进行充值活动。'
  },
  {
    question: '收到"育儿补贴"短信，要求点击链接填写银行卡信息领取，你应该？',
    options: ['立即点击领取', '先填写看看', '通过官方渠道核实', '转发给朋友一起领'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '政府补贴会通过官方渠道发放，不会要求点击不明链接或提供银行卡信息。遇到此类情况要核实真伪。'
  },
  {
    question: '孩子收到同学发来的消息"急需用钱，请转账500元"，孩子应该？',
    options: ['立即转账帮助同学', '先打电话确认', '先转一部分试试', '询问其他同学是否知道'],
    correct: 1,
    selected: null,
    answered: false,
    explanation: '收到转账要求要打电话确认，可能是账号被盗或冒充。不要轻信网络消息，涉及金钱要格外谨慎。'
  },
  {
    question: '有人邀请孩子参加"免费游戏活动"，还能领取"稀有皮肤"，孩子应该？',
    options: ['立即参加领取皮肤', '先去看看情况', '拒绝并告诉家长', '叫上朋友一起去'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '"免费领取"往往是诈骗的诱饵。不要贪图小便宜，遇到可疑情况要告诉家长，保护自己的财产安全。'
  }
]

const currentVideo = computed(() => videos[currentVideoIndex.value])

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
  background: #f5f5f5;
}

.page-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 25%;
  min-width: 260px;
  background: white;
  border-right: 1px solid #e0e0e0;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-nav {
  padding: 16px;
}

.nav-section {
  margin-bottom: 24px;
}

.nav-section:last-child {
  margin-bottom: 0;
}

.nav-section-title {
  font-size: 0.85rem;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
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
  gap: 10px;
  padding: 12px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 6px;
  color: #666;
  font-size: 0.9rem;
}

.nav-item:hover {
  background: #f5f5f5;
  color: #333;
}

.nav-item.active {
  background: linear-gradient(135deg, #c5e8b7, #a8d89a);
  color: #3d6b2e;
  font-weight: 500;
}

.nav-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.nav-text {
  flex: 1;
}

.main-content {
  flex: 1;
  padding: 20px 30px;
  background: white;
}

.content-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 1.6rem;
  color: #333;
  margin-bottom: 14px;
  font-weight: 700;
}

.knowledge-section {
  background: linear-gradient(135deg, #f0fff4, #e8f5e9);
  border-left: 4px solid #a8d89a;
  border-radius: 8px;
  padding: 14px 18px;
}

.knowledge-title {
  font-size: 1rem;
  color: #5a9e4a;
  margin-bottom: 8px;
  font-weight: 600;
}

.knowledge-text {
  color: #555;
  line-height: 1.6;
  font-size: 0.9rem;
}

.video-section {
  margin-bottom: 20px;
}

.quiz-section {
  padding: 0;
}

@media (max-width: 1024px) {
  .page-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
  }

  .main-content {
    padding: 16px;
  }

  .page-title {
    font-size: 1.4rem;
  }
}
</style>
