<template>
  <div class="main-container">
    <section class="hero-section">
      <h1 class="hero-title">亲子课堂</h1>
      <p class="hero-subtitle">守护家庭财产安全，让骗子无处遁形</p>
    </section>

    <div class="two-column-layout">
      <div class="content-card">
        <h2 class="card-title">
          <span class="card-icon">🚨</span>
          警惕！宝妈群体高发诈骗类型
        </h2>

        <div class="warning-box">
          <h3 class="warning-title">刷单返利诈骗专盯宝妈</h3>
          <p class="warning-text">
            诈骗分子利用宝妈希望在家赚钱补贴家用的心理，以"轻松兼职、日赚百元"为诱饵，
            诱导受害者进行刷单操作。<strong style="color: #E65100;">记住：所有刷单都是诈骗！</strong>
          </p>
        </div>

        <div class="fraud-type-grid">
          <div class="fraud-type-card" v-for="(fraud, index) in fraudTypes" :key="index">
            <div class="fraud-type-icon">{{ fraud.icon }}</div>
            <h4 class="fraud-type-title">{{ fraud.title }}</h4>
            <p class="fraud-type-desc">{{ fraud.desc }}</p>
          </div>
        </div>
      </div>

      <div class="content-card">
        <h2 class="card-title">
          <span class="card-icon">🛡️</span>
          防范技巧，守护家庭
        </h2>

        <ul class="tips-list">
          <li class="tips-item" v-for="(tip, index) in preventionTips" :key="index">
            <span class="tips-number">{{ index + 1 }}</span>
            <div class="tips-content">
              <h4>{{ tip.title }}</h4>
              <p>{{ tip.content }}</p>
            </div>
          </li>
        </ul>
      </div>

      <div class="content-card full-width">
        <h2 class="card-title">
          <span class="card-icon">📖</span>
          真实案例警示
        </h2>

        <div class="two-column-layout" style="padding: 0; gap: 15px;">
          <div class="case-card" v-for="(caseItem, index) in realCases" :key="index">
            <span class="case-badge">真实案例</span>
            <h4 class="case-title">{{ caseItem.title }}</h4>
            <p class="case-content">{{ caseItem.content }}</p>
            <div class="case-highlight">
              <strong>💡 警示：</strong>{{ caseItem.warning }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="quiz-btn-container">
      <button class="quiz-start-btn" @click="startQuiz">
        🎯 开始防骗小测试
      </button>
    </div>

    <div class="emergency-section">
      <h3 class="emergency-title">🆘 遇到诈骗怎么办？</h3>
      <div class="emergency-phone">96110</div>
      <p class="emergency-desc">全国反诈专线 | 24小时为您服务</p>
    </div>

    <div v-if="showQuizModal" class="quiz-modal-overlay" @click.self="closeQuiz">
      <div class="quiz-modal">
        <button class="quiz-close-btn" @click="closeQuiz">&times;</button>

        <div v-if="!quizFinished">
          <h3 class="quiz-modal-title">🎯 防骗小测试</h3>

          <div class="quiz-question-box">
            <div class="quiz-question-num">问题 {{ currentQuestionIndex + 1 }} / {{ quizzes.length }}</div>
            <div class="quiz-question-text">{{ currentQuiz.question }}</div>
          </div>

          <div class="quiz-options-box">
            <div v-for="(option, oIndex) in currentQuiz.options" :key="oIndex" class="quiz-option-btn" :class="{
                'selected': currentQuiz.selected === oIndex && !currentQuiz.answered,
                'correct': currentQuiz.answered && oIndex === currentQuiz.correct,
                'wrong': currentQuiz.answered && currentQuiz.selected === oIndex && oIndex !== currentQuiz.correct
              }" @click="selectOption(oIndex)">
              {{ option }}
            </div>
          </div>

          <div v-if="currentQuiz.answered" class="quiz-explanation">
            <span v-if="currentQuiz.selected === currentQuiz.correct" style="color: #4CAF50; font-weight: bold;">✅
              回答正确！</span>
            <span v-else style="color: #EF5350; font-weight: bold;">❌ 回答错误。</span>
            {{ currentQuiz.explanation }}
          </div>

          <div class="quiz-nav-btns">
            <button class="quiz-nav-btn" @click="prevQuestion" :disabled="currentQuestionIndex === 0">上一题</button>
            <button v-if="!currentQuiz.answered" class="quiz-nav-btn" @click="confirmAnswer"
              :disabled="currentQuiz.selected === null">确认答案</button>
            <button v-else class="quiz-nav-btn" @click="nextQuestion">
              {{ currentQuestionIndex === quizzes.length - 1 ? '查看成绩' : '下一题' }}
            </button>
          </div>
        </div>

        <div v-else class="quiz-result-box">
          <div class="quiz-score">{{ quizScore }}分</div>
          <div class="quiz-result-text">
            <span v-if="quizScore === 100">🎉 太棒了！满分！你是防骗小达人！</span>
            <span v-else-if="quizScore >= 66">👍 不错！继续保持警惕！</span>
            <span v-else>💪 还需努力，多学习防骗知识哦！</span>
          </div>
          <p style="color: #666; margin-bottom: 20px;">共 {{ quizzes.length }} 题，答对 {{ correctCount }} 题</p>
          <button class="quiz-restart-btn" @click="restartQuiz">再测一次</button>
        </div>
      </div>
    </div>

    <!-- 紧急求助弹窗 -->
    <div v-if="showEmergencyModal" class="emergency-modal-overlay" @click.self="closeEmergencyModal">
      <div class="emergency-modal">
        <button class="emergency-close-btn" @click="closeEmergencyModal">&times;</button>

        <div class="emergency-content">
          <div class="emergency-section map-section">
            <h3 class="section-title">
              <i class="fas fa-map-marker-alt"></i>
              附近公安局
            </h3>
            <div ref="amapContainer" class="amap-container">
              <div v-if="!mapLoaded && !mapError" class="map-loading">
                <i class="fas fa-spinner fa-spin"></i>
                <p>正在定位并搜索附近公安局...</p>
              </div>
              <div v-if="mapError" class="map-error">
                <i class="fas fa-exclamation-circle"></i>
                <p>{{ mapError }}</p>
                <button class="retry-btn" @click="initMap">重新加载</button>
              </div>
            </div>
            <div v-if="nearestPoliceStation" class="police-station-info">
              <div class="station-name">{{ nearestPoliceStation.name }}</div>
              <div class="station-address">{{ nearestPoliceStation.address }}</div>
              <div class="station-distance">距离约 {{ nearestPoliceStation.distance }} 米</div>
              <a :href="navigationUrl" target="_blank" class="navigate-btn">
                <i class="fas fa-directions"></i> 导航前往
              </a>
            </div>
            <div v-else-if="mapLoaded && !nearestPoliceStation" class="no-station-info">
              <p>未找到附近公安局，请手动搜索或拨打110</p>
            </div>

            <!-- 调试信息 -->
            <div v-if="debugInfo" class="debug-info">
              <div class="debug-title">🔧 调试信息</div>
              <pre>{{ debugInfo }}</pre>
            </div>
          </div>

          <div class="emergency-section">
            <h3 class="section-title">
              <i class="fas fa-clipboard-list"></i>
              报案需携带物品
            </h3>
            <ul class="items-list">
              <li class="item">
                <span class="item-icon">🆔</span>
                <div class="item-content">
                  <strong>身份证原件</strong>
                  <span>报案人本人身份证</span>
                </div>
              </li>
              <li class="item">
                <span class="item-icon">📱</span>
                <div class="item-content">
                  <strong>手机/通讯设备</strong>
                  <span>保存好聊天记录、通话记录</span>
                </div>
              </li>
              <li class="item">
                <span class="item-icon">💳</span>
                <div class="item-content">
                  <strong>银行卡/转账凭证</strong>
                  <span>银行流水、转账截图等</span>
                </div>
              </li>
              <li class="item">
                <span class="item-icon">📝</span>
                <div class="item-content">
                  <strong>相关证据材料</strong>
                  <span>诈骗信息截图、链接、APP等</span>
                </div>
              </li>
              <li class="item">
                <span class="item-icon">📋</span>
                <div class="item-content">
                  <strong>事件经过说明</strong>
                  <span>手写或打印的被骗经过</span>
                </div>
              </li>
            </ul>
          </div>

          <div class="emergency-tips">
            <div class="tips-title">⚠️ 温馨提示</div>
            <p>1. 发现被骗后请第一时间报警，不要犹豫</p>
            <p>2. 保留所有证据，不要删除任何相关信息</p>
            <p>3. 及时联系银行冻结相关账户</p>
            <p>4. 拨打96110反诈专线咨询</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ParentChildClassroom',
  data() {
    return {
      fraudTypes: [
        { icon: '📱', title: '刷单返利诈骗', desc: '以"轻松赚钱"为诱饵，要求先垫付资金刷单' },
        { icon: '💬', title: '虚假招聘诈骗', desc: '发布高薪兼职信息，收取培训费后消失' },
        { icon: '🎁', title: '免费领礼品诈骗', desc: '以免费领母婴用品为诱饵骗取信息' },
        { icon: '👥', title: '冒充客服诈骗', desc: '冒充电商平台客服骗取银行卡信息' }
      ],
      preventionTips: [
        { title: '拒绝所有刷单邀请', content: '任何要求先垫付资金的"兼职"都是诈骗。' },
        { title: '保护个人信息', content: '不随意填写身份证、银行卡信息。' },
        { title: '核实招聘信息', content: '通过正规招聘平台找工作，保持警惕。' },
        { title: '安装国家反诈APP', content: '开启来电预警功能，及时识别诈骗电话。' },
        { title: '与家人多沟通', content: '遇到可疑情况及时与家人商量。' }
      ],
      realCases: [
        {
          title: '案例一："轻松日赚300元"的陷阱',
          content: '李女士在微信群看到"刷单兼职，日赚300元"的广告。完成第一单后确实收到返利，于是继续投入，最终被骗走2万余元。',
          warning: '小额返利是诱饵，大额投入是陷阱！'
        },
        {
          title: '案例二："免费领婴儿车"骗局',
          content: '王女士在朋友圈看到"转发免费领婴儿车"活动。按要求转发后，对方以"邮费""海关税费"为由骗取200多元。',
          warning: '天上不会掉馅饼，免费领礼品往往是骗局。'
        },
        {
          title: '案例三：冒充客服退款诈骗',
          content: '张女士接到自称"某宝客服"电话，称奶粉有质量问题要退款。对方诱导其下载软件并开启屏幕共享，转走5万元。',
          warning: '正规退款不会要求下载软件或屏幕共享。'
        },
        {
          title: '案例四："高薪招聘试衣员"陷阱',
          content: '陈女士在某招聘网站看到"招聘试衣员，月薪8000"的信息。添加对方后被告知需先交500元"入职培训费"，交完钱后对方将其拉黑。',
          warning: '正规招聘不会收取任何费用，要求先交钱的都是诈骗！'
        }
      ],
      showQuizModal: false,
      currentQuestionIndex: 0,
      quizFinished: false,
      showEmergencyModal: false,
      mapLoaded: false,
      mapError: null,
      nearestPoliceStation: null,
      currentPosition: null,
      map: null,
      debugInfo: null,
      quizzes: [
        {
          question: '有人在群里发"刷单兼职，日赚200-500元"的信息，你应该怎么做？',
          options: ['先试试看，赚点零花钱', '立即举报并删除', '推荐给朋友一起做', '先交押金再开始'],
          correct: 1,
          selected: null,
          answered: false,
          explanation: '所有刷单都是诈骗！正规兼职不会要求先交钱，看到此类信息应立即举报。'
        },
        {
          question: '接到自称"电商平台客服"的电话，说你的订单有问题要退款，要求你下载软件，你应该？',
          options: ['按照要求下载软件', '先下载看看什么情况', '挂断电话，通过官方APP核实', '提供银行卡信息'],
          correct: 2,
          selected: null,
          answered: false,
          explanation: '正规退款不会要求下载软件！遇到此类情况应挂断电话，通过官方渠道核实。'
        },
        {
          question: '朋友圈看到"免费领婴儿用品，只需付邮费"的活动，正确的做法是？',
          options: ['转发参与，付邮费领取', '填写信息参与活动', '警惕这是骗局，不参与', '推荐给宝妈群'],
          correct: 2,
          selected: null,
          answered: false,
          explanation: '免费领礼品+付邮费是常见诈骗套路，目的是骗取小额资金或个人信息。'
        }
      ]
    }
  },
  methods: {
    startQuiz() {
      this.showQuizModal = true
      this.currentQuestionIndex = 0
      this.quizFinished = false
      this.quizzes.forEach(q => {
        q.selected = null
        q.answered = false
      })
    },
    closeQuiz() {
      this.showQuizModal = false
    },
    selectOption(index) {
      if (!this.currentQuiz.answered) {
        this.currentQuiz.selected = index
      }
    },
    confirmAnswer() {
      if (this.currentQuiz.selected !== null) {
        this.currentQuiz.answered = true
      }
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
      }
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.quizzes.length - 1) {
        this.currentQuestionIndex++
      } else {
        this.quizFinished = true
      }
    },
    restartQuiz() {
      this.currentQuestionIndex = 0
      this.quizFinished = false
      this.quizzes.forEach(q => {
        q.selected = null
        q.answered = false
      })
    },
    openEmergencyModal() {
      this.showEmergencyModal = true
      this.$nextTick(() => {
        this.initMap()
      })
    },
    closeEmergencyModal() {
      this.showEmergencyModal = false
      this.mapLoaded = false
      this.mapError = null
      this.nearestPoliceStation = null
      this.debugInfo = null
      if (this.map) {
        this.map.destroy()
        this.map = null
      }
    },
    initMap() {
      if (!window.AMap) {
        this.mapError = '地图加载失败，请检查网络连接'
        return
      }

      this.mapLoaded = false
      this.mapError = null

      // 获取当前位置
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const lng = position.coords.longitude
            const lat = position.coords.latitude
            this.currentPosition = [lng, lat]
            this.loadMap(lng, lat)
          },
          (error) => {
            console.error('定位失败:', error)
            // 使用默认位置（北京天安门）
            this.currentPosition = [116.397428, 39.90923]
            this.loadMap(116.397428, 39.90923)
          },
          { enableHighAccuracy: true, timeout: 10000 }
        )
      } else {
        this.mapError = '您的浏览器不支持地理定位'
      }
    },
    loadMap(lng, lat) {
      try {
        // 等待DOM更新完成
        this.$nextTick(() => {
          const container = this.$refs.amapContainer
          if (!container) {
            this.mapError = '地图容器未找到'
            return
          }

          // 创建地图
          this.map = new window.AMap.Map(container, {
            zoom: 15,
            center: [lng, lat],
            viewMode: '2D'
          })

          // 添加当前位置标记（小图标）
          const currentMarker = new window.AMap.Marker({
            position: [lng, lat],
            content: '<div style="width:20px;height:20px;background:#2196f3;border:3px solid white;border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>',
            offset: new window.AMap.Pixel(-10, -10)
          })
          currentMarker.setMap(this.map)

          // 添加定位精度圆圈
          new window.AMap.Circle({
            center: [lng, lat],
            radius: 200,
            fillColor: '#2196f3',
            fillOpacity: 0.15,
            strokeColor: '#2196f3',
            strokeWeight: 1,
            strokeOpacity: 0.3
          }).setMap(this.map)

          // 搜索附近公安局
          this.searchPoliceStation(lng, lat)
          this.mapLoaded = true
        })
      } catch (error) {
        console.error('地图初始化失败:', error)
        this.mapError = '地图初始化失败，请稍后重试'
      }
    },
    searchPoliceStation(lng, lat) {
      // 使用高德地图LocalSearch进行搜索
      let debugLogs = []

      debugLogs.push(`当前位置: ${lng}, ${lat}`)
      debugLogs.push(`使用LocalSearch搜索...`)

      // 加载LocalSearch插件
      window.AMap.plugin(['AMap.LocalSearch'], () => {
        const localSearch = new window.AMap.LocalSearch({
          pageSize: 10,
          pageIndex: 1
        })

        // 搜索派出所
        localSearch.searchNearBy('派出所', [lng, lat], 10000, (status, result) => {
          debugLogs.push(`派出所搜索状态: ${status}`)
          console.log('派出所搜索结果:', status, result)

          if (status === 'complete' && result && result.info === 'OK' && result.poiList && result.poiList.pois && result.poiList.pois.length > 0) {
            debugLogs.push(`✅ 找到派出所: ${result.poiList.pois[0].name}`)
            this.handleSearchResult(result.poiList.pois, debugLogs)
          } else {
            debugLogs.push(`❌ 未找到派出所`)
            if (result && result.info) debugLogs.push(`错误: ${result.info}`)

            // 搜索公安局
            localSearch.searchNearBy('公安局', [lng, lat], 10000, (status2, result2) => {
              debugLogs.push(`公安局搜索状态: ${status2}`)
              console.log('公安局搜索结果:', status2, result2)

              if (status2 === 'complete' && result2 && result2.info === 'OK' && result2.poiList && result2.poiList.pois && result2.poiList.pois.length > 0) {
                debugLogs.push(`✅ 找到公安局: ${result2.poiList.pois[0].name}`)
                this.handleSearchResult(result2.poiList.pois, debugLogs)
              } else {
                debugLogs.push(`❌ 未找到公安局`)

                // 搜索警务室
                localSearch.searchNearBy('警务室', [lng, lat], 10000, (status3, result3) => {
                  debugLogs.push(`警务室搜索状态: ${status3}`)
                  console.log('警务室搜索结果:', status3, result3)

                  if (status3 === 'complete' && result3 && result3.info === 'OK' && result3.poiList && result3.poiList.pois && result3.poiList.pois.length > 0) {
                    debugLogs.push(`✅ 找到警务室: ${result3.poiList.pois[0].name}`)
                    this.handleSearchResult(result3.poiList.pois, debugLogs)
                  } else {
                    debugLogs.push(`❌ 未找到警务室`)
                    this.nearestPoliceStation = null
                    this.mapError = '附近未找到公安局/派出所，请拨打110求助'
                    debugLogs.push('所有搜索完成，未找到结果')
                  }
                  this.debugInfo = debugLogs.join('\n')
                })
              }
            })
          }
        })
      })
    },
    handleSearchResult(pois, debugLogs) {
      // 找到最近的公安局
      const nearest = pois[0]
      this.nearestPoliceStation = {
        name: nearest.name,
        address: nearest.address || '暂无详细地址',
        location: nearest.location,
        distance: Math.round(nearest.distance)
      }

      // 在地图上标记公安局
      const policeMarker = new window.AMap.Marker({
        position: [nearest.location.lng, nearest.location.lat],
        title: nearest.name,
        content: '<div style="background:#4CAF50;color:white;padding:5px 10px;border-radius:15px;white-space:nowrap;font-size:12px;font-weight:bold;box-shadow:0 2px 6px rgba(0,0,0,0.3);">' + nearest.name + '</div>',
        offset: new window.AMap.Pixel(-50, -40)
      })
      policeMarker.setMap(this.map)

      // 调整地图视野包含两个点
      this.map.setFitView([policeMarker], false, [80, 80, 80, 80])

      // 更新调试信息
      if (debugLogs) {
        this.debugInfo = debugLogs.join('\n')
      }
    }
  },
  computed: {
    currentQuiz() {
      return this.quizzes[this.currentQuestionIndex]
    },
    correctCount() {
      return this.quizzes.filter(q => q.selected === q.correct).length
    },
    quizScore() {
      return Math.round((this.correctCount / this.quizzes.length) * 100)
    },
    navigationUrl() {
      if (this.nearestPoliceStation && this.currentPosition) {
        const start = `${this.currentPosition[0]},${this.currentPosition[1]}`
        const end = `${this.nearestPoliceStation.location.lng},${this.nearestPoliceStation.location.lat}`
        return `https://uri.amap.com/navigation?from=${start}&to=${end}&mode=car&policy=1`
      }
      return '#'
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.main-container {
  position: relative;
  z-index: 1;
  padding-top: 120px;
  max-width: 1400px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 40px 20px 30px 20px;
  position: relative;
  background: linear-gradient(135deg, #f5f9ff 0%, #e3f2fd 100%);
  margin: 0 20px 30px 20px;
  border-radius: 16px;
}

.hero-title {
  font-size: 2rem;
  color: #0064b2;
  margin-bottom: 12px;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 1rem;
  color: #666;
  font-weight: 600;
}

.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding: 0 20px;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0, 100, 178, 0.08);
  border: 1px solid #e3f2fd;
}

.card-title {
  font-size: 1.2rem;
  color: #0064b2;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.card-icon {
  font-size: 1.5rem;
}

.warning-box {
  background: #f5f9ff;
  border-left: 4px solid #0064b2;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
}

.warning-title {
  font-size: 1rem;
  color: #0064b2;
  margin-bottom: 8px;
  font-weight: 600;
}

.warning-text {
  color: #666;
  line-height: 1.6;
  font-size: 0.95rem;
}

.fraud-type-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 16px;
}

