<template>
  <div class="elder-guard-page">

    <div class="main-container">
      <section class="hero-section">
        <h1 class="hero-title">银发守护</h1>
        <p class="hero-subtitle">守护老年群体财产安全，让诈骗无处遁形</p>
      </section>

      <div class="two-column-layout">
        <div class="content-card">
          <h2 class="card-title">
            <span class="card-icon">⚠️</span>
            老年人高发诈骗类型
          </h2>

          <div class="warning-box">
            <h3 class="warning-title">诈骗分子专盯老年人</h3>
            <p class="warning-text">
              诈骗分子利用老年人信息闭塞、情感孤独、渴望健康等特点，精心设计骗局。
              <strong style="color: #0064b2;">记住：凡是要求转账汇款的，都要提高警惕！</strong>
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
            防范技巧，守护养老钱
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
            <span v-if="quizScore === 100">🎉 太棒了！满分！您是防骗达人！</span>
            <span v-else-if="quizScore >= 66">👍 不错！继续保持警惕！</span>
            <span v-else>💪 还需努力，多学习防骗知识哦！</span>
          </div>
          <p style="color: #666; margin-bottom: 20px;">共 {{ quizzes.length }} 题，答对 {{ correctCount }} 题</p>
          <button class="quiz-restart-btn" @click="restartQuiz">再测一次</button>
        </div>
      </div>
    </div>

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
  name: 'ElderGuard',
  data() {
    return {
      fraudTypes: [
        { icon: '📞', title: '冒充公检法诈骗', desc: '冒充公安、检察院、法院，以涉嫌犯罪为由要求转账' },
        { icon: '💊', title: '保健品诈骗', desc: '夸大保健品功效，以免费体验为诱饵骗取钱财' },
        { icon: '🏠', title: '养老投资诈骗', desc: '以高回报养老项目为诱饵，骗取养老钱' },
        { icon: '👨‍👩‍👧', title: '冒充亲友诈骗', desc: '冒充子女、亲友，以急事为由要求汇款' }
      ],
      preventionTips: [
        { title: '不轻信陌生电话', content: '公检法不会电话办案，遇到可疑电话立即挂断。' },
        { title: '不透露个人信息', content: '身份证号、银行卡号、验证码等重要信息绝不外泄。' },
        { title: '不随意点击链接', content: '不明链接、二维码不要点击，防止木马病毒。' },
        { title: '不贪图小便宜', content: '免费礼品、高额回报往往是诈骗诱饵。' },
        { title: '多与家人沟通', content: '遇到可疑情况及时与子女、亲友商量。' },
        { title: '安装反诈APP', content: '下载国家反诈中心APP，开启来电预警功能。' }
      ],
      realCases: [
        {
          title: '案例一："涉嫌洗钱"的恐吓',
          content: '张大爷接到自称"检察院"电话，称其涉嫌洗钱，要求将资金转入"安全账户"配合调查。张大爷被恐吓后，将20万元养老钱转入对方账户。',
          warning: '公检法不会要求转账汇款，更没有"安全账户"！'
        },
        {
          title: '案例二："免费体检"的陷阱',
          content: '李大妈参加社区"免费体检"活动，被查出"严重疾病"。对方推荐"特效药"，声称能根治。李大妈花费8万元购买后，发现只是普通保健品。',
          warning: '生病要去正规医院，不要轻信免费体检和特效药。'
        },
        {
          title: '案例三："养老公寓"的投资',
          content: '王大爷看到"养老公寓"投资广告，承诺年化收益15%，还提供免费入住。王大爷投入15万元后，对方失联，项目根本不存在。',
          warning: '高回报必有高风险，养老投资要选择正规渠道。'
        },
        {
          title: '案例四："孙子出事"的急电',
          content: '赵奶奶接到"孙子"电话，说在外地打架被抓，需要5万元保释金。赵奶奶救孙心切，汇款后发现孙子安然在家。',
          warning: '接到亲友急事电话，一定要先核实身份，不要盲目汇款。'
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
      quizzes: [
        {
          question: '接到自称"公安局"的电话，说你涉嫌犯罪，要求转账到"安全账户"，你应该？',
          options: ['立即配合转账', '按照要求提供银行卡信息', '挂断电话，拨打110核实', '先转账再报警'],
          correct: 2,
          selected: null,
          answered: false,
          explanation: '公检法不会电话办案，更不会要求转账到"安全账户"！遇到此类电话立即挂断并拨打110核实。'
        },
        {
          question: '有人打电话说你的孙子在外地出事了，急需用钱，你应该？',
          options: ['立即汇款救急', '先打电话给孙子核实', '按照对方要求转账', '向邻居借钱'],
          correct: 1,
          selected: null,
          answered: false,
          explanation: '遇到亲友急事电话，一定要先通过其他方式核实身份，不要盲目汇款。'
        },
        {
          question: '看到"免费体检、赠送礼品"的活动，正确的做法是？',
          options: ['积极参加，免费领取', '填写个人信息参与', '警惕这是骗局，不参与', '推荐给其他老人'],
          correct: 2,
          selected: null,
          answered: false,
          explanation: '免费体检、赠送礼品往往是诈骗诱饵，目的是骗取个人信息或推销高价保健品。'
        },
        {
          question: '有人推荐"养老公寓投资项目"，承诺年化收益15%，你应该？',
          options: ['立即投资', '先了解项目详情', '高回报必有高风险，谨慎对待', '借钱投资'],
          correct: 2,
          selected: null,
          answered: false,
          explanation: '高回报必有高风险，养老投资要选择正规渠道，不要轻信高回报承诺。'
        }
      ]
    }
  },
  computed: {
    currentQuiz() {
      return this.quizzes[this.currentQuestionIndex]
    },
    quizScore() {
      const correctCount = this.quizzes.filter(q => q.answered && q.selected === q.correct).length
      return Math.round((correctCount / this.quizzes.length) * 100)
    },
    correctCount() {
      return this.quizzes.filter(q => q.answered && q.selected === q.correct).length
    },
    navigationUrl() {
      if (this.nearestPoliceStation && this.currentPosition) {
        const [lng, lat] = this.currentPosition
        return `https://uri.amap.com/navigation?to=${this.nearestPoliceStation.name},${lng},${lat}&mode=car&policy=1&coordinate=gaode&callnative=1`
      }
      return '#'
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
            this.currentPosition = [116.397428, 39.90923]
            this.loadMap(116.397428, 39.90923)
          },
          { enableHighAccuracy: true, timeout: 10000 }
        )
      } else {
        this.currentPosition = [116.397428, 39.90923]
        this.loadMap(116.397428, 39.90923)
      }
    },
    loadMap(lng, lat) {
      try {
        this.map = new AMap.Map(this.$refs.amapContainer, {
          zoom: 15,
          center: [lng, lat],
          viewMode: '2D'
        })

        AMap.plugin(['AMap.PlaceSearch', 'AMap.Geolocation', 'AMap.Marker'], () => {
          const geolocation = new AMap.Geolocation({
            enableHighAccuracy: true,
            timeout: 10000
          })

          geolocation.getCurrentPosition((status, result) => {
            if (status === 'complete') {
              const position = [result.position.lng, result.position.lat]
              this.currentPosition = position
              this.map.setCenter(position)

              const marker = new AMap.Marker({
                position: position,
                icon: new AMap.Icon({
                  size: new AMap.Size(20, 20),
                  image: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMTAiIGN5PSIxMCIgcj0iMTAiIGZpbGw9IiMwMDY0YjIiLz48L3N2Zz4=',
                  imageSize: new AMap.Size(20, 20)
                })
              })
              this.map.addControl(marker)

              const placeSearch = new AMap.PlaceSearch({
                type: '派出所',
                pageSize: 5,
                pageIndex: 1,
                extensions: 'all'
              })

              placeSearch.searchNearBy('公安局', position, 3000, (status, result) => {
                if (status === 'complete' && result.poiList && result.poiList.pois.length > 0) {
                  const nearestStation = result.poiList.pois[0]
                  this.nearestPoliceStation = {
                    name: nearestStation.name,
                    address: nearestStation.address,
                    distance: Math.round(nearestStation.distance)
                  }

                  const stationMarker = new AMap.Marker({
                    position: [nearestStation.location.lng, nearestStation.location.lat],
                    icon: new AMap.Icon({
                      size: new AMap.Size(32, 32),
                      image: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTQiIGZpbGw9IiNmZmYwMDAiIHN0cm9rZT0iIzAwNDRiMiIgc3Ryb2tlLXdpZHRoPSIyIi8+PC9zdmc+',
                      imageSize: new AMap.Size(32, 32)
                    })
                  })
                  this.map.addControl(stationMarker)

                  this.map.setFitView([marker, stationMarker], false, [60, 60, 60, 60])
                  this.mapLoaded = true
                } else {
                  this.mapLoaded = true
                }
              })
            } else {
              this.mapLoaded = true
            }
          })
        })
      } catch (error) {
        console.error('地图加载失败:', error)
        this.mapError = '地图加载失败，请检查网络连接'
      }
    }
  }
}
</script>

<style scoped>
.elder-guard-page {
  min-height: 100vh;
  background: #ffffff;
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

.emergency-section {
  margin-bottom: 30px;
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