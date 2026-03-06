<template>
  <div class="fraud-news-dashboard">
    <!-- 主内容区：采用flex布局，左侧内容区 + 右侧边栏 -->
    <div class="main-container">
      <!-- 左侧主内容区 -->
      <div class="content-area">
        <!-- 搜索区（改进版） -->
        <div class="search-section">
          <div class="search-wrapper">
            <input 
              type="text" 
              class="search-input" 
              placeholder="搜索案例、诈骗手法、关键词..."
            >
            <button class="search-button">搜索</button>
          </div>
          <div class="hot-search">
            <span class="hot-label">热门搜索：</span>
            <a href="#" class="hot-tag">刷单诈骗</a>
            <a href="#" class="hot-tag">冒充公检法</a>
            <a href="#" class="hot-tag">演唱会门票</a>
            <a href="#" class="hot-tag">FaceTime诈骗</a>
          </div>
        </div>

        <!-- 头条焦点区 - 重大预警轮播 -->
        <div class="featured-section">
          <h2 class="section-title">⚠️ 紧急预警</h2>
          <div class="featured-carousel">
            <div class="featured-card" v-for="(item, index) in featuredItems" :key="'featured'+index">
              <img :src="item.image" :alt="item.title" class="featured-image">
              <div class="featured-content">
                <h3 class="featured-title">{{ item.title }}</h3>
                <p class="featured-summary">{{ item.summary }}</p>
                <span class="featured-tag">{{ item.tag }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 新闻流主区 - 一图一文卡片列表 -->
        <div class="news-feed-section">
          <h2 class="section-title">📰 最新动态</h2>
          <div class="news-feed">
            <article 
              v-for="item in newsItems" 
              :key="item.id" 
              class="news-card"
              @click="viewDetail(item)"
            >
              <div class="card-image">
                <img :src="item.imageUrl" :alt="item.title" loading="lazy">
                <span v-if="item.type === 'case'" class="case-badge">真实案例</span>
                <span v-if="item.type === 'warning'" class="warning-badge">警方预警</span>
              </div>
              <div class="card-content">
                <h3 class="news-title">{{ item.title }}</h3>
                <p class="news-summary">{{ item.summary }}</p>
                <div class="news-meta" @click.stop>
                  <span class="publish-time">{{ item.publishTime }}</span>
                  <div class="interaction-bar">
                    <button class="action-btn like-btn" :class="{ liked: item.isLiked }" @click="toggleLike(item)">
                      <span class="icon">{{ item.isLiked ? '❤️' : '🤍' }}</span>
                      <span class="count">{{ formatCount(item.likes) }}</span>
                    </button>
                    <button class="action-btn" @click="shareItem(item)">
                      <i class="fa-solid fa-share"></i>
                      <span>分享</span>
                    </button>
                    <button class="action-btn" @click="commentOnItem(item)">
                      <span class="icon">💬</span>
                      <span class="count">{{ formatCount(item.comments) }}</span>
                    </button>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>

      <!-- 右侧边栏 - 包含浏览记录等功能 -->
      <aside class="sidebar">
        <!-- 浏览记录模块 -->
        <div class="sidebar-card">
          <h3 class="sidebar-title">📋 近期浏览</h3>
          <div class="history-list">
            <div v-if="historyItems.length === 0" class="empty-history">
              暂无浏览记录
            </div>
            <a v-for="(item, index) in historyItems" :key="'history'+index" href="#" class="history-item">
              <span class="history-title">{{ item.title }}</span>
              <span class="history-time">{{ item.time }}</span>
            </a>
          </div>
          <button class="clear-history" @click="clearHistory">清除记录</button>
        </div>

        <!-- 热门推荐模块 -->
        <div class="sidebar-card">
          <h3 class="sidebar-title">🔥 热门推荐</h3>
          <div class="hot-list">
            <div v-for="(item, index) in hotItems" :key="'hot'+index" class="hot-item" @click="viewDetail(item)">
              <span class="hot-rank" :class="'rank-'+ (index+1)">{{ index+1 }}</span>
              <div class="hot-content">
                <h4 class="hot-title">{{ item.title }}</h4>
                <span class="hot-stats">🔥 {{ formatCount(item.views) }} 阅读</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 反诈专线入口 -->
        <div class="sidebar-card hotline-card">
          <div class="hotline-content">
            <div class="hotline-icon">📞</div>
            <div class="hotline-text">
              <h4>反诈专线</h4>
              <p>96110</p>
            </div>
          </div>
          <p class="hotline-desc">遇骗请立即拨打</p>
        </div>

        <!-- 举报入口 -->
        <div class="sidebar-card report-card">
          <div class="report-content">
            <span class="report-icon">🚨</span>
            <span>在线举报</span>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script>
import news1 from '../assets/images/news_photo/facetime2.jpeg'
import news2 from '../assets/images/news_photo/演唱会1.jpg'
import news3 from '../assets/images/news_photo/客服诈骗.jpg'
import news4 from '../assets/images/news_photo/演唱会2.jpg'
import news5 from '../assets/images/news_photo/facetime.png'
import news6 from '../assets/images/news_photo/刷单.jpeg'
import news7 from '../assets/images/news_photo/假公安.jpeg'
import news8 from '../assets/images/news_photo/虚假教育机构.jpeg'
import news9 from '../assets/images/news_photo/诱导投资.png'
export default {
  name: 'FraudNewsDashboard',
  data() {
    return {
      // 头条焦点数据
      featuredItems: [
        {
          title: 'FaceTime来电需警惕！已有多人被骗',
          summary: '近期利用FaceTime冒充客服诈骗高发，切勿开启屏幕共享',
          image: news1,
          tag: '紧急'
        },
        {
          title: '演唱会门票诈骗新套路：假票务网站',
          summary: '骗子伪造票务网站，诱导直接转账后失联',
          image: news2,
          tag: '新手法'
        },
        {
          title: '警惕"百万保障"到期骗局',
          summary: '冒充微信/支付宝客服，称百万保障到期需续费',
          image: news3,
          tag: '高发'
        }
      ],
      // 新闻流数据
      newsItems: [
        {
          id: 1,
          type: 'case',
          title: '为看演唱会买"黄牛票"，大学生被骗3万元',
          summary: '在微博联系转让门票，按要求转账后被拉黑，警方已立案。',
          imageUrl: news4,
          publishTime: '2小时前',
          likes: 1234,
          comments: 289,
          views: 5678,
          isLiked: false
        },
        {
          id: 2,
          type: 'warning',
          title: 'FaceTime来电称"利率调整"，女子被骗18万',
          summary: '骗子冒充金融平台客服，诱导开启屏幕共享盗刷银行卡。',
          imageUrl: news5,
          publishTime: '5小时前',
          likes: 2567,
          comments: 401,
          views: 8901,
          isLiked: true
        },
        {
          id: 3,
          type: 'case',
          title: '刷单返利：先给甜头后骗大额',
          summary: '先返现几十元获取信任，随后以"连单""卡单"为由骗取数万元。',
          imageUrl: news6,
          publishTime: '昨天',
          likes: 892,
          comments: 134,
          views: 3456,
          isLiked: false
        },
        {
          id: 4,
          type: 'case',
          title: '假"公安"来电称涉嫌洗钱，老人转账50万',
          summary: '骗子伪造通缉令，要求将资金转入"安全账户"审查。',
          imageUrl: news7,
          publishTime: '昨天',
          likes: 3456,
          comments: 512,
          views: 12034,
          isLiked: false
        },
        {
          id: 5,
          type: 'warning',
          title: '当心！骗子冒充孩子索要培训费',
          summary: '通过QQ冒充子女，以报名名校培训班为由要求家长转账。',
          imageUrl: news8,
          publishTime: '3天前',
          likes: 678,
          comments: 98,
          views: 2345,
          isLiked: false
        },
        {
          id: 6,
          type: 'case',
          title: '网络交友诱导投资，女子一周被骗24万',
          summary: '网友诱导下载投资APP，前期盈利后无法提现。',
          imageUrl: news9,
          publishTime: '4天前',
          likes: 1890,
          comments: 277,
          views: 7890,
          isLiked: false
        }
      ],
      // 浏览记录数据
      historyItems: [
        { title: 'FaceTime来电诈骗揭秘', time: '10分钟前' },
        { title: '演唱会门票诈骗新套路', time: '1小时前' },
        { title: '冒充公检法诈骗话术解析', time: '3小时前' }
      ],
      // 热门推荐数据
      hotItems: [
        { id: 7, title: '2024年最新诈骗手法TOP10', views: 23456 },
        { id: 8, title: '遇到FaceTime诈骗怎么办', views: 18765 },
        { id: 9, title: '刷单诈骗的完整话术解析', views: 15432 },
        { id: 10, title: '96110来电一定要接', views: 12345 },
        { id: 11, title: '国家反诈中心App使用指南', views: 10987 }
      ]
    }
  },
  methods: {
    toggleLike(item) {
      item.isLiked = !item.isLiked;
      if (item.isLiked) {
        item.likes += 1;
      } else {
        item.likes -= 1;
      }
    },
    shareItem(item) {
      alert(`分享：${item.title}`);
    },
    commentOnItem(item) {
      alert(`评论：${item.title}`);
    },
    viewDetail(item) {
      alert(`查看详情：${item.title}`);
      // 实际开发中可添加跳转逻辑
      // 模拟添加浏览记录
      this.addToHistory(item);
    },
    addToHistory(item) {
      // 简单实现：将查看的新闻添加到浏览记录最前面
      const exists = this.historyItems.findIndex(h => h.title === item.title);
      if (exists !== -1) {
        this.historyItems.splice(exists, 1);
      }
      this.historyItems.unshift({
        title: item.title,
        time: '刚刚'
      });
      // 只保留最近5条
      if (this.historyItems.length > 5) {
        this.historyItems.pop();
      }
    },
    clearHistory() {
      this.historyItems = [];
    },
    formatCount(num) {
      if (num >= 10000) {
        return (num / 10000).toFixed(1) + 'w';
      }
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
      }
      return num.toString();
    }
  }
}
</script>