.fraud-type-card {
  background: #f5f9ff;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  border: 1px solid #e3f2fd;
}

.fraud-type-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.fraud-type-title {
  font-size: 1rem;
  color: #0064b2;
  margin-bottom: 8px;
  font-weight: 600;
}

.fraud-type-desc {
  color: #666;
  font-size: 0.85rem;
  line-height: 1.5;
}

.tips-list {
  list-style: none;
  padding: 0;
}

.tips-item {
  background: #f5f9ff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  border-left: 4px solid #0064b2;
}

.tips-number {
  background: #0064b2;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.tips-content h4 {
  color: #0064b2;
  font-size: 1rem;
  margin-bottom: 4px;
  font-weight: 600;
}

.tips-content p {
  color: #555;
  line-height: 1.5;
  font-size: 0.9rem;
}

.case-card {
  background: #f5f9ff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid #e3f2fd;
  position: relative;
}

.case-badge {
  position: absolute;
  top: -8px;
  right: 12px;
  background: #0064b2;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.case-title {
  font-size: 1rem;
  color: #0064b2;
  margin-bottom: 10px;
  padding-right: 70px;
  font-weight: 600;
}

.case-content {
  color: #555;
  line-height: 1.6;
  font-size: 0.9rem;
}

.case-highlight {
  background: #e3f2fd;
  padding: 12px;
  border-radius: 6px;
  margin-top: 12px;
  border-left: 3px solid #0064b2;
  font-size: 0.85rem;
}

