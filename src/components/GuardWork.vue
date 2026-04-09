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
                :class="{ active: currentVideoIndex === index && !showQuiz && !showCheckTool }"
                @click="selectVideo(index)"
              >
                <span class="nav-icon"><font-awesome-icon icon="video" /></span>
                <span class="nav-text">{{ video.title }}</span>
              </li>
            </ul>
          </div>

          <div class="nav-section">
            <h4 class="nav-section-title">实用工具</h4>
            <ul class="nav-list">
              <li
                class="nav-item"
                :class="{ active: showCheckTool }"
                @click="startCheckTool"
              >
                <span class="nav-icon"><font-awesome-icon icon="search" /></span>
                <span class="nav-text">公司风险自查</span>
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
        </nav>
      </aside>

      <main class="main-content">
        <!-- 视频学习页面 -->
        <div v-if="!showQuiz && !showCheckTool">
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
        </div>

        <!-- 公司风险自查页面 -->
        <div v-else-if="showCheckTool" class="check-tool-page">
          <div class="check-tool-header">
            <h1 class="page-title">公司风险自查工具</h1>
            <p class="tool-description">输入公司名称，快速识别该公司是否存在诈骗风险</p>
          </div>

          <div class="check-tool-content">
            <div class="input-group">
              <input 
                v-model="companyName" 
                type="text" 
                placeholder="请输入公司名称进行风险自查"
                class="company-input"
                @keyup.enter="checkCompany"
              />
              <button @click="checkCompany" class="check-btn">
                <span class="btn-icon"><font-awesome-icon icon="search" /></span>
                <span>立即自查</span>
              </button>
            </div>
            
            <div v-if="checkResult" class="result-card" :class="checkResult.riskLevel">
              <div class="result-header">
                <span class="result-icon" v-html="checkResult.icon"></span>
                <span class="result-title">{{ checkResult.title }}</span>
              </div>
              <p class="result-description">{{ checkResult.description }}</p>
              <div v-if="checkResult.risks && checkResult.risks.length > 0" class="risk-list">
                <h4 class="risk-list-title">风险点：</h4>
                <ul>
                  <li v-for="(risk, index) in checkResult.risks" :key="index">
                    {{ risk }}
                  </li>
                </ul>
              </div>
              <div v-if="checkResult.suggestions && checkResult.suggestions.length > 0" class="suggestion-list">
                <h4 class="suggestion-list-title">建议⚠️</h4>
                <ul>
                  <li v-for="(suggestion, index) in checkResult.suggestions" :key="index">
                    {{ suggestion }}
                  </li>
                </ul>
              </div>
            </div>

            <div v-if="!checkResult" class="check-tips">
              <h3 class="tips-title">自查说明</h3>
              <div class="tips-content">
                <div class="tip-item">
                  <span class="tip-icon">💡</span>
                  <div class="tip-text">
                    <strong>高风险关键词⚠️</strong>
                    <span>刷单、兼职、返利、培训贷⚠️</span>
                  </div>
                </div>
                <div class="tip-item">
                  <span class="tip-icon">⚠️</span>
                  <div class="tip-text">
                    <strong>中风险关键词⚠️</strong>
                    <span>投资、理财、金融等</span>
                  </div>
                </div>
                <div class="tip-item">
                  <span class="tip-icon">💡</span>
                  <div class="tip-text">
                    <strong>低风险：</strong>
                    <span>未包含明显风险关键词的公司</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 防骗测试页面 -->
        <div v-else class="quiz-section">
          <QuizComponent :quizzes="quizzes" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import VideoPlayer from '../components/VideoPlayer.vue'
import QuizComponent from '../components/QuizComponent.vue'

const currentVideoIndex = ref(0)
const showQuiz = ref(false)
const showCheckTool = ref(false)
const companyName = ref('')
const checkResult = ref(null)

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
    title: '企业财会人员防诈',
    url: '/videos/workplace/caihui.mp4',
    knowledge: '企业财会人员是诈骗分子的重点目标。常见诈骗手段包括：冒充公司领导要求紧急转账、伪造供应商变更收款账户、虚假发票诈骗等。财会人员务必严格执行财务制度，大额转账必须当面或电话核实，不轻信邮件、微信等渠道的转账指令。'
  }
]