<style scoped>
/* ========== 全局样式：简约明亮配色 ========== */
.fraud-news-dashboard {
  max-width: 1280px;
  margin: 0 auto;
  background: #f8fafc;  /* 极浅灰蓝背景 */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #1e293b;
  min-height: 100vh;
}

/* ========== 主容器flex布局 ========== */
.main-container {
  display: flex;
  gap: 24px;
  padding: 24px;
  padding-top: 20px;
  max-width: 1280px;
  margin: 0 auto;
}

/* 左侧主内容区 - 占2/3宽度 */
.content-area {
  flex: 2;
  min-width: 0; /* 防止flex溢出 */
}

/* 右侧边栏 - 占1/3宽度 */
.sidebar {
  flex: 1;
  min-width: 260px;
  position: sticky;
  top: 80px;
  height: fit-content;
  align-self: flex-start;
}

/* ========== 搜索区样式 ========== */
.search-section {
  background: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  border: 1px solid #eef2f6;
}

.search-wrapper {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.search-input {
  flex: 1;
  height: 48px;
  border: 1px solid #e2e8f0;
  border-radius: 40px;
  padding: 0 20px;
  font-size: 15px;
  background: #f8fafc;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #2563eb;
  background: white;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}

.search-button {
  width: 100px;
  background: #2563eb;
  border: none;
  border-radius: 40px;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.search-button:hover {
  background: #1d4ed8;
}

.hot-search {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 14px;
}

.hot-label {
  color: #64748b;
}

.hot-tag {
  color: #2563eb;
  text-decoration: none;
  background: #eef2ff;
  padding: 4px 12px;
  border-radius: 30px;
  font-size: 13px;
  transition: background 0.2s;
}

.hot-tag:hover {
  background: #dbeafe;
}

/* ========== 头条焦点区 ========== */
.featured-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 16px;
  padding-left: 4px;
}

.featured-carousel {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.featured-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  border: 1px solid #eef2f6;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.featured-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 20px -10px rgba(0,0,0,0.1);
}

.featured-image {
  width: 100%;
  height: 140px;
  object-fit: cover;
}

.featured-content {
  padding: 16px;
}

.featured-title {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 8px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.featured-summary {
  font-size: 13px;
  color: #475569;
  margin: 0 0 12px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.featured-tag {
  display: inline-block;
  background: #fee2e2;
  color: #b91c1c;
  font-size: 11px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 30px;
}

/* ========== 新闻流主区 ========== */
.news-feed {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.news-card {
  display: flex;
  gap: 20px;
  background: white;
  border-radius: 20px;
  padding: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  border: 1px solid #eef2f6;
  transition: all 0.2s ease;
  cursor: pointer;
}

.news-card:hover {
  box-shadow: 0 10px 20px -8px rgba(0,0,0,0.08);
  border-color: #d1d9e6;
}

.card-image {
  position: relative;
  flex-shrink: 0;
  width: 120px;
  height: 90px;
  border-radius: 16px;
  overflow: hidden;
  background: #e2e8f0;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.news-card:hover .card-image img {
  transform: scale(1.05);
}

.case-badge, .warning-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  font-size: 10px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 30px;
  color: white;
}

.case-badge {
  background: #dc2626;
}

.warning-badge {
  background: #ea580c;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.news-title {
  margin: 0 0 6px 0;
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-summary {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #475569;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
}

.publish-time {
  font-size: 12px;
  color: #64748b;
}

.interaction-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  padding: 4px 8px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
  border-radius: 30px;
  transition: background 0.2s;
}

.action-btn:hover {
  background: #f1f5f9;
  color: #2563eb;
}

.like-btn.liked {
  color: #dc2626;
}

.action-btn .icon {
  font-size: 16px;
}

.action-btn .count {
  font-size: 12px;
  font-weight: 500;
}

/* ========== 右侧边栏样式 ========== */
.sidebar-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  border: 1px solid #eef2f6;
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 16px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eef2f6;
}

/* 浏览记录样式 */
.history-list {
  margin-bottom: 12px;
}

.empty-history {
  color: #94a3b8;
  font-size: 14px;
  text-align: center;
  padding: 20px 0;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  text-decoration: none;
  border-bottom: 1px solid #f1f5f9;
}

.history-item:last-child {
  border-bottom: none;
}

.history-title {
  font-size: 14px;
  color: #1e293b;
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-time {
  font-size: 12px;
  color: #94a3b8;
}

.clear-history {
  width: 100%;
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 30px;
  padding: 8px;
  font-size: 13px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 8px;
}

.clear-history:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

/* 热门推荐样式 */
.hot-item {
  display: flex;
  gap: 10px;
  padding: 10px 0;
  cursor: pointer;
  border-bottom: 1px solid #f1f5f9;
}

.hot-item:last-child {
  border-bottom: none;
}

.hot-rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 600;
  color: #475569;
}

.hot-rank.rank-1 {
  background: #fef9c3;
  color: #854d0e;
}

.hot-rank.rank-2 {
  background: #e0f2fe;
  color: #0369a1;
}

.hot-rank.rank-3 {
  background: #ffe4e6;
  color: #9f1239;
}

.hot-content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hot-title {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  margin: 0;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hot-stats {
  font-size: 12px;
  color: #94a3b8;
}

/* 反诈专线卡片 - 图标稍小，文字居中靠拢 */
.hotline-card {
  background: linear-gradient(145deg, #f0f9ff, #e6f0fa);
  border: 1px solid #b9d9f0;
  padding: 16px;           /* 适当减小内边距 */
}

.hotline-content {
  display: flex;
  align-items: center;     /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  gap: 8px;                /* 减小间距，让文字向中间靠 */
  margin-bottom: 8px;
}

.hotline-icon {
  font-size: 28px;         /* 图标稍微调小 */
  line-height: 1;
}

.hotline-text {
  text-align: left;
}

.hotline-text h4 {
  font-size: 18px;
  font-weight: 700;
  color: #0369a1;
  margin: 0 0 2px 0;       /* 减小标题和号码间距 */
}

.hotline-text p {
  font-size: 22px;         /* 号码稍微调小一点，与图标更协调 */
  font-weight: 700;
  color: #0284c7;
  margin: 0;
  letter-spacing: 0.5px;
}

.hotline-desc {
  font-size: 13px;
  color: #2563eb;
  margin: 4px 0 0 0;
  text-align: center;
}

/* 举报卡片 */
.report-card {
  background: #fef2f2;
  border: 1px solid #fecaca;
  cursor: pointer;
  transition: all 0.2s;
}

.report-card:hover {
  background: #fee2e2;
}

.report-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
  color: #b91c1c;
}

.report-icon {
  font-size: 20px;
}

/* ========== 响应式 ========== */
@media (max-width: 900px) {
  .main-container {
    flex-direction: column;
  }
  
  .sidebar {
    position: static;
    width: 100%;
  }
  
  .featured-carousel {
    grid-template-columns: 1fr;
  }
  
  .top-nav {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .nav-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}

@media (max-width: 600px) {
  .news-card {
    flex-direction: column;
  }
  
  .card-image {
    width: 100%;
    height: 160px;
  }
  
  .search-wrapper {
    flex-direction: column;
  }
  
  .search-button {
    width: 100%;
    height: 44px;
  }
}
</style>