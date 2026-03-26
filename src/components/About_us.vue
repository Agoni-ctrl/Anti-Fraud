<template>
  <div class="about-page">
    <!-- 首屏：杂志风格双栏，左侧大标题右侧视觉 -->
    <div class="hero-magazine">
      <div class="hero-content">
        <span class="hero-tagline">数字时代的火眼金睛</span>
        <h1 class="hero-title">让每一张图片、<br>每一段音频、每一个视频<br><span class="highlight">回归真实</span></h1>
        <p class="hero-desc">我们专注于AI伪造检测技术，为图片、音频、视频提供深度真伪分析。无论是AI换脸、语音合成还是深度伪造视频，让技术成为你辨别真假的可靠伙伴。</p>
      </div>
      <div class="hero-visual-card">
        <div class="visual-icon-group">
          <i class="fas fa-image"></i>
          <i class="fas fa-microphone-alt"></i>
          <i class="fas fa-video"></i>
        </div>
        <p class="visual-text">AI真伪识别 · 守护真相</p>
      </div>
    </div>

    <!-- 核心服务：整洁的杂志风格三栏，大小错落但有秩序 -->
    <div class="services-section">
      <div class="section-header">
        <span class="section-eyebrow">核心能力</span>
        <h2 class="section-title">多维伪造检测技术</h2>
        <p class="section-desc">基于深度学习的多模态检测引擎，为您的数字内容提供专业可信的真伪分析</p>
      </div>
      <div class="services-grid magazine-grid">
        <div class="service-card card-large">
          <div class="card-icon"><i class="fas fa-camera-retro"></i></div>
          <h3>图片真伪识别</h3>
          <p>检测AI生成图像、深度伪造人脸、PS篡改痕迹。支持JPG、PNG、WebP等主流格式，提供像素级分析报告。</p>
          <div class="card-tag">GAN检测 · 元数据分析</div>
        </div>
        <div class="service-card card-medium">
          <div class="card-icon"><i class="fas fa-waveform"></i></div>
          <h3>音频伪造检测</h3>
          <p>识别AI语音合成、声音克隆、音频拼接篡改。无论是电话录音还是语音消息，都能快速给出置信度评估。</p>
          <div class="card-tag">声纹分析 · 频谱检测</div>
        </div>
        <div class="service-card card-medium">
          <div class="card-icon"><i class="fas fa-film"></i></div>
          <h3>视频深度鉴伪</h3>
          <p>检测Deepfake换脸、口型同步伪造、帧序列篡改。逐帧分析，揪出每一处不自然的痕迹。</p>
          <div class="card-tag">时序分析 · 生物特征</div>
        </div>
      </div>
    </div>

    <!-- 技术特色：左右不对称但整洁的杂志布局 -->
    <div class="feature-spread">
      <div class="feature-block primary-block">
        <div class="feature-icon-large">
          <i class="fas fa-chart-line"></i>
        </div>
        <h3>持续进化的检测能力</h3>
        <p>面对不断更新的AI生成技术，我们的模型保持高频迭代训练。通过对抗式学习，让检测算法始终领先伪造技术一步。</p>
      </div>
      <div class="feature-block secondary-block">
        <div class="feature-icon-large">
          <i class="fas fa-shield-alt"></i>
        </div>
        <h3>隐私优先 · 数据不上云</h3>
        <p>用户上传的内容仅用于本地分析或加密传输，检测完成后即时清理，充分尊重您的数据隐私权。</p>
      </div>
      <div class="feature-block tertiary-block">
        <div class="feature-icon-large">
          <i class="fas fa-gauge-high"></i>
        </div>
        <h3>轻量快速 · 即传即测</h3>
        <p>优化的模型推理引擎，在保证准确率的同时实现快速响应，无需漫长等待即可获得检测结果。</p>
      </div>
    </div>

    <!-- 关于团队：整洁的卡片网格 -->
    <div class="team-section">
      <div class="section-header centered">
        <span class="section-eyebrow">守护者团队</span>
        <h2 class="section-title">技术向善的践行者</h2>
        <p class="section-desc">汇聚AI安全、数字取证、反欺诈领域的专业人士，以技术之力守护信息真实</p>
      </div>
      <div class="team-grid">
        <div class="team-card">
          <div class="team-avatar"><i class="fas fa-microchip"></i></div>
          <h4>AI安全研究组</h4>
          <p>专注于深度伪造检测、对抗性攻击防御算法研究</p>
        </div>
        <div class="team-card">
          <div class="team-avatar"><i class="fas fa-database"></i></div>
          <h4>数字取证团队</h4>
          <p>多媒体内容分析、篡改痕迹挖掘与证据链构建</p>
        </div>
        <div class="team-card">
          <div class="team-avatar"><i class="fas fa-hand-holding-heart"></i></div>
          <h4>反诈公益联盟</h4>
          <p>技术科普、公众教育与反诈知识传播</p>
        </div>
      </div>
    </div>

    <!-- 使命号召：杂志风格的底部区块 -->
    <div class="mission-footer">
      <div class="mission-content">
        <i class="fas fa-bullhorn mission-icon"></i>
        <h2>让真相不被伪装</h2>
        <p>无论是辨别网络信息的真伪，还是保护自己免受AI伪造内容的侵害，我们始终在这里，用技术为你守住真实的那道防线。</p>
        <button class="btn-primary" @click="handleTryNow">开始识别 <i class="fas fa-arrow-right"></i></button>
      </div>
      <div class="mission-quote">
        <i class="fas fa-quote-right"></i>
        <p>在AI生成内容泛滥的时代，<br>真实变得弥足珍贵，<br>而我们选择成为真实的守护者。</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutPage',
  methods: {
    handleTryNow() {
      // 跳转到真伪识别页面
      this.$router.push('/detection')
    }
  }
}
</script>

