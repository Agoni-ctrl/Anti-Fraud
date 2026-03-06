<template>
  <div class="home-page">
    <!-- 背景色块装饰 - 蓝白色调（增强版） -->
    <div class="bg-block block-1"></div>
    <div class="bg-block block-2"></div>
    <div class="bg-block block-3"></div>
    <div class="bg-block block-4"></div>
    <div class="bg-block block-5"></div>
    
    <!-- 新增小色块 -->
    <div class="bg-block-small small-1"></div>
    <div class="bg-block-small small-2"></div>
    <div class="bg-block-small small-3"></div>
    <div class="bg-block-small small-4"></div>
    <div class="bg-block-small small-5"></div>
    <div class="bg-block-small small-6"></div>
    <div class="bg-block-small small-7"></div>
    <div class="bg-block-small small-8"></div>
    
    <main class="home-main">
      <!-- 英雄区 + 动态Logo轮播 -->
      <section class="hero-split-section">
        <!-- 左侧：固定文案区（文字加大，稍微靠左） -->
        <div class="hero-content">
          <h1 class="hero-title">
            <span class="title-line">慧眼识骗</span><br />
            <span class="title-line gradient-text">智护万家</span>
          </h1>
          <p class="hero-subtitle">AI反诈守护系统 · 让欺骗无处遁形</p>
          <p class="hero-description">
            基于深度学习的多模态反诈平台，实时识别AI换脸、钓鱼链接、
            诈骗话术，为您和家人的数字生活保驾护航。
          </p>
          <div class="hero-cta">
            <button class="btn btn-primary" @click="exploreFeatures">
              <span>开始使用</span>
              <i class="fas fa-arrow-right"></i>
            </button>
            <button class="btn btn-secondary" @click="handleEmergency">
              <i class="fas fa-exclamation-triangle"></i>
              <span>紧急求助 96110</span>
            </button>
          </div>
          <div class="hero-badges">
            <span class="badge-item">🗃️ 支持多种文件</span>
            <span class="badge-item">🔒 数据安全</span>
            <span class="badge-item">📖 反诈知识库</span>
          </div>
        </div>

        <!-- 右侧：Lottie动画Logo轮播区 -->
        <div class="hero-logo">
          <!-- Lottie动画容器 -->
          <div class="logo-carousel">
            <div
              v-for="(item, index) in logoList"
              :key="item.id"
              class="logo-slide"
              :class="{ active: currentLogoIndex === index }"
              :ref="'lottieContainer_' + index"
            ></div>
          </div>

          <!-- 文字说明区 -->
          <div class="logo-caption">
            <p class="caption-main">{{ currentCaption.main }}</p>
            <p class="caption-sub">
              <i class="fas fa-shield-alt"></i>
              <span>{{ currentCaption.sub }}</span>
            </p>
          </div>

          <!-- 指示点 -->
          <div class="logo-indicators">
            <span
              v-for="(item, idx) in logoList"
              :key="'dot-' + idx"
              class="indicator-dot"
              :class="{ active: currentLogoIndex === idx }"
              @click="setLogoIndex(idx)"
            ></span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import lottie from 'lottie-web'

// 导入所有Lottie动画JSON文件
import magnifierAnimation from '../assets/animations/page-not-found.json'
import chattingAnimation from '../assets/animations/chatting.json'
import dataLossAnimation from '../assets/animations/data loss prevention.json'
import timeAnimation from '../assets/animations/time.json'

