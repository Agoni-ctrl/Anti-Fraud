<template>
  <div class="elder-guard-page">
    <div class="page-layout">
      <aside class="sidebar">
        <nav class="sidebar-nav">
          <div class="nav-section">
            <h4 class="nav-section-title">
              <i class="fas fa-video"></i> 视频学习
            </h4>
            <ul class="nav-list">
              <li
                v-for="(video, index) in videos"
                :key="index"
                class="nav-item"
                :class="{ active: currentVideoIndex === index && !showQuiz }"
                @click="selectVideo(index)"
              >
                <i class="fas fa-play-circle"></i>
                <span class="nav-text">{{ video.title }}</span>
              </li>
            </ul>
          </div>

          <div class="nav-section">
            <h4 class="nav-section-title">
              <i class="fas fa-tasks"></i> 防骗小测试
            </h4>
            <ul class="nav-list">
              <li
                class="nav-item"
                :class="{ active: showQuiz }"
                @click="startQuiz"
              >
                <i class="fas fa-bullseye"></i>
                <span class="nav-text">开始测试</span>
              </li>
            </ul>
          </div>
        </nav>
      </aside>

      <main class="main-content">
        <div v-if="!showQuiz">
          <div class="content-header">
            <h1 class="page-title">
              <i class="fas fa-graduation-cap"></i>
              {{ currentVideo.title }}
              <button class="speak-btn" @click="speakText(currentVideo.title)" title="朗读标题">
                <i class="fas fa-volume-up"></i>
              </button>
            </h1>
          </div>

          <div class="video-section">
            <VideoPlayer :video-url="currentVideo.url" />
          </div>
          
          <div class="knowledge-section">
            <h3 class="knowledge-title">
              <i class="fas fa-lightbulb"></i> 知识点
            </h3>
            <div class="knowledge-content">
              <div 
                v-for="(sentence, index) in currentVideoSentences" 
                :key="index" 
                class="sentence-item"
              >
                <i class="fas fa-check-circle"></i>
                <span class="sentence-text">{{ sentence }}</span>
                <button class="speak-btn" @click="speakText(sentence)" title="朗读这段话">
                  <i class="fas fa-volume-up"></i>
                </button>
              </div>
            </div>
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
import { ref, computed, onUnmounted } from 'vue'
import VideoPlayer from '../components/VideoPlayer.vue'
import QuizComponent from '../components/QuizComponent.vue'

const currentVideoIndex = ref(0)
const showQuiz = ref(false)
const isSpeaking = ref(false)
let speechSynthesis = null
let currentUtterance = null

if ('speechSynthesis' in window) {
  speechSynthesis = window.speechSynthesis
}

const videos = [
  {
    title: '常见养老诈骗套路',
    url: '/videos/elder/taolu.mp4',
    knowledge: '养老诈骗是专门针对老年群体的诈骗行为，常见类型包括虚假养老服务、保健品诈骗、投资理财诈骗、冒充公检法等。骗子利用老年人信息闭塞、情感孤独、渴望健康等特点，精心设计骗局。老年人要提高警惕，不轻信陌生人的承诺，不向陌生账户转账，遇到可疑情况及时向子女或警方求助。'
  },
  {
    title: '奶奶智破骗局',
    url: '/videos/elder/nainai.mp4',
    knowledge: '真实案例分享：张奶奶接到"孙子"的求助电话，说"出车祸急需用钱"。张奶奶没有慌张，而是先打电话给儿子核实，成功识破了骗局。这个案例告诉我们：遇到亲属求助电话要亲自确认，不要轻信陌生来电。骗子常冒充亲属实施诈骗，要通过其他渠道核实情况。'
  },
  {
    title: '守护养老钱袋子',
    url: '/videos/elder/qiandai.mp4',
    knowledge: '守护养老钱需要全家共同努力。老年人要记住"三不一多"原则：不轻信陌生来电、不透露个人信息、不向陌生账户转账、多与子女沟通。子女要常与父母联系，关注父母的网络活动和社交情况，帮助父母识别骗局。遇到可疑情况，及时拨打96110反诈专线。'
  }
]