<style scoped>
.about-page {
  max-width: 1280px;
  margin: 2rem auto 4rem;
  padding: 0 2rem;
  font-family: 'Inter', 'Segoe UI', Roboto, system-ui, sans-serif;
  color: #1a2f3e;
}

/* 首屏杂志风格 */
.hero-magazine {
  display: flex;
  flex-wrap: wrap;
  gap: 3rem;
  margin-bottom: 5rem;
  align-items: center;
  justify-content: space-between;
}

.hero-content {
  flex: 1.2;
  min-width: 280px;
}

.hero-tagline {
  display: inline-block;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #4682B1;
  font-weight: 600;
  margin-bottom: 1rem;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: #1e3a4d;
}

.hero-title .highlight {
  color: #4682B1;
  position: relative;
  display: inline-block;
}

.hero-title .highlight::after {
  content: '';
  position: absolute;
  bottom: 8px;
  left: 0;
  width: 100%;
  height: 8px;
  background: #87CEEB;
  opacity: 0.4;
  z-index: -1;
}

.hero-desc {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #4a6f84;
  max-width: 90%;
}

.hero-visual-card {
  flex: 0.8;
  background: #FFFFFF;
  border-radius: 32px;
  padding: 2rem;
  text-align: center;
  border: 1px solid #d4eef2;
  box-shadow: 0 8px 24px rgba(70, 130, 177, 0.06);
}

.visual-icon-group {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.visual-icon-group i {
  font-size: 2.5rem;
  color: #4682B1;
  background: #f0fafc;
  padding: 1rem;
  border-radius: 24px;
  transition: all 0.2s;
}

.visual-text {
  font-weight: 500;
  color: #4682B1;
  font-size: 0.9rem;
}

/* 核心服务区域 */
.services-section {
  margin: 5rem 0;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header.centered {
  text-align: center;
}

.section-eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #4682B1;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #1e3a4d;
  margin-bottom: 1rem;
}

.section-desc {
  font-size: 1rem;
  color: #5a7f94;
  max-width: 600px;
  margin: 0 auto;
}

/* 杂志风格网格：大小错落但整洁 */
.services-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.8rem;
  justify-content: center;
}

.magazine-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.8rem;
}

.service-card {
  background: #FFFFFF;
  border-radius: 28px;
  padding: 2rem;
  transition: all 0.3s ease;
  border: 1px solid #e2f0f2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.service-card:hover {
  transform: translateY(-4px);
  border-color: #87CEEB;
  box-shadow: 0 12px 28px rgba(70, 130, 177, 0.08);
}

.card-large {
  flex: 1.4;
  min-width: 280px;
}

.card-medium {
  flex: 1;
  min-width: 240px;
}