const quizzes = [
  {
    question: '在网上看到刷单兼职，日赚300-500元的广告，你应该？',
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
    question: '收到"公司领导"发来的微信，要求你紧急转1万元给客户，你应该？',
    options: ['立即转账，展现执行力', '回复"好的"后拖延时间', '打电话或当面核实领导身份', '先转一小部分试试'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '收到转账要求务必通过电话或当面核实！骗子常冒充领导实施诈骗，不要轻信社交软件上的身份。'
  },
  {
    question: '某公司承诺月薪2万，包培训，但要求你办3万元培训贷款，你应该？',
    options: ['办理贷款，入职后工资高', '先办理，培训完再想办法', '拒绝并举报，这是培训贷诈骗', '询问是否可以分期付款'],
    correct: 2,
    selected: null,
    answered: false,
    explanation: '这是典型的培训贷诈骗！正规公司不会要求员工贷款培训，高薪承诺往往是诱饵。'
  },
  {
    question: '作为企业财务人员，收到供应商邮件要求变更收款账户，你应该？',
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
  showCheckTool.value = false
}

const startQuiz = () => {
  showQuiz.value = true
  showCheckTool.value = false
}

const startCheckTool = () => {
  showCheckTool.value = true
  showQuiz.value = false
}

const checkCompany = () => {
  if (!companyName.value.trim()) {
    alert('请输入公司名称')
    return
  }

  const name = companyName.value.trim().toLowerCase()
  
  if (name.includes('刷单') || name.includes('兼职') || name.includes('返利')) {
    checkResult.value = {
      riskLevel: 'high',
      icon: '<font-awesome-icon icon="triangle-exclamation" />',
      title: '高风险公司',
      description: '该公司名称包含刷单、兼职、返利等关键词，极有可能是诈骗公司。',
      risks: [
        '承诺高额返利或轻松赚钱',
        '要求先垫付资金',
        '工作内容不明确',
        '无法提供正规营业执照'
      ],
      suggestions: [
        '立即停止与该公司的任何交易',
        '不要向该公司转账或提供个人信息',
        '向相关部门举报该公司',
        '选择正规渠道寻找工作'
      ]
    }
  } else if (name.includes('培训') && name.includes('贷')) {
    checkResult.value = {
      riskLevel: 'high',
      icon: '<font-awesome-icon icon="triangle-exclamation" />',
      title: '高风险公司',
      description: '该公司名称包含培训贷，极有可能是诈骗公司。',
      risks: [
        '要求办理贷款支付培训费',
        '承诺高薪但要求先付费',
        '培训内容与实际工作不符',
        '存在强制贷款条款'
      ],
      suggestions: [
        '拒绝办理任何形式的培训贷款',
        '核实公司资质和培训内容',
        '向教育部门或市场监管部门举报',
        '选择正规培训机构'
      ]
    }
  } else if (name.includes('投资') || name.includes('理财')) {
    checkResult.value = {
      riskLevel: 'medium',
      icon: '<font-awesome-icon icon="triangle-exclamation" />',
      title: '中风险公司',
      description: '该公司涉及投资理财业务，请谨慎对待。',
      risks: [
        '承诺高收益零风险',
        '要求向个人账户转账',
        '缺乏正规金融牌照',
        '投资项目信息不透明'
      ],
      suggestions: [
        '核实公司是否持有金融牌照',
        '不轻信高收益承诺',
        '通过正规金融机构投资',
        '咨询专业人士意见'
      ]
    }
  } else {
    checkResult.value = {
      riskLevel: 'low',
      icon: '<font-awesome-icon icon="lightbulb" />',
      title: '暂未发现明显风险',
      description: '根据公司名称初步判断，暂未发现明显的诈骗风险特征。但仍建议您谨慎核实。',
      risks: [],
      suggestions: [
        '核实公司营业执照和资质',
        '查看公司官方网站和评价',
        '了解公司经营状况和口碑',
        '如有疑问可咨询相关部门'
      ]
    }
  }
}
</script>

<style scoped>
.workplace-page {
  min-height: 100vh;
  background: #f8fbfe;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
}

.page-layout {
  display: flex;
  min-height: 100vh;
}

/* 左侧导航栏 - 保持不变 */
.sidebar {
  width: 280px;
  background: #fff;
  border-right: 1px solid #e0f2fe;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  box-shadow: 2px 0 8px rgba(93, 176, 223, 0.1);
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
  color: #5db0df;
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
  background: linear-gradient(135deg, #5db0df, #4a98c2);
  color: #fff;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(93, 176, 223, 0.3);
}

.nav-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.nav-text {
  flex: 1;
}

/* ========== 右侧区域修改 - 与其他页面视频大小一致 ========== */
.main-content {
  flex: 1;
  padding: 8px 40px 32px 40px;
  background: #fff;
}

.content-header {
  margin-bottom: 28px;  /* 增加标题与视频间距 */
}

.page-title {
  font-size: 26px;
  color: #2a5a6a;
  margin-bottom: 0;
  font-weight: 700;
}

/* 视频区域 - 与其他页面大小一致 */
.video-section {
  margin-bottom: 24px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(93, 176, 223, 0.15);
  max-width: 60%;  /* 从76%改为60%，与其他页面一致 */
  margin-left: auto;
  margin-right: auto;
}

/* 控制视频高度比例 - 与其他页面一致 */
.video-section :deep(.video-wrapper) {
  padding-top: 45% !important;  /* 从52%改为45%，与其他页面一致 */
}

.knowledge-section {
  background: linear-gradient(135deg, #e0f2fe, #d0ebfc);
  border-left: 4px solid #5db0df;
  border-radius: 12px;
  padding: 12px 20px;
  margin-bottom: 20px;
  margin-top: 4px;
  box-shadow: 0 2px 8px rgba(93, 176, 223, 0.15);
}

.knowledge-title {
  font-size: 18px;
  color: #5a9ab8;
  margin-bottom: 8px;
  font-weight: 600;
}

.knowledge-text {
  color: #4a6a7a;
  line-height: 1.5;
  font-size: 15px;
}

/* 公司风险自查页面样式 */
.check-tool-page {
  max-width: 800px;
}

.check-tool-header {
  margin-bottom: 20px;
}

.tool-description {
  color: #5a7a8a;
  font-size: 15px;
  margin-top: 6px;
}

.check-tool-content {
  background: #f8fbfe;
  border-radius: 16px;
  padding: 20px 24px;
  border: 1px solid #e0f2fe;
  box-shadow: 0 4px 16px rgba(93, 176, 223, 0.1);
}

.input-group {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.company-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e0f2fe;
  border-radius: 10px;
  font-size: 15px;
  color: #2a5a6a;
  outline: none;
  transition: all 0.2s ease;
}

.company-input:focus {
  border-color: #5db0df;
  box-shadow: 0 0 0 3px rgba(93, 176, 223, 0.1);
}

.check-btn {
  padding: 12px 22px;
  background: linear-gradient(135deg, #5db0df, #4a98c2);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(93, 176, 223, 0.3);
}

.result-card {
  background: #fff;
  border-radius: 12px;
  padding: 18px 22px;
  margin-top: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border-left: 4px solid;
}

.result-card.high {
  border-left-color: #ff6b6b;
}

.result-card.medium {
  border-left-color: #ffa94d;
}

.result-card.low {
  border-left-color: #51cf66;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.result-icon {
  font-size: 28px;
}

.result-title {
  font-size: 18px;
  font-weight: 600;
}

.result-description {
  color: #4a6a7a;
  line-height: 1.5;
  margin-bottom: 16px;
  font-size: 15px;
}

.risk-list,
.suggestion-list {
  margin-top: 12px;
}

.risk-list-title,
.suggestion-list-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #2a5a6a;
}

.risk-list li,
.suggestion-list li {
  padding: 6px 0;
  padding-left: 22px;
  font-size: 14px;
}

.check-tips {
  background: #fff;
  border-radius: 12px;
  padding: 18px 22px;
  margin-top: 16px;
  border: 1px solid #e0f2fe;
}

.tips-title {
  font-size: 17px;
  color: #2a5a6a;
  margin-bottom: 16px;
  font-weight: 600;
}

.tips-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 14px;
  background: #f8fbfe;
  border-radius: 8px;
}

.tip-icon {
  font-size: 22px;
  flex-shrink: 0;
}

.tip-text {
  color: #4a6a7a;
  font-size: 14px;
  line-height: 1.5;
}

.quiz-section {
  padding: 0;
}

/* 响应式 - 与其他页面一致 */
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
    padding: 12px 20px;
  }
  
  .content-header {
    margin-bottom: 24px;
  }

  .page-title {
    font-size: 24px;
  }
  
  .video-section {
    max-width: 75%;  /* 平板宽度与其他页面一致 */
  }

  .check-tool-content {
    padding: 16px 20px;
  }

  .input-group {
    flex-direction: column;
  }

  .check-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .sidebar-nav {
    padding: 16px 12px;
  }

  .main-content {
    padding: 10px 16px;
  }
  
  .content-header {
    margin-bottom: 20px;
  }

  .page-title {
    font-size: 20px;
  }
  
  .video-section {
    margin-bottom: 20px;
    max-width: 90%;  /* 手机宽度与其他页面一致 */
  }
  
  .video-section :deep(.video-wrapper) {
    padding-top: 56.25% !important;
  }

  .knowledge-section {
    padding: 10px 16px;
  }

  .knowledge-title {
    font-size: 16px;
  }
  
  .knowledge-text {
    font-size: 14px;
  }

  .check-tool-content {
    padding: 14px 16px;
  }
  
  .result-card {
    padding: 14px 18px;
  }
  
  .check-tips {
    padding: 14px 18px;
  }
}
</style>