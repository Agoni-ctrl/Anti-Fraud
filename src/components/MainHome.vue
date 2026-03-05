<template>
  <div class="home-page">
    <main class="home-main">
      <!-- ===== 融合英雄区 + 双栏轮播区 ===== -->
      <section class="hero-split-section">
        <!-- 左侧：固定文案区 -->
        <div class="hero-content">
          <h1 class="hero-title">
            <span class="title-line">慧眼识骗</span>
            <span class="title-line gradient-text">智护万家</span>
          </h1>
          <p class="hero-subtitle">AI反诈守护系统 · 让欺骗无处遁形</p>
          <p class="hero-description">
            基于深度学习的多模态反诈平台，实时识别AI换脸、钓鱼链接、诈骗话术，
            为您和家人的数字生活保驾护航。
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
            <span class="badge-item">🏆 公安部推荐</span>
            <span class="badge-item">🔒 数据加密</span>
            <span class="badge-item">⚡ 毫秒级响应</span>
          </div>
        </div>

        <!-- 右侧：轮播图片区 (每隔几秒自动切换，悬停显示透明介绍) -->
        <div class="hero-carousel">
          <div class="carousel-container">
            <!-- 轮播图片 -->
            <div
              class="carousel-track"
              :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
            >
              <div
                v-for="(slide, index) in carouselSlides"
                :key="index"
                class="carousel-slide"
                @mouseenter="activeHoverSlide = index"
                @mouseleave="activeHoverSlide = null"
              >
                <!-- 图片部分 (使用emoji和渐变模拟，实际可替换为真实图片) -->
                <div class="slide-image" :style="{ background: slide.bgGradient }">
                  <!-- 实际项目中这里可以用 <img> 替换 -->
                  <span class="slide-emoji">{{ slide.emoji }}</span>
                </div>

                <!-- 鼠标悬停时显示的透明介绍版块 -->
                <div
                  class="slide-hover-overlay"
                  v-show="activeHoverSlide === index"
                >
                  <div class="hover-content">
                    <h4 class="hover-title">{{ slide.title }}</h4>
                    <p class="hover-desc">{{ slide.description }}</p>
                    <span class="hover-tag">{{ slide.tag }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 轮播控制按钮 -->
            <button class="carousel-btn prev" @click="prevSlide" :disabled="isTransitioning">←</button>
            <button class="carousel-btn next" @click="nextSlide" :disabled="isTransitioning">→</button>

            <!-- 轮播指示点 -->
            <div class="carousel-dots">
              <span
                v-for="(_, index) in carouselSlides"
                :key="index"
                class="dot"
                :class="{ active: currentSlide === index }"
                @click="goToSlide(index)"
              ></span>
            </div>
          </div>
        </div>
      </section>

      <!-- ===== 简洁的品牌理念区 (替代原来的双栏区，极简) ===== -->
      <section class="mission-section">
        <div class="mission-quote">
          <span class="quote-mark">"</span>
          <p class="mission-text">
            在这个AI生成内容日益泛滥的时代，<br>
            我们坚信每个人都有权利看清真相。
          </p>
        </div>
        <div class="mission-badges">
          <span class="badge-light">AI深度伪造检测</span>
          <span class="badge-light">实时诈骗预警</span>
          <span class="badge-light">96110专线接入</span>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      currentSlide: 0,
      activeHoverSlide: null,
      isTransitioning: false,
      autoPlayTimer: null,
      carouselSlides: [
        {
          img,
          title: 'AI换脸诈骗',
          description: '骗子利用AI技术换脸、合成视频，冒充亲友或领导要求转账。',
          tag: '#新型骗局',
          bgGradient: 'linear-gradient(145deg, #f0f5ff, #ffffff)'
        },
        {
          emoji: '⚖️',
          title: '冒充公检法',
          description: '谎称涉嫌洗钱、犯罪，要求将资金转入“安全账户”配合调查。',
          tag: '#高发类型',
          bgGradient: 'linear-gradient(145deg, #faf0ff, #ffffff)'
        },
        {
          emoji: '💘',
          title: '杀猪盘',
          description: '通过社交平台建立感情，诱导投资、赌博或借钱。',
          tag: '#情感陷阱',
          bgGradient: 'linear-gradient(145deg, #fff0f5, #ffffff)'
        },
        {
          emoji: '📞',
          title: '冒充客服退款',
          description: '谎称商品质量问题要退款，诱导点击钓鱼链接或提供验证码。',
          tag: '#网购诈骗',
          bgGradient: 'linear-gradient(145deg, #f0faf5, #ffffff)'
        }
      ]
    };
  },
  mounted() {
    this.startAutoPlay();
  },
  beforeUnmount() {
    this.stopAutoPlay();
  },
  methods: {
    nextSlide() {
      if (this.isTransitioning) return;
      this.isTransitioning = true;
      this.currentSlide = (this.currentSlide + 1) % this.carouselSlides.length;
      setTimeout(() => {
        this.isTransitioning = false;
      }, 500);
      this.resetAutoPlay();
    },
    prevSlide() {
      if (this.isTransitioning) return;
      this.isTransitioning = true;
      this.currentSlide = (this.currentSlide - 1 + this.carouselSlides.length) % this.carouselSlides.length;
      setTimeout(() => {
        this.isTransitioning = false;
      }, 500);
      this.resetAutoPlay();
    },
    goToSlide(index) {
      if (this.isTransitioning || index === this.currentSlide) return;
      this.isTransitioning = true;
      this.currentSlide = index;
      setTimeout(() => {
        this.isTransitioning = false;
      }, 500);
      this.resetAutoPlay();
    },
    startAutoPlay() {
      this.autoPlayTimer = setInterval(() => {
        if (!this.isTransitioning) {
          this.currentSlide = (this.currentSlide + 1) % this.carouselSlides.length;
        }
      }, 5000); // 每5秒切换
    },
    stopAutoPlay() {
      if (this.autoPlayTimer) {
        clearInterval(this.autoPlayTimer);
      }
    },
    resetAutoPlay() {
      this.stopAutoPlay();
      this.startAutoPlay();
    },
    exploreFeatures() {
      alert('请使用上方导航栏选择具体功能');
    },
    handleEmergency() {
      alert('紧急求助通道已开启，请保持冷静，我们将立即联系您');
    }
  }
};
</script>