.card-icon {
  font-size: 2.5rem;
  color: #4682B1;
  margin-bottom: 1.2rem;
}

.service-card h3 {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #1e3a4d;
}

.service-card p {
  color: #5a7f94;
  line-height: 1.5;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.card-tag {
  display: inline-block;
  font-size: 0.7rem;
  padding: 0.25rem 0.75rem;
  background: #f0fafc;
  color: #4682B1;
  border-radius: 20px;
  margin-top: 0.5rem;
}

/* 技术特色区块 - 杂志风格三栏不对称但有秩序 */
.feature-spread {
  display: flex;
  flex-wrap: wrap;
  gap: 1.8rem;
  margin: 5rem 0;
}

.feature-block {
  flex: 1;
  padding: 2rem;
  border-radius: 28px;
  transition: all 0.2s;
}

.primary-block {
  background: #FFFFFF;
  border: 1px solid #87CEEB;
  box-shadow: 0 4px 12px rgba(135, 206, 235, 0.1);
}

.secondary-block {
  background: #FFFFFF;
  border: 1px solid #e2f0f2;
}

.tertiary-block {
  background: #FFFFFF;
  border: 1px solid #e2f0f2;
}

.feature-block:hover {
  transform: translateY(-4px);
  border-color: #4682B1;
}

.feature-icon-large {
  font-size: 2.2rem;
  color: #4682B1;
  margin-bottom: 1rem;
}

.feature-block h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #1e3a4d;
}

.feature-block p {
  color: #5a7f94;
  line-height: 1.5;
  font-size: 0.95rem;
}

/* 团队区域 */
.team-section {
  margin: 5rem 0;
}

.team-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
  margin-top: 2rem;
}

.team-card {
  flex: 1;
  min-width: 220px;
  background: #FFFFFF;
  border-radius: 28px;
  padding: 2rem 1.5rem;
  text-align: center;
  border: 1px solid #e2f0f2;
  transition: all 0.2s;
}

.team-card:hover {
  border-color: #87CEEB;
  transform: translateY(-4px);
}

.team-avatar {
  width: 80px;
  height: 80px;
  background: #f0fafc;
  border-radius: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.2rem;
  font-size: 2.2rem;
  color: #4682B1;
}

.team-card h4 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1e3a4d;
}

.team-card p {
  font-size: 0.85rem;
  color: #6b8ba0;
  line-height: 1.4;
}

/* 使命底部区域 */
.mission-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 4rem;
  background: #FFFFFF;
  border-radius: 40px;
  padding: 3rem;
  border: 1px solid #e2f0f2;
  box-shadow: 0 8px 24px rgba(70, 130, 177, 0.04);
}

.mission-content {
  flex: 1.2;
}

.mission-icon {
  font-size: 2.5rem;
  color: #4682B1;
  margin-bottom: 1rem;
}

.mission-content h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1e3a4d;
}

.mission-content p {
  font-size: 1rem;
  line-height: 1.6;
  color: #5a7f94;
  margin-bottom: 1.8rem;
}

.btn-primary {
  background: #4682B1;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 40px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background: #2c5a7a;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(70, 130, 177, 0.2);
}

.mission-quote {
  flex: 0.8;
  background: #f9fdfe;
  border-radius: 28px;
  padding: 2rem;
  text-align: right;
  border-left: 3px solid #87CEEB;
}

.mission-quote i {
  font-size: 2rem;
  color: #87CEEB;
  margin-bottom: 1rem;
  display: block;
  text-align: right;
}

.mission-quote p {
  font-size: 1.1rem;
  line-height: 1.5;
  color: #2c5a7a;
  font-style: italic;
}

/* 响应式 */
@media (max-width: 850px) {
  .about-page {
    padding: 0 1.2rem;
  }
  
  .hero-title {
    font-size: 2.2rem;
  }
  
  .hero-desc {
    max-width: 100%;
  }
  
  .hero-magazine,
  .feature-spread,
  .mission-footer {
    flex-direction: column;
  }
  
  .mission-quote {
    text-align: left;
  }
  
  .mission-quote i {
    text-align: left;
  }
  
  .section-title {
    font-size: 1.8rem;
  }
  
  .service-card {
    min-width: 100%;
  }
}
</style>