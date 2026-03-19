<template>
  <div class="workplace-page">
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
    title: '谨防电信诈骗',
    url: '/videos/workplace/dianxin.mp4',
    knowledge: '电信诈骗是指利用电话、短信、网络等通讯工具，虚构事实或隐瞒真相，骗取公私财物的行为。常见类型包括冒充客服退款、冒充公检法、冒充领导转账等。防范要点：不轻信陌生来电，不透露个人信息，不向陌生账户转账。遇到可疑情况，及时拨打96110反诈专线咨询。'
  },
  {
    title: '刷单诈骗',
    url: '/videos/workplace/shuadan.mp4',
    knowledge: '刷单诈骗是指骗子以"轻松兼职、高额返利"为诱饵，诱导受害者进行虚假交易刷单。骗子通常会先让受害者完成几单小额任务并给予返利，获取信任后，再诱导受害者投入大额资金，最终卷款消失。记住：所有刷单都是诈骗，不要相信"轻松赚钱"的兼职广告。'
  },
  {
    title: '企业财会人员防诈骗',
    url: '/videos/workplace/caikui.mp4',
    knowledge: '企业财会人员是诈骗分子的重点目标。常见诈骗手段包括：冒充公司领导要求紧急转账、伪造供应商变更收款账户、虚假发票诈骗等。财会人员务必严格执行财务制度，大额转账必须当面或电话核实，不轻信邮件、微信等渠道的转账指令。'
  }
]

const quizzes = [
  {
    question: '在网上看到"刷单兼职，日赚300-500元"的广告，你应该？',
    options: ['试试看，赚点零花钱', '先做一单试试真假', '立即举报，所有刷单都是诈骗', '推荐给朋友一起做'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '所有刷单都是诈骗！骗子先用小额返利获取信任，再诱导大额投入后消失。'
  },
  {
    question: '收到"客服"电话，称你购买的商品有质量问题需要退款，要求你点击链接填写银行卡信息，你应该？',
    options: ['立即点击链接填写', '先核实客服身份再决定', '提供部分信息试试', '按照客服指示操作'],
    correct: 1,
    selected: null,
    answered: false,
    explanation: '收到退款电话要警惕！正规客服不会要求点击不明链接或提供银行卡信息，应通过官方渠道核实。'
  },
  {
    question: '收到"公司领导"发来的微信，要求你紧急转账5万元给客户，你应该？',
    options: ['立即转账，展现执行力', '回复"好的"后拖延时间', '打电话或当面核实领导身份', '先转一小部分试试'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '收到转账要求务必通过电话或当面核实！骗子常冒充领导实施诈骗，不要轻信社交软件上的身份。'
  },
  {
    question: '某公司承诺"月薪2万，包培训"，但要求你办理3万元培训贷款，你应该？',
    options: ['办理贷款，入职后工资高', '先办理，培训完再想办法', '拒绝并举报，这是培训贷诈骗', '询问是否可以分期付款'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '这是典型的"培训贷"诈骗！正规公司不会要求员工贷款培训，高薪承诺往往是诱饵。'
  },
  {
    question: '作为企业财务人员，收到"供应商"邮件要求变更收款账户，你应该？',
    options: ['立即按邮件要求变更', '先小额转账测试', '电话联系供应商核实', '转发给同事处理'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '财务人员必须电话核实账户变更信息！骗子常伪造供应商邮件实施诈骗，切勿轻信邮件指令。'
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
.workplace-page {
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
  background: linear-gradient(135deg, #a8d8ea, #81c9d4);
  color: #2c5f6e;
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
  background: linear-gradient(135deg, #f0f9ff, #e3f2fd);
  border-left: 4px solid #a8d8ea;
  border-radius: 8px;
  padding: 14px 18px;
}

.knowledge-title {
  font-size: 1rem;
  color: #5a9eb8;
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