<style scoped>
/* ===== 全局样式 - 纯浅色系 ===== */
.home-page {
  min-height: 100vh;
  background: #fafcff; /* 极浅的蓝白背景 */
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.home-main {
  max-width: 1300px;
  margin: 0 auto;
  padding: 2rem 2rem 3rem;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

/* ===== 按钮样式 (浅色) ===== */
.btn {
  padding: 0.8rem 2rem;
  border-radius: 40px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #2d5be3;
  color: white;
  box-shadow: 0 6px 14px rgba(45, 91, 227, 0.15);
}

.btn-primary:hover {
  background: #1a3fb0;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(45, 91, 227, 0.2);
}

.btn-secondary {
  background: white;
  color: #1e2b3f;
  border: 1px solid #d0e0ff;
}

.btn-secondary:hover {
  background: #f5f9ff;
  border-color: #2d5be3;
  transform: translateY(-2px);
}

/* ===== 融合英雄区 + 双栏轮播区 ===== */
.hero-split-section {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 3rem;
  align-items: center;
  background: white;
  border-radius: 48px;
  padding: 3rem;
  box-shadow: 0 20px 40px -15px rgba(0, 40, 80, 0.08);
  border: 1px solid #eef4ff;
}

/* 左侧文案区 */
.hero-content {
  display: flex;
  flex-direction: column;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 1rem;
  color: #1a2a3a;
}

.title-line {
  display: block;
}

.gradient-text {
  background: linear-gradient(135deg, #2d5be3, #7b68ee);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.hero-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  color: #5a6f88;
  margin-bottom: 1rem;
}

.hero-description {
  font-size: 1rem;
  color: #4a5e78;
  line-height: 1.6;
  margin-bottom: 2rem;
  max-width: 450px;
}

.hero-cta {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.hero-badges {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.badge-item {
  background: #f0f7ff;
  padding: 0.3rem 1rem;
  border-radius: 30px;
  font-size: 0.85rem;
  color: #2d5be3;
  border: 1px solid #d9e8ff;
}

/* 右侧轮播区 */
.hero-carousel {
  width: 100%;
  border-radius: 36px;
  overflow: hidden;
  background: #f9fcff;
  box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.05);
}

.carousel-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  border-radius: 36px;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.carousel-slide {
  min-width: 100%;
  position: relative;
  aspect-ratio: 4/3; /* 控制图片比例 */
}

/* 图片区域 */
.slide-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  border-radius: 36px;
}

.slide-emoji {
  font-size: 6rem;
  filter: drop-shadow(0 10px 15px rgba(0, 0, 0, 0.05));
}

/* 悬停透明介绍版块 */
.slide-hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 36px;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.hover-content {
  max-width: 80%;
  text-align: center;
  padding: 1.5rem;
}

.hover-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a2a3a;
  margin: 0 0 0.5rem;
}

.hover-desc {
  font-size: 1rem;
  color: #3a4e68;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.hover-tag {
  display: inline-block;
  background: #eef4ff;
  color: #2d5be3;
  padding: 0.3rem 1rem;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* 轮播按钮 */
.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: white;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  font-size: 1.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s;
  color: #2d5be3;
  opacity: 0.9;
}

.carousel-btn:hover:not(:disabled) {
  background: #f5f9ff;
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.1);
  opacity: 1;
}

.carousel-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.carousel-btn.prev {
  left: 15px;
}
.carousel-btn.next {
  right: 15px;
}

/* 指示点 */
.carousel-dots {
  position: absolute;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 10;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(45, 91, 227, 0.3);
  cursor: pointer;
  transition: all 0.2s;
}

.dot.active {
  width: 24px;
  border-radius: 12px;
  background: #2d5be3;
}

/* ===== 简洁的品牌理念区 ===== */
.mission-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  border-radius: 36px;
  padding: 2rem 2.5rem;
  box-shadow: 0 15px 30px -10px rgba(0, 40, 80, 0.05);
  border: 1px solid #eef4ff;
  flex-wrap: wrap;
  gap: 2rem;
}