export default {
  name: "HomePage",
  data() {
    return {
      // Logo列表 - 使用不同的Lottie动画文件
      logoList: [
        {
          id: 1,
          name: "深度伪造检测",
          animationData: magnifierAnimation,
          mainCaption: "深度伪造检测",
          subCaption: "AI换脸 / 声音合成 实时鉴别",
        },
        {
          id: 2,
          name: "诈骗话术识别",
          animationData: chattingAnimation,
          mainCaption: "诈骗话术识别",
          subCaption: "聊天内容实时分析 / 诈骗模式预警",
        },
        {
          id: 3,
          name: "隐私数据保护",
          animationData: dataLossAnimation,
          mainCaption: "隐私数据保护",
          subCaption: "敏感信息加密 / 防数据泄露",
        },
        {
          id: 4,
          name: "风险时效预警",
          animationData: timeAnimation,
          mainCaption: "风险时效预警",
          subCaption: "诈骗时段分析 / 紧急提醒",
        }
      ],
      currentLogoIndex: 0,
      intervalTimer: null,
      lottieAnimations: [],
    };
  },
  computed: {
    // 根据当前索引获取对应的说明文字
    currentCaption() {
      const item = this.logoList[this.currentLogoIndex] || this.logoList[0];
      return {
        main: item.mainCaption,
        sub: item.subCaption,
      };
    },
  },
  mounted() {
    // 初始化所有Lottie动画
    this.initLottieAnimations();
    
    // 启动轮播 - 5秒切换一次
    this.startCarousel();
  },
  beforeDestroy() {
    // 清除定时器
    if (this.intervalTimer) {
      clearInterval(this.intervalTimer);
    }
    
    // 销毁所有Lottie动画实例
    this.lottieAnimations.forEach(animation => {
      if (animation) {
        animation.destroy();
      }
    });
  },
  methods: {
    // 初始化所有Lottie动画
    initLottieAnimations() {
      this.$nextTick(() => {
        this.logoList.forEach((item, index) => {
          const containerRef = this.$refs[`lottieContainer_${index}`];
          if (containerRef && containerRef[0]) {
            try {
              const animation = lottie.loadAnimation({
                container: containerRef[0],
                renderer: 'svg',
                loop: true,
                autoplay: true,
                animationData: item.animationData
              });
              
              this.lottieAnimations.push(animation);
            } catch (error) {
              console.error(`Lottie动画加载失败 (${item.name}):`, error);
            }
          }
        });
      });
    },
    
    // 开始自动轮播 - 5秒切换
    startCarousel() {
      this.intervalTimer = setInterval(() => {
        this.currentLogoIndex = (this.currentLogoIndex + 1) % this.logoList.length;
      }, 5000);
    },
    
    // 手动切换到指定logo
    setLogoIndex(index) {
      this.currentLogoIndex = index;
      if (this.intervalTimer) {
        clearInterval(this.intervalTimer);
        this.startCarousel();
      }
    },
    
    // 按钮方法
    exploreFeatures() {
      alert("请使用上方导航栏选择具体功能");
    },
    handleEmergency() {
      alert("紧急求助通道已开启，请保持冷静，我们将立即联系您");
    },
  },
};
</script>

<style scoped>
/* ===== 整体页面 ===== */
.home-page {
  min-height: 100vh;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
  position: relative;
  overflow: hidden;
  background: linear-gradient(145deg, #f0f8ff 0%, #e1edfa 100%);
  display: flex;
  flex-direction: column;
}

/* ===== 蓝白色块背景装饰（大色块） ===== */
.bg-block {
  position: absolute;
  border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
  z-index: 0;
  opacity: 0.5;
}

.block-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #4299ff 0%, #7abfff 100%);
  top: -50px;
  left: -100px;
  animation: floatBlock 18s ease-in-out infinite alternate;
}

.block-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(225deg, #3182ce 0%, #63b3ed 100%);
  bottom: 50px;
  right: -50px;
  animation: floatBlock 15s ease-in-out infinite alternate-reverse;
}

