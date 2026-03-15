<template>
  <div class="fraud-news-dashboard">
    <!-- 主内容区：采用flex布局，左侧内容区 + 右侧边栏 -->
    <div class="main-container">
      <!-- 左侧主内容区 -->
      <div class="content-area">
        <!-- 搜索区（带真实搜索功能） -->
        <div class="search-section">
          <div class="search-wrapper">
            <input 
              type="text" 
              class="search-input" 
              v-model="searchQuery"
              placeholder="搜索案例、诈骗手法、关键词..."
              @keyup.enter="performSearch"
            >
            <button class="search-button" @click="performSearch">搜索</button>
          </div>
          <div class="hot-search">
            <span class="hot-label">热门搜索：</span>
            <a 
              href="javascript:void(0)" 
              v-for="(tag, index) in hotSearchTags" 
              :key="index"
              class="hot-tag" 
              @click="searchByTag(tag)"
            >
              {{ tag }}
            </a>
          </div>
          
          <!-- 搜索结果提示 -->
          <div v-if="searchPerformed" class="search-result-info">
            找到 {{ filteredNewsItems.length }} 条与“{{ lastSearchQuery }}”相关的结果
            <button class="clear-search" @click="clearSearch">× 清除</button>
          </div>
        </div>

        <!-- 头条焦点区 - 重大预警轮播 -->
        <div class="featured-section">
          <h2 class="section-title">⚠️ 紧急预警</h2>
          <div class="featured-carousel">
            <div class="featured-card" v-for="(item, index) in featuredItems" :key="'featured'+index" @click="viewDetail(item)">
              <img :src="item.image" :alt="item.title" class="featured-image">
              <div class="featured-content">
                <h3 class="featured-title">{{ item.title }}</h3>
                <p class="featured-summary">{{ item.summary }}</p>
                <span class="featured-tag">{{ item.tag }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 新闻流主区 - 一图一文卡片列表（支持过滤显示搜索结果） -->
        <div class="news-feed-section">
          <h2 class="section-title">{{ searchPerformed ? '🔍 搜索结果' : '📰 最新动态' }}</h2>
          <div v-if="displayedNewsItems.length === 0" class="no-results">
            暂无相关新闻
          </div>
          <div class="news-feed">
            <article 
              v-for="item in displayedNewsItems" 
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
                <h3 class="news-title" v-html="highlightText(item.title)"></h3>
                <p class="news-summary" v-html="highlightText(item.summary)"></p>
                <div class="news-meta" @click.stop>
                  <span class="publish-time">{{ item.publishTime }}</span>
                  <div class="interaction-bar">
                    <button class="action-btn like-btn" :class="{ liked: item.isLiked }" @click="toggleLike(item)">
                      <span class="icon">{{ item.isLiked ? '❤️' : '🤍' }}</span>
                      <span class="count">{{ formatCount(item.likes) }}</span>
                    </button>
                    <button class="action-btn" @click="shareItem(item)">
                      <span class="icon"><i class="fa-solid fa-share-nodes"></i></span>
                    </button>
                    <button class="action-btn" @click="openCommentModal(item)">
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

      <!-- 右侧边栏 -->
      <aside class="sidebar">
        <!-- 浏览记录模块 -->
        <div class="sidebar-card">
          <h3 class="sidebar-title">📋 最近浏览</h3>
          <div class="history-list">
            <div v-if="historyItems.length === 0" class="empty-history">
              暂无浏览记录
            </div>
            <a 
              v-for="(item, index) in historyItems" 
              :key="'history'+index" 
              href="javascript:void(0)" 
              class="history-item"
              @click="viewHistoryItem(item)"
            >
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
            <span class="hotline-icon">📞</span>
            <div class="hotline-text">
              <h4>反诈专线</h4>
              <p>96110</p>
            </div>
          </div>
          <p class="hotline-desc">遇骗请立即拨打</p>
        </div>

        <!-- 举报入口 -->
        <div class="sidebar-card report-card" @click="openReport">
          <div class="report-content">
            <span class="report-icon">🚨</span>
            <span>在线举报</span>
          </div>
        </div>
      </aside>
    </div>

    <!-- 评论弹窗组件 -->
    <transition name="modal-fade">
      <div v-if="showCommentModal" class="modal-overlay" @click.self="closeCommentModal">
        <div class="comment-modal">
          <div class="modal-header">
            <h3>📝 评论 · {{ currentNews?.title }}</h3>
            <button class="close-modal" @click="closeCommentModal">×</button>
          </div>
          
          <div class="comments-list" ref="commentsContainer">
            <div v-if="commentsLoading" class="comments-loading">
              <span class="loading-spinner"></span> 加载评论中...
            </div>
            <div v-else-if="currentComments.length === 0" class="no-comments">
              暂无评论，快来抢沙发吧～
            </div>
            <div v-else>
              <div v-for="comment in currentComments" :key="comment.id" class="comment-item">
                <div class="comment-avatar">
                  <img 
                    :src="comment.avatar || `https://ui-avatars.com/api/?name=${comment.author}&background=2563eb&color=fff&size=40`" 
                    :alt="comment.author"
                    @error="handleImageError"
                  >
                </div>
                <div class="comment-content">
                  <div class="comment-header">
                    <span class="comment-author">{{ comment.author }}</span>
                    <span class="comment-time">{{ comment.time }}</span>
                  </div>
                  <p class="comment-text">{{ comment.text }}</p>
                  <div class="comment-actions">
                    <button class="comment-like" @click="likeComment(comment)">
                      <span>{{ comment.isLiked ? '❤️' : '🤍' }}</span>
                      <span>{{ comment.likes > 0 ? comment.likes : '' }}</span>
                    </button>
                    <button class="comment-reply" @click="replyToComment(comment)">回复</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="comment-input-area">
            <textarea 
              v-model="newCommentText" 
              placeholder="写下你的评论..." 
              rows="2"
              @keydown.enter.prevent="submitComment"
            ></textarea>
            <div class="comment-actions-bottom">
              <span class="comment-length">{{ newCommentText.length }}/200</span>
              <button 
                class="submit-comment" 
                @click="submitComment"
                :disabled="!newCommentText.trim() || submittingComment"
              >
                {{ submittingComment ? '发布中...' : '发布评论' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- 提示消息组件 -->
    <transition name="toast-fade">
      <div v-if="toast.show" class="global-toast" :class="toast.type">
        {{ toast.message }}
      </div>
    </transition>
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
      // ========== 搜索相关 ==========
      searchQuery: '',
      lastSearchQuery: '',
      searchPerformed: false,
      hotSearchTags: ['刷单诈骗', '冒充公检法', '演唱会门票', 'FaceTime诈骗'],
      
      // ========== 头条焦点数据 ==========
      featuredItems: [
        {
          id: 'f1',
          title: 'FaceTime来电需警惕！已有多人被骗',
          summary: '近期利用FaceTime冒充客服诈骗高发，切勿开启屏幕共享',
          image: news1,
          tag: '紧急'
        },
        {
          id: 'f2',
          title: '演唱会门票诈骗新套路：假票务网站',
          summary: '骗子伪造票务网站，诱导直接转账后失联',
          image: news2,
          tag: '新手法'
        },
        {
          id: 'f3',
          title: '警惕"百万保障"到期骗局',
          summary: '冒充微信/支付宝客服，称百万保障到期需续费',
          image: news3,
          tag: '高发'
        }
      ],
      
      // ========== 新闻流数据 ==========
      newsItems: [
        {
          id: 1,
          type: 'case',
          title: '【刷单诈骗】为看演唱会买"黄牛票"，大学生被骗3万元',
          summary: '在微博联系转让门票，按要求转账后被拉黑，警方已立案。',
          imageUrl: news4,
          publishTime: '2小时前',
          likes: 1234,
          comments: 289,
          views: 5678,
          isLiked: false,
          shareUrl: 'https://fan-zha.com/news/1',
          shareTitle: '为看演唱会买"黄牛票"，大学生被骗3万元'
        },
        {
          id: 2,
          type: 'warning',
          title: '【FaceTime诈骗】来电称"利率调整"，女子被骗18万',
          summary: '骗子冒充金融平台客服，诱导开启屏幕共享盗刷银行卡。',
          imageUrl: news5,
          publishTime: '5小时前',
          likes: 2567,
          comments: 401,
          views: 8901,
          isLiked: true,
          shareUrl: 'https://fan-zha.com/news/2',
          shareTitle: 'FaceTime来电称"利率调整"，女子被骗18万'
        },
        {
          id: 3,
          type: 'case',
          title: '【刷单返利】先给甜头后骗大额，已有多人上当',
          summary: '先返现几十元获取信任，随后以"连单""卡单"为由骗取数万元。',
          imageUrl: news6,
          publishTime: '昨天',
          likes: 892,
          comments: 134,
          views: 3456,
          isLiked: false,
          shareUrl: 'https://fan-zha.com/news/3',
          shareTitle: '刷单返利：先给甜头后骗大额'
        },
        {
          id: 4,
          type: 'case',
          title: '【冒充公检法】假"公安"来电称涉嫌洗钱，老人转账50万',
          summary: '骗子伪造通缉令，要求将资金转入"安全账户"审查。',
          imageUrl: news7,
          publishTime: '昨天',
          likes: 3456,
          comments: 512,
          views: 12034,
          isLiked: false,
          shareUrl: 'https://fan-zha.com/news/4',
          shareTitle: '假"公安"来电称涉嫌洗钱，老人转账50万'
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
          isLiked: false,
          shareUrl: 'https://fan-zha.com/news/5',
          shareTitle: '当心！骗子冒充孩子索要培训费'
        },
        {
          id: 6,
          type: 'case',
          title: '【网络交友诈骗】诱导投资，女子一周被骗24万',
          summary: '网友诱导下载投资APP，前期盈利后无法提现。',
          imageUrl: news9,
          publishTime: '4天前',
          likes: 1890,
          comments: 277,
          views: 7890,
          isLiked: false,
          shareUrl: 'https://fan-zha.com/news/6',
          shareTitle: '网络交友诱导投资，女子一周被骗24万'
        }
      ],
      
      // ========== 浏览记录 ==========
      historyItems: [
        { id: 1, title: 'FaceTime来电诈骗揭秘', time: '10分钟前' },
        { id: 2, title: '演唱会门票诈骗新套路', time: '1小时前' },
        { id: 3, title: '冒充公检法诈骗话术解析', time: '3小时前' }
      ],
      
      // ========== 热门推荐 ==========
      hotItems: [
        { id: 7, title: '2024年最新诈骗手法TOP10', views: 23456, imageUrl: '', type: 'news' },
        { id: 8, title: '遇到FaceTime诈骗怎么办', views: 18765, imageUrl: '', type: 'news' },
        { id: 9, title: '刷单诈骗的完整话术解析', views: 15432, imageUrl: '', type: 'news' },
        { id: 10, title: '96110来电一定要接', views: 12345, imageUrl: '', type: 'news' },
        { id: 11, title: '国家反诈中心App使用指南', views: 10987, imageUrl: '', type: 'news' }
      ],
      
      // ========== 评论弹窗相关 ==========
      showCommentModal: false,
      currentNews: null,
      currentComments: [],
      commentsLoading: false,
      newCommentText: '',
      submittingComment: false,
      
      // 模拟评论数据（按新闻ID存储）
      commentsDatabase: {
        1: [
          { id: 101, author: '平安市民', text: '太可怕了，我也差点被骗', time: '1小时前', likes: 12, isLiked: false },
          { id: 102, author: '反诈志愿者', text: '大家一定要通过官方渠道购票', time: '45分钟前', likes: 8, isLiked: false }
        ],
        2: [
          { id: 201, author: '苹果用户', text: 'FaceTime真的要注意，我收到过', time: '3小时前', likes: 24, isLiked: true },
          { id: 202, author: '警察叔叔', text: '建议关闭FaceTime功能', time: '2小时前', likes: 56, isLiked: false },
          { id: 203, author: '科技达人', text: '已经转告家人了', time: '1小时前', likes: 7, isLiked: false }
        ],
        3: [
          { id: 301, author: '学生小明', text: '刷单都是骗人的，千万别信', time: '昨天', likes: 32, isLiked: false }
        ],
        4: [
          { id: 401, author: '退休老人', text: '接到这种电话直接挂断', time: '昨天', likes: 45, isLiked: false },
          { id: 402, author: '社区民警', text: '公安机关不会电话办案', time: '20小时前', likes: 67, isLiked: false }
        ],
        5: [
          { id: 501, author: '家长', text: '一定要和孩子约定暗号', time: '3天前', likes: 19, isLiked: false }
        ],
        6: [
          { id: 601, author: '单身青年', text: '网上交友要谨慎，别被骗', time: '4天前', likes: 23, isLiked: false },
          { id: 602, author: '投资顾问', text: '高回报投资基本都是骗局', time: '3天前', likes: 15, isLiked: false }
        ]
      },
      
      // ========== 提示消息 ==========
      toast: {
        show: false,
        message: '',
        type: 'info'
      },
      
      // 评论ID计数器
      nextCommentId: 1000
    }
  },
  
  computed: {
    // 根据搜索条件过滤新闻
    filteredNewsItems() {
      if (!this.searchPerformed || !this.lastSearchQuery) {
        return this.newsItems;
      }
      
      const query = this.lastSearchQuery.toLowerCase();
      return this.newsItems.filter(item => 
        item.title.toLowerCase().includes(query) || 
        item.summary.toLowerCase().includes(query)
      );
    },
    
    // 当前显示的新闻
    displayedNewsItems() {
      return this.searchPerformed ? this.filteredNewsItems : this.newsItems;
    }
  },
  
  methods: {
    // 头像加载失败处理
    handleImageError(event) {
      const img = event.target;
      img.style.display = 'none';
      
      const parent = img.parentNode;
      parent.classList.add('avatar-fallback');
      
      const author = img.alt || '用';
      parent.setAttribute('data-initial', author.charAt(0).toUpperCase());
    },
    
    // ========== 搜索功能 ==========
    performSearch() {
      if (!this.searchQuery.trim()) {
        this.showToast('请输入搜索关键词', 'info');
        return;
      }
      
      this.lastSearchQuery = this.searchQuery.trim();
      this.searchPerformed = true;
      
      const resultCount = this.filteredNewsItems.length;
      this.showToast(`找到 ${resultCount} 条相关结果`, 'success');
    },
    
    searchByTag(tag) {
      this.searchQuery = tag;
      this.lastSearchQuery = tag;
      this.searchPerformed = true;
  
      const resultCount = this.filteredNewsItems.length;
      this.showToast(`找到 ${resultCount} 条与“${tag}”相关的结果`, resultCount > 0 ? 'success' : 'info');
    },
    
    clearSearch() {
      this.searchQuery = '';
      this.lastSearchQuery = '';
      this.searchPerformed = false;
      this.showToast('已清除搜索', 'info');
    },
    
    // 高亮搜索关键词
    highlightText(text) {
      if (!this.searchPerformed || !this.lastSearchQuery || !text) return text;
      
      const regex = new RegExp(`(${this.lastSearchQuery})`, 'gi');
      return text.replace(regex, '<mark class="search-highlight">$1</mark>');
    },
    
    // ========== 点赞功能 ==========
    toggleLike(item) {
      item.isLiked = !item.isLiked;
      if (item.isLiked) {
        item.likes += 1;
      } else {
        item.likes -= 1;
      }
    },
    
    // ========== 智能分享功能 ==========
    async shareItem(item) {
      const shareData = {
        title: item.shareTitle || item.title,
        text: `【反诈提醒】${item.summary} 查看详情：`,
        url: item.shareUrl || `https://fan-zha.com/news/${item.id}`
      };
      
      if (navigator.share && navigator.canShare && navigator.canShare(shareData)) {
        try {
          await navigator.share(shareData);
          this.showToast('分享成功', 'success');
        } catch (error) {
          if (error.name !== 'AbortError') {
            console.error('分享失败:', error);
            this.fallbackShare(item);
          }
        }
      } else {
        this.fallbackShare(item);
      }
    },
    
    // 降级分享：复制链接
    fallbackShare(item) {
      const url = item.shareUrl || `https://fan-zha.com/news/${item.id}`;
      
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(() => {
          this.showToast('链接已复制到剪贴板，可分享给好友', 'success');
        }).catch(() => {
          this.fallbackCopy(url);
        });
      } else {
        this.fallbackCopy(url);
      }
    },
    
    fallbackCopy(text) {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      
      try {
        const successful = document.execCommand('copy');
        if (successful) {
          this.showToast('链接已复制到剪贴板', 'success');
        } else {
          this.showToast('复制失败，请手动复制', 'error');
        }
      } catch (err) {
        this.showToast('复制失败，请手动复制', 'error');
      }
      
      document.body.removeChild(textarea);
    },
    
    // ========== 评论弹窗功能 ==========
    openCommentModal(item) {
      this.currentNews = item;
      this.currentComments = [];
      this.commentsLoading = true;
      this.showCommentModal = true;
      this.newCommentText = '';
      
      setTimeout(() => {
        this.currentComments = (this.commentsDatabase[item.id] || []).map(c => ({...c}));
        this.commentsLoading = false;
        
        this.$nextTick(() => {
          const container = this.$refs.commentsContainer;
          if (container) container.scrollTop = 0;
        });
      }, 500);
    },
    
    closeCommentModal() {
      this.showCommentModal = false;
      this.currentNews = null;
      this.currentComments = [];
      this.newCommentText = '';
    },
    
    submitComment() {
      if (!this.newCommentText.trim() || this.submittingComment) return;
      if (this.newCommentText.length > 200) {
        this.showToast('评论不能超过200字', 'error');
        return;
      }
      
      this.submittingComment = true;
      
      setTimeout(() => {
        const newComment = {
          id: this.nextCommentId++,
          author: '当前用户',
          avatar: '',
          text: this.newCommentText.trim(),
          time: '刚刚',
          likes: 0,
          isLiked: false
        };
        
        this.currentComments.unshift(newComment);
        
        if (!this.commentsDatabase[this.currentNews.id]) {
          this.commentsDatabase[this.currentNews.id] = [];
        }
        this.commentsDatabase[this.currentNews.id].unshift(newComment);
        
        const newsItem = this.newsItems.find(n => n.id === this.currentNews.id);
        if (newsItem) {
          newsItem.comments += 1;
        }
        
        this.newCommentText = '';
        this.submittingComment = false;
        this.showToast('评论发布成功', 'success');
        
        this.$nextTick(() => {
          const container = this.$refs.commentsContainer;
          if (container) container.scrollTop = 0;
        });
      }, 800);
    },
    
    likeComment(comment) {
      comment.isLiked = !comment.isLiked;
      if (comment.isLiked) {
        comment.likes += 1;
      } else {
        comment.likes -= 1;
      }
    },
    
    replyToComment(comment) {
      this.newCommentText = `回复 @${comment.author}：`;
      this.$nextTick(() => {
        const textarea = document.querySelector('.comment-input-area textarea');
        if (textarea) {
          textarea.focus();
          textarea.setSelectionRange(this.newCommentText.length, this.newCommentText.length);
        }
      });
    },
    
    // ========== 浏览记录功能 ==========
    viewDetail(item) {
      this.addToHistory(item);
      this.showToast(`查看详情：${item.title}`, 'info');
    },
    
    viewHistoryItem(item) {
      const newsItem = this.newsItems.find(n => n.id === item.id) || 
                      { title: item.title, summary: '', id: item.id };
      this.viewDetail(newsItem);
    },
    
    addToHistory(item) {
      const existsIndex = this.historyItems.findIndex(h => h.id === item.id);
      if (existsIndex !== -1) {
        this.historyItems.splice(existsIndex, 1);
      }
      this.historyItems.unshift({
        id: item.id,
        title: item.title,
        time: '刚刚'
      });
      if (this.historyItems.length > 5) {
        this.historyItems.pop();
      }
    },
    
    clearHistory() {
      this.historyItems = [];
      this.showToast('浏览记录已清除', 'success');
    },
    
    openReport() {
      this.showToast('举报功能开发中，请拨打96110', 'info');
    },
    
    showToast(message, type = 'info') {
      this.toast = {
        show: true,
        message,
        type
      };
      
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
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
  background: #f8fafc;
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

.content-area {
  flex: 2;
  min-width: 0;
}

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

.hotline-card {
  background: linear-gradient(145deg, #f0f9ff, #e6f0fa);
  border: 1px solid #b9d9f0;
  padding: 16px;
}

.hotline-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 8px;
}

.hotline-icon {
  font-size: 28px;
  line-height: 1;
}

.hotline-text {
  text-align: left;
}

.hotline-text h4 {
  font-size: 18px;
  font-weight: 700;
  color: #0369a1;
  margin: 0 0 2px 0;
}

.hotline-text p {
  font-size: 22px;
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

/* 搜索高亮 */
.search-highlight {
  background-color: #fff3cd;
  color: #856404;
  padding: 0 2px;
  border-radius: 4px;
  font-weight: 600;
}

.search-result-info {
  margin-top: 12px;
  padding: 8px 12px;
  background: #e6f7ff;
  border-radius: 30px;
  font-size: 14px;
  color: #0066b3;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.clear-search {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 16px;
  padding: 0 4px;
}

.clear-search:hover {
  color: #dc2626;
}

.no-results {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 20px;
  color: #94a3b8;
  font-size: 16px;
  border: 1px dashed #cbd5e1;
}

/* ========== 评论弹窗样式 ========== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.comment-modal {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 520px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modal-slide-up 0.3s ease;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 1px solid #eef2f6;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  max-width: 350px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.close-modal {
  background: none;
  border: none;
  font-size: 28px;
  line-height: 1;
  color: #94a3b8;
  cursor: pointer;
  padding: 0 8px;
  transition: color 0.2s;
}

.close-modal:hover {
  color: #dc2626;
}

.comments-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  min-height: 200px;
  max-height: 400px;
  background: #ffffff;
}

.comments-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px 0;
  color: #64748b;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

.no-comments {
  text-align: center;
  padding: 40px 0;
  color: #94a3b8;
  font-size: 14px;
}

.comment-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  animation: comment-fade-in 0.3s ease;
}

.comment-avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 20px;
  font-weight: 500;
}

.comment-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.comment-content {
  flex: 1;
  background: #f8fafc;
  padding: 12px 16px;
  border-radius: 16px;
  border-top-left-radius: 4px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.comment-author {
  font-weight: 600;
  font-size: 14px;
  color: #0f172a;
}

.comment-time {
  font-size: 11px;
  color: #94a3b8;
}

.comment-text {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #1e293b;
  line-height: 1.5;
  word-break: break-word;
}

.comment-actions {
  display: flex;
  gap: 16px;
}

.comment-like, .comment-reply {
  background: none;
  border: none;
  padding: 4px 0;
  font-size: 12px;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}

.comment-like:hover, .comment-reply:hover {
  color: #2563eb;
}

/* 修复评论输入区域 - 增强版 */
.comment-input-area {
  border-top: 1px solid #eef2f6;
  padding: 20px;
  background: #fafcfc;
  flex-shrink: 0;
}

.comment-input-area textarea {
  width: 100%;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 14px 16px;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  outline: none;
  transition: all 0.2s;
  box-sizing: border-box;
  background: white;
  line-height: 1.5;
}

.comment-input-area textarea:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}

.comment-actions-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding: 0 4px;
}

.comment-length {
  font-size: 13px;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 30px;
}

.submit-comment {
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px 28px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 110px;
  box-shadow: 0 2px 8px rgba(37,99,235,0.25);
  letter-spacing: 0.3px;
}

.submit-comment:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(37,99,235,0.35);
}

.submit-comment:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
  transform: none;
}

/* 头像加载失败的备用样式 */
.comment-avatar.avatar-fallback {
  background: #2563eb;
  color: white;
  font-size: 18px;
  font-weight: 500;
  line-height: 40px;
  text-align: center;
}

.comment-avatar.avatar-fallback img {
  display: none;
}

.comment-avatar.avatar-fallback::before {
  content: attr(data-initial);
}

/* ========== 全局提示样式 ========== */
.global-toast {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 50px;
  background: white;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
  font-size: 14px;
  font-weight: 500;
  z-index: 2000;
  border-left: 4px solid;
  max-width: 80%;
  text-align: center;
  animation: toast-slide-up 0.3s ease;
}

.global-toast.info {
  border-left-color: #2563eb;
  color: #1e293b;
}

.global-toast.success {
  border-left-color: #10b981;
  color: #065f46;
}

.global-toast.error {
  border-left-color: #dc2626;
  color: #991b1b;
}

/* ========== 动画 ========== */
@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes modal-slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes comment-fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes toast-slide-up {
  from {
    opacity: 0;
    transform: translate(-50%, 20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}
</style>