.quiz-btn-container {
  text-align: center;
  padding: 30px 20px;
}

.quiz-start-btn {
  background: #0064b2;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 16px 40px;
  font-size: 1.1rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 100, 178, 0.2);
  font-weight: 600;
}

.quiz-start-btn:hover {
  background: #0055a0;
}

.quiz-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.quiz-modal {
  background: white;
  border-radius: 12px;
  padding: 30px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.quiz-modal-title {
  font-size: 1.5rem;
  color: #0064b2;
  text-align: center;
  margin-bottom: 20px;
  font-weight: 600;
}

.quiz-close-btn {
  position: absolute;
  top: 15px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.quiz-close-btn:hover {
  color: #333;
}

.quiz-question-box {
  background: #f5f9ff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.quiz-question-num {
  font-size: 1rem;
  color: #0064b2;
  margin-bottom: 12px;
  font-weight: 600;
}

.quiz-question-text {
  font-size: 1rem;
  color: #333;
  line-height: 1.6;
}

.quiz-options-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.quiz-option-btn {
  background: white;
  border: 2px solid #e3f2fd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  text-align: center;
  font-size: 0.95rem;
  color: #333;
  transition: all 0.2s ease;
}

.quiz-option-btn.selected {
  border-color: #0064b2;
  background: #e3f2fd;
}

.quiz-option-btn.correct {
  background: #e8f5e9;
  border-color: #4caf50;
}

.quiz-option-btn.wrong {
  background: #ffebee;
  border-color: #f44336;
}

.quiz-explanation {
  margin-top: 15px;
  padding: 15px;
  background: #fff8e1;
  border-radius: 8px;
  border-left: 4px solid #ff9800;
  font-size: 0.9rem;
  line-height: 1.6;
}

.quiz-nav-btns {
  display: flex;
  justify-content: space-between;
  margin-top: 25px;
}

.quiz-nav-btn {
  background: #0064b2;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 24px;
  font-size: 0.95rem;
  cursor: pointer;
  font-weight: 600;
}

.quiz-nav-btn:disabled {
  background: #e0e0e0;
  cursor: not-allowed;
}

.quiz-result-box {
  text-align: center;
  padding: 30px;
}

.quiz-score {
  font-size: 3.5rem;
  color: #0064b2;
  margin-bottom: 20px;
  font-weight: 700;
}

.quiz-result-text {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 25px;
}

.quiz-restart-btn {
  background: #0064b2;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 12px 32px;
  font-size: 1.1rem;
  cursor: pointer;
  font-weight: 600;
}

.emergency-section {
  background: #f5f9ff;
  border-radius: 12px;
  padding: 24px;
  margin: 20px;
  text-align: center;
  border: 1px solid #e3f2fd;
}

.emergency-title {
  font-size: 1.2rem;
  color: #0064b2;
  margin-bottom: 15px;
  font-weight: 600;
}

.emergency-phone {
  font-size: 2rem;
  font-weight: bold;
  color: #0064b2;
  font-family: 'Nunito', sans-serif;
}

.emergency-desc {
  color: #666;
  margin-top: 8px;
  font-size: 0.9rem;
}

.full-width {
  grid-column: 1 / -1;
}

/* 紧急求助弹窗样式 */
.emergency-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.emergency-modal {
  background: white;
  border-radius: 12px;
  width: 95%;
  max-width: 900px;
  max-height: 95vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.emergency-close-btn {
  position: absolute;
  top: 15px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  z-index: 100;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.emergency-close-btn:hover {
  background: #f0f0f0;
  color: #333;
}

.emergency-content {
  padding: 30px;
}

.map-section {
  background: #f5f9ff;
  padding: 25px;
  border-radius: 12px;
}

.section-title {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.section-title i {
  color: #0064b2;
}

.amap-container {
  width: 100%;
  height: 400px;
  background: #e3f2fd;
  border-radius: 8px;
  position: relative;
  margin-bottom: 20px;
  overflow: hidden;
}

.map-loading,
.map-error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #666;
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.map-loading i,
.map-error i {
  font-size: 2rem;
  margin-bottom: 15px;
  display: block;
  color: #0064b2;
}

.map-error i {
  color: #f44336;
}

.retry-btn {
  margin-top: 15px;
  padding: 10px 25px;
  background: #0064b2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
}

.police-station-info {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border-left: 5px solid #0064b2;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.station-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.station-address {
  font-size: 1rem;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.5;
}

.station-distance {
  font-size: 1rem;
  color: #0064b2;
  font-weight: bold;
  margin-bottom: 15px;
}

.navigate-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #0064b2;
  color: white;
  padding: 10px 24px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.navigate-btn:hover {
  background: #0055a0;
}

.no-station-info {
  text-align: center;
  padding: 20px;
  color: #666;
  background: #f5f9ff;
  border-radius: 8px;
  border-left: 4px solid #ff9800;
}

.debug-info {
  margin-top: 15px;
  padding: 15px;
  background: #263238;
  border-radius: 8px;
  color: #aed581;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
}

.debug-title {
  color: #ffcc80;
  font-weight: bold;
  margin-bottom: 10px;
  font-size: 14px;
}

.debug-info pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 200px;
  overflow-y: auto;
}

.items-list {
  list-style: none;
  padding: 0;
}

.items-list .item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f5f9ff;
  border-radius: 8px;
  margin-bottom: 10px;
}

.item-icon {
  font-size: 1.5rem;
}

.item-content {
  flex: 1;
}

.item-content strong {
  display: block;
  color: #333;
  margin-bottom: 3px;
}

.item-content span {
  font-size: 0.85rem;
  color: #666;
}

.emergency-tips {
  background: #f5f9ff;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #0064b2;
}

.tips-title {
  font-weight: bold;
  color: #0064b2;
  margin-bottom: 10px;
  font-size: 1rem;
}

.emergency-tips p {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
  line-height: 1.5;
}

@media (max-width: 900px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 1.8rem;
  }

  .fraud-type-grid {
    grid-template-columns: 1fr;
  }

  .quiz-options-box {
    grid-template-columns: 1fr;
  }
}
</style>