.block-3 {
  width: 250px;
  height: 250px;
  background: linear-gradient(45deg, #2c5282 0%, #4299ff 100%);
  top: 30%;
  left: 15%;
  animation: floatBlock 20s ease-in-out infinite alternate;
  opacity: 0.3;
}

.block-4 {
  width: 350px;
  height: 350px;
  background: linear-gradient(180deg, #90cdf4 0%, #bee3f8 100%);
  bottom: 5%;
  left: 5%;
  animation: floatBlock 22s ease-in-out infinite alternate-reverse;
  opacity: 0.4;
}

.block-5 {
  width: 200px;
  height: 200px;
  background: linear-gradient(90deg, #1a4b7a 0%, #2a69ac 100%);
  top: 15%;
  right: 10%;
  animation: floatBlock 16s ease-in-out infinite alternate;
  opacity: 0.25;
}

/* ===== 新增小色块 ===== */
.bg-block-small {
  position: absolute;
  border-radius: 30% 70% 50% 50% / 30% 40% 60% 70%;
  z-index: 0;
  opacity: 0.3;
  animation: floatSmall 12s ease-in-out infinite alternate;
}

.small-1 {
  width: 80px;
  height: 80px;
  background: linear-gradient(145deg, #63b3ed, #90cdf4);
  top: 15%;
  left: 25%;
  animation-delay: 0s;
}

.small-2 {
  width: 60px;
  height: 60px;
  background: linear-gradient(225deg, #3182ce, #63b3ed);
  bottom: 20%;
  right: 15%;
  animation-delay: 1s;
  opacity: 0.4;
}

.small-3 {
  width: 40px;
  height: 40px;
  background: linear-gradient(90deg, #2c5282, #4299ff);
  top: 60%;
  left: 30%;
  animation-delay: 2s;
  opacity: 0.5;
}

.small-4 {
  width: 100px;
  height: 100px;
  background: linear-gradient(180deg, #7abfff, #bee3f8);
  top: 10%;
  right: 25%;
  animation-delay: 3s;
  opacity: 0.25;
}

.small-5 {
  width: 50px;
  height: 50px;
  background: linear-gradient(45deg, #1a4b7a, #3182ce);
  bottom: 30%;
  left: 20%;
  animation-delay: 4s;
  opacity: 0.35;
}

.small-6 {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #4299ff, #90cdf4);
  top: 40%;
  right: 30%;
  animation-delay: 5s;
  opacity: 0.3;
}

.small-7 {
  width: 45px;
  height: 45px;
  background: linear-gradient(225deg, #2c5282, #63b3ed);
  bottom: 15%;
  left: 40%;
  animation-delay: 6s;
  opacity: 0.4;
}

.small-8 {
  width: 90px;
  height: 90px;
  background: linear-gradient(90deg, #3182ce, #7abfff);
  top: 70%;
  right: 20%;
  animation-delay: 7s;
  opacity: 0.25;
}

@keyframes floatBlock {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
  }
  100% {
    transform: translate(80px, 60px) rotate(15deg) scale(1.1);
  }
}

@keyframes floatSmall {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
  }
  100% {
    transform: translate(40px, 30px) rotate(30deg) scale(1.2);
  }
}

/* ===== 主内容 ===== */
.home-main {
  flex: 1;
  max-width: 1300px;
  width: 100%;
  margin: 0 auto;
  padding: 0.2rem 1.5rem;
  position: relative;
  z-index: 5;
  display: flex;
  align-items: flex-start;
  padding-top: 0;
  margin-top: -10px;
}

/* ===== Hero区域 ===== */
.hero-split-section {
  display: grid;
  grid-template-columns: 1.3fr 1fr; /* 进一步加大左侧比例，从1.2fr增加到1.3fr */
  gap: 0.8rem; /* 进一步减小间隙，从1rem减到0.8rem */
  align-items: center;
  width: 100%;
  margin-left: 2%; /* 减小整体右移幅度，从5%减到2% */
}

/* ===== 左侧文案（文字加大，稍微靠左） ===== */
.hero-content {
  display: flex;
  flex-direction: column;
  max-width: 650px; /* 增加最大宽度，从600px增加到650px */
  margin-left: 8%; /* 减小左边距，从15%减到8%，让文案靠左 */
  position: relative;
  left: 10px; /* 减小向右偏移，从20px减到10px */
}

.hero-title {
  font-size: 4rem; /* 从3.5rem加大到4rem */
  font-weight: 800;
  line-height: 1.1; /* 减小行高使更紧凑 */
  margin-bottom: 0.5rem;
  color: #113946;
  letter-spacing: -0.02em;
}

.gradient-text {
  background: linear-gradient(145deg, #1e4a7a, #4299ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.hero-subtitle {
  font-size: 1.3rem; /* 从1.15rem加大到1.3rem */
  font-weight: 500;
  color: #2c5f7b;
  margin-bottom: 0.4rem;
}

.hero-description {
  font-size: 1.15rem; /* 从1.05rem加大到1.15rem */
  color: #3e6b8c;
  line-height: 1.5;
  margin-bottom: 1.2rem;
  max-width: 550px; /* 增加最大宽度，从520px增加到550px */
}

/* ===== 按钮 ===== */
.hero-cta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.2rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.8rem 2.2rem; /* 从0.75rem 2rem加大到0.8rem 2.2rem */
  border-radius: 60px;
  font-size: 1.05rem; /* 从1rem加大到1.05rem */
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  box-shadow: 0 4px 10px rgba(0, 80, 120, 0.15);
}

.btn-primary {
  background: linear-gradient(135deg, #3182ce, #63b3ed);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 25px rgba(49, 130, 206, 0.3);
}

.btn-secondary {
  background: white;
  color: #1a587d;
  border: 1px solid #cae0f0;
}

/* ===== 标签 ===== */
.hero-badges {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.badge-item {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(2px);
  padding: 0.4rem 1.2rem; /* 从0.35rem 1.1rem加大到0.4rem 1.2rem */
  border-radius: 60px;
  font-size: 0.95rem; /* 从0.9rem加大到0.95rem */
  color: #1d618b;
  border: 1px solid #d2e6ff;
  transition: 0.2s;
}

/* ===== 右侧Logo轮播区 ===== */
.hero-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin-right: 3%; /* 减小右边距，从5%减到3% */
}

/* Logo轮播容器 */
.logo-carousel {
  position: relative;
  width: 100%;
  max-width: 420px; /* 从440px减到420px，进一步让右侧变小 */
  min-height: 400px; /* 从420px减到400px */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 每个logo滑动项 */
.logo-slide {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.6s ease-in-out;
  pointer-events: none;
}

.logo-slide.active {
  opacity: 1;
  pointer-events: auto;
}

/* Lottie动画容器样式 */
.logo-slide > div {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-slide svg {
  width: 100%;
  height: auto;
  max-width: 360px; /* 从380px减到360px */
}

/* 文字说明区 */
.logo-caption {
  margin-top: 0.2rem;
  text-align: center;
  min-height: 60px;
}

.caption-main {
  font-size: 1.2rem; /* 从1.25rem稍微减小到1.2rem，与放大的左侧形成对比 */
  font-weight: 600;
  margin-bottom: 0.15rem;
  background: linear-gradient(145deg, #1e4a7a, #3182ce);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.caption-sub {
  font-size: 0.88rem; /* 稍微减小 */
  color: #3e6b8c;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.caption-sub i {
  color: #4299ff;
  font-size: 0.85rem;
}

/* 指示点 */
.logo-indicators {
  display: flex;
  gap: 8px;
  margin-top: 6px;
  justify-content: center;
}

.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 8px;
  background: #bdd9f0;
  transition: all 0.3s;
  cursor: pointer;
}

.indicator-dot.active {
  width: 20px;
  background: #3182ce;
}

/* ===== 响应式 ===== */
@media (max-width: 1000px) {
  .hero-split-section {
    grid-template-columns: 1fr;
    gap: 0.8rem;
    margin-left: 0;
  }

  .hero-content {
    max-width: 100%;
    margin-left: 0;
    left: 0;
  }

  .logo-carousel {
    min-height: 380px;
  }
  
  .hero-title {
    font-size: 3.2rem; /* 移动端适当减小 */
  }
  
  .hero-logo {
    margin-right: 0;
  }
}
</style>