const quizzes = [
  {
    question: '接到"警察"电话，说你涉嫌犯罪，要求转账到"安全账户"，你应该？',
    options: ['立即转账证明清白', '按照指示操作', '挂断电话并报警', '向对方询问具体情况'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '公检法机关不会通过电话办案，更不会要求转账汇款。这是典型的冒充公检法诈骗，要立即挂断电话并报警。'
  },
  {
    question: '有人向你推销"神奇保健品"，声称能"包治百病"，你应该？',
    options: ['立即购买试试', '先买少量看看效果', '拒绝并告知子女', '推荐给其他老人'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '保健品不能替代药品，生病要去正规医院治疗。不要轻信"包治百病"的宣传，购买保健品要通过正规渠道。'
  },
  {
    question: '有人推荐"养老公寓投资"，承诺"高收益零风险"，你应该？',
    options: ['立即投资养老', '先投资一小部分', '拒绝并咨询子女', '向其他老人了解'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '高收益必然伴随高风险，不要相信"保本保息"的承诺。投资要通过正规金融机构，遇到可疑情况要咨询子女或专业人士。'
  },
  {
    question: '收到"孙子"的求助电话，说"出车祸急需用钱"，你应该？',
    options: ['立即汇款救人', '先汇一部分', '打电话给本人确认', '向其他家人询问'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '收到亲属求助电话要亲自确认，不要轻信陌生来电。骗子常冒充亲属实施诈骗，要通过其他渠道核实情况。'
  },
  {
    question: '有人邀请参加"免费健康讲座"，还能领取"免费礼品"，你应该？',
    options: ['立即参加领礼品', '先去看看情况', '拒绝并告知子女', '叫上其他老人一起'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '"免费讲座"往往是推销保健品的幌子。不要贪图小便宜，遇到可疑情况要告知子女，避免上当受骗。'
  }
]

const currentVideo = computed(() => videos[currentVideoIndex.value])

const currentVideoSentences = computed(() => {
  const knowledge = currentVideo.value.knowledge
  const sentences = knowledge.split(/[。！？]/).filter(s => s.trim())
  return sentences.map(s => s + '。')
})

const selectVideo = (index) => {
  currentVideoIndex.value = index
  showQuiz.value = false
  stopSpeech()
}

const startQuiz = () => {
  showQuiz.value = true
  stopSpeech()
}

const speakText = (text) => {
  if (!speechSynthesis) {
    alert('您的浏览器不支持语音播报功能')
    return
  }
  
  stopSpeech()
  
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'zh-CN'
  utterance.rate = 0.85
  utterance.pitch = 1.0
  utterance.volume = 1.0
  
  const voices = speechSynthesis.getVoices()
  const femaleVoice = voices.find(voice => 
    voice.lang.includes('zh') && 
    (voice.name.includes('Female') || voice.name.includes('女') || voice.name.includes('Xiaoxiao'))
  )
  if (femaleVoice) {
    utterance.voice = femaleVoice
  }
  
  utterance.onstart = () => {
    isSpeaking.value = true
  }
  
  utterance.onend = () => {
    isSpeaking.value = false
  }
  
  utterance.onerror = () => {
    isSpeaking.value = false
  }
  
  currentUtterance = utterance
  speechSynthesis.speak(utterance)
}

const stopSpeech = () => {
  if (speechSynthesis) {
    speechSynthesis.cancel()
    isSpeaking.value = false
    currentUtterance = null
  }
}

onUnmounted(() => {
  stopSpeech()
})
</script>

<style scoped>
.elder-guard-page {
  min-height: 100vh;
  background: #f0f9ff;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  font-size: 18px;
}

.page-layout {
  display: flex;
  min-height: 100vh;
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
  font-size: 24px;
  color: #0064b2;
  font-weight: 700;
  margin-bottom: 20px;
  padding: 12px 8px;
  background: linear-gradient(135deg, #e6f3ff, #f0f9ff);
  border-radius: 12px;
  letter-spacing: 2px;
}

.nav-section-title i {
  margin-right: 12px;
  font-size: 22px;
  color: #0099ff;
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
  padding: 14px 18px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 10px;
  color: #1a3a5a;
  font-size: 17px;
  background: #f8fbfe;
  border: 1px solid #e0f2fe;
}

.nav-item i {
  width: 22px;
  font-size: 18px;
  flex-shrink: 0;
  color: #0099ff;
}

.nav-item.active i {
  color: #fff;
}

.nav-item:hover {
  background: #e0f2fe;
}

.nav-item.active {
  background: linear-gradient(135deg, #0064b2, #0099ff);
  color: #fff;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0, 100, 178, 0.25);
}

.nav-text {
  flex: 1;
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
  font-size: 28px;
  color: #0064b2;
  margin-bottom: 0;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title i {
  font-size: 30px;
  color: #0099ff;
}

.video-section {
  margin-bottom: 48px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 100, 178, 0.12);
  max-width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.knowledge-section {
  background: linear-gradient(135deg, #f8fbfe, #f0f9ff);
  border-radius: 16px;
  padding: 28px 32px;
  margin-top: 16px;
  border: 1px solid #e0f2fe;
  border-left: 4px solid #0064b2;
}

.knowledge-title {
  font-size: 24px;
  color: #0064b2;
  margin-bottom: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
}

.knowledge-title i {
  font-size: 26px;
  color: #ffc107;
}

.knowledge-content {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.sentence-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 18px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e0f2fe;
  transition: all 0.2s ease;
}

.sentence-item:hover {
  background: #f8fbfe;
  box-shadow: 0 2px 8px rgba(0, 100, 178, 0.08);
}

.sentence-item i {
  font-size: 20px;
  color: #28a745;
  margin-top: 3px;
  flex-shrink: 0;
}

.sentence-text {
  flex: 1;
  color: #2a4a6a;
  line-height: 1.7;
  font-size: 17px;
}

.speak-btn {
  background: linear-gradient(135deg, #0064b2, #0099ff);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #fff;
  box-shadow: 0 2px 8px rgba(0, 100, 178, 0.25);
}

.speak-btn i {
  font-size: 18px;
  color: #fff;
}

.speak-btn:hover {
  background: linear-gradient(135deg, #0055a0, #0088ee);
  transform: scale(1.08);
  box-shadow: 0 4px 12px rgba(0, 100, 178, 0.35);
}

.speak-btn:active {
  transform: scale(0.96);
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
    border-bottom: 1px solid #e0f2fe;
  }

  .main-content {
    padding: 24px 20px;
  }

  .page-title {
    font-size: 24px;
  }
  
  .page-title i {
    font-size: 26px;
  }
  
  .video-section {
    margin-bottom: 40px;
  }
  
  .knowledge-section {
    padding: 24px 28px;
  }
  
  .knowledge-title {
    font-size: 22px;
  }
  
  .knowledge-title i {
    font-size: 24px;
  }

  .sentence-text {
    font-size: 16px;
  }
  
  .sentence-item i {
    font-size: 18px;
  }

  .speak-btn {
    width: 38px;
    height: 38px;
  }
  
  .speak-btn i {
    font-size: 16px;
  }
}

@media (max-width: 768px) {
  .sidebar-nav {
    padding: 16px 12px;
  }
  
  .nav-section-title {
    font-size: 20px;
    padding: 10px 8px;
  }
  
  .nav-section-title i {
    font-size: 18px;
  }

  .main-content {
    padding: 20px 16px;
  }

  .page-title {
    font-size: 22px;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .page-title i {
    font-size: 24px;
  }
  
  .video-section {
    margin-bottom: 36px;
  }

  .knowledge-section {
    padding: 20px 18px;
    margin-top: 12px;
  }

  .knowledge-title {
    font-size: 20px;
  }
  
  .knowledge-title i {
    font-size: 22px;
  }

  .sentence-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .sentence-item i {
    margin-top: 0;
  }

  .speak-btn {
    align-self: flex-end;
  }
}
</style>