.mission-quote {
  display: flex;
  align-items: flex-start;
  gap: 0.3rem;
  flex: 2;
  min-width: 300px;
}

.quote-mark {
  font-size: 3rem;
  line-height: 1;
  color: #2d5be3;
  font-family: serif;
  margin-top: -10px;
  opacity: 0.4;
}

.mission-text {
  font-size: 1.1rem;
  color: #2a3f5a;
  line-height: 1.5;
  margin: 0;
  font-weight: 400;
}

.mission-badges {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: flex-end;
  flex: 1;
}

.badge-light {
  background: #f0f7ff;
  padding: 0.4rem 1.2rem;
  border-radius: 40px;
  font-size: 0.9rem;
  color: #2d5be3;
  border: 1px solid #d9e8ff;
}

/* ===== 响应式 ===== */
@media (max-width: 1000px) {
  .hero-split-section {
    grid-template-columns: 1fr;
    gap: 2rem;
    padding: 2rem;
  }
  
  .hero-description {
    max-width: 100%;
  }
  
  .mission-section {
    flex-direction: column;
    text-align: center;
  }
  
  .mission-quote {
    justify-content: center;
  }
  
  .mission-badges {
    justify-content: center;
  }
}

@media (max-width: 700px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .slide-emoji {
    font-size: 4rem;
  }
  
  .hover-title {
    font-size: 1.3rem;
  }
  
  .hover-desc {
    font-size: 0.9rem;
  }
  
  .carousel-btn {
    width: 36px;
    height: 36px;
    font-size: 1.2rem;
  }
}
</style>