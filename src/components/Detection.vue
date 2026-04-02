
<template>
  <div class="fraud-platform">
    <!-- 左侧导航栏 (保持不变) -->
    <div class="sidebar">
      <div class="logo-area">
        <i class="fas fa-shield-alt"></i>
        <span>检测平台</span>
      </div>
      
      <div class="nav-menu">
        <div 
          v-for="item in navItems" 
          :key="item.id"
          class="nav-item"
          :class="{ active: currentNav === item.id }"
          @click="currentNav = item.id"
        >
          <i :class="item.icon"></i>
          <span>{{ item.name }}</span>
        </div>
      </div>
      
    </div>

    <!-- 右侧主内容区 - 移除了上边距，与顶部导航栏相接 -->
    <div class="main-content main-content-no-gap">
      
      <!-- ==================== 检测中心 ==================== -->
      <div v-if="currentNav === 'detect'" class="content-page">
        <div class="detect-layout">
          <!-- 左侧上传/输入区域 -->
          <div class="upload-section">
            <div class="section-card">
              <div class="section-header-balanced">
                <h3 class="section-title-large"><i class="fas fa-cloud-upload-alt"></i> 文件上传</h3>
              </div>
              
              <!-- ==================== 文件类型选择器 ==================== -->
              <!-- 功能说明：用户选择检测对象的类型（文本/图片/音频/视频） -->
              <!-- 接入说明：如需增加新的检测类型，在 fileTypes 数组中添加即可 -->
              <div class="file-type-selector">
                <label>检测对象：</label>
                <div class="type-buttons">
                  <button 
                    v-for="type in fileTypes" 
                    :key="type.value"
                    class="type-btn"
                    :class="{ active: selectedFileType === type.value }"
                    @click="selectedFileType = type.value"
                  >
                    <i :class="type.icon"></i>
                    {{ type.name }}
                  </button>
                </div>
              </div>

              <!-- ==================== 图片子类选择 ==================== -->
              <!-- 功能说明：仅当选择图片类型时显示，用于区分人脸照片和聊天记录截图 -->
              <!-- 接入说明：如需增加新的图片子类，在 subtype-options 中添加即可 -->
              <div v-if="selectedFileType === 'image'" class="subtype-selector">
                <label>图片类型：</label>
                <div class="subtype-options">
                  <label class="radio-label">
                    <input type="radio" value="face" v-model="imageSubtype" />
                    <i class="fas fa-user"></i> 人脸照片
                  </label>
                  <label class="radio-label">
                    <input type="radio" value="chat" v-model="imageSubtype" />
                    <i class="fas fa-comments"></i> 聊天记录截图
                  </label>
                </div>
              </div>

              <!-- ==================== 检测模型选择器 ==================== -->
              <!-- 功能说明：用户可以选择不同的检测模型，针对不同内容优化检测效果 -->
              <!-- 接入说明：如需增加新的检测模型，在 model-select 的 option 中添加即可 -->
              <div class="model-selector">
                <label>检测模型：</label>
                <select v-model="selectedModel" class="model-select">
                  <option value="standard">人脸检测专精模型</option>
                  <option value="deep">深度伪造专精模型</option>
                  <option value="face">聊天记录检测模型</option>
                  <option value="text">文本语义分析模型</option>
                  <option value="audio">音频伪造检测模型</option>
                </select>
              </div>

              <!-- ==================== 文本输入区域 ==================== -->
              <!-- 功能说明：当选择文本类型时，显示文本输入框，用户可直接输入文本内容 -->
              <!-- 接入说明：文本内容通过 textContent 变量获取，可在此处添加文本预处理逻辑 -->
              <!-- 限制：最多500字，可通过 maxlength 属性调整 -->
              <div v-if="selectedFileType === 'text'" class="text-input-section">
                <label>请输入要检测的文本内容：</label>
                <div class="text-input-container">
                  <textarea 
                    v-model="textContent" 
                    placeholder="请输入要检测的文本内容（最多500字）..."
                    maxlength="500"
                    class="text-input-area"
                  ></textarea>
                  <span class="text-counter">{{ textContent.length }}/500</span>
                </div>
              </div>

              <!-- ==================== 文件上传区域 ==================== -->
              <!-- 功能说明：当选择图片/音频/视频时，显示文件上传区域 -->
              <!-- 接入说明：
                   1. accept="*/*" 表示接受所有类型，实际类型限制在 addFiles 方法中实现
                   2. 如需限制特定文件类型，可修改 accept 属性，如 accept="image/*,audio/*,video/*"
                   3. 支持拖拽上传和点击上传两种方式
                   4. 最多支持10个文件，可通过修改 addFiles 中的判断条件调整
              -->
              <div v-else class="upload-area" @dragover.prevent @drop.prevent="handleDrop">
                <input 
                  type="file" 
                  ref="fileInput" 
                  @change="handleFileSelect" 
                  accept="*/*"
                  class="file-input"
                  multiple
                />
                <div class="upload-content">
                  <i class="fas fa-cloud-upload-alt"></i>
                  <p>点击或拖拽文件到此区域上传</p>
                  <span class="upload-hint">支持图片、音频、视频文件，最多10个文件</span>
                  <button class="select-file-btn" @click="$refs.fileInput.click()">
                    选择文件
                  </button>
                </div>
              </div>

              <!-- ==================== 已选文件列表 ==================== -->
              <!-- 功能说明：显示已上传的文件列表，包含预览功能 -->
              <!-- 接入说明：
                   1. uploadedFiles 数组存储已上传的文件信息
                   2. 每个文件对象包含：name(文件名), size(文件大小), type(文件类型), file(原始File对象), previewUrl(预览URL)
                   3. 预览功能支持图片、视频、音频，如需支持其他格式可扩展
              -->
              <div v-if="selectedFileType !== 'text' && uploadedFiles.length > 0" class="file-list">
                <div v-for="(file, index) in uploadedFiles" :key="index" class="file-item">
                  <div class="file-preview">
                    <!-- 图片预览 -->
                    <img v-if="file.type === 'image' && file.previewUrl" :src="file.previewUrl" class="preview-image" alt="预览">
                    <!-- 视频预览 -->
                    <video v-else-if="file.type === 'video' && file.previewUrl" :src="file.previewUrl" class="preview-video" controls></video>
                    <!-- 音频预览 -->
                    <audio v-else-if="file.type === 'audio' && file.previewUrl" :src="file.previewUrl" class="preview-audio" controls></audio>
                    <!-- 默认图标 -->
                    <i v-else :class="getFileIcon(file.type)" class="file-icon-large"></i>
                  </div>
                  <div class="file-info">
                    <span class="file-name">{{ file.name }}</span>
                    <span class="file-size">{{ formatFileSize(file.size) }}</span>
                  </div>
                  <button class="remove-file" @click="removeFile(index)">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
              </div>

              <!-- ==================== 操作按钮 ==================== -->
              <!-- 功能说明：开始检测和清空按钮 -->
              <!-- 接入说明：开始检测按钮的启用条件由 canStartDetection 计算属性控制 -->
              <div class="upload-actions">
                <button class="start-detect-btn" @click="startDetection" :disabled="!canStartDetection">
                  <i class="fas fa-play"></i> 开始检测
                </button>
                <button class="clear-btn" @click="clearAll">
                  <i class="fas fa-trash-alt"></i> 清空
                </button>
              </div>
            </div>
          </div>

          <!-- 右侧结果区域 -->
          <div class="result-section">
            <div class="section-card result-card">
              <div class="section-header-balanced">
                <h3 class="section-title-large"><i class="fas fa-chart-bar"></i> 检测结果</h3>
                <div class="result-header-actions">
                  <span class="date-badge"><i class="far fa-calendar"></i> {{ currentDate }}</span>
                  <!-- 导出报告按钮 - 仅当有检测结果时显示 -->
                  <button v-if="hasResult" class="export-report-btn" @click="exportReport">
                    <i class="fas fa-file-export"></i> 导出报告
                  </button>
                </div>
              </div>

              <!-- 检测中动画 -->
              <div v-if="isDetecting" class="detecting-animation">
                <div class="detecting-spinner">
                  <div class="spinner"></div>
                </div>
                <h4>正在检测中...</h4>
                <p>正在进行多模态深度分析，请稍候</p>
                <div class="detecting-progress">
                  <div class="progress-steps">
                    <div class="progress-step" :class="{ active: detectStep >= 1 }">
                      <i class="fas fa-file-upload"></i>
                      <span>文件解析</span>
                    </div>
                    <div class="progress-step" :class="{ active: detectStep >= 2 }">
                      <i class="fas fa-microscope"></i>
                      <span>特征提取</span>
                    </div>
                    <div class="progress-step" :class="{ active: detectStep >= 3 }">
                      <i class="fas fa-brain"></i>
                      <span>模型分析</span>
                    </div>
                    <div class="progress-step" :class="{ active: detectStep >= 4 }">
                      <i class="fas fa-chart-bar"></i>
                      <span>生成报告</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 未检测时的说明 -->
              <div v-else-if="!hasResult" class="empty-result">
                <div class="empty-illustration">
                  <i class="fas fa-microscope"></i>
                </div>
                <h4>开始您的第一次检测</h4>
                
                <!-- 功能特点展示 -->
                <div class="feature-description-result">
                  <div class="feature-item">
                    <span class="feature-dot"></span>
                    <div class="feature-text">
                      <strong>多模态识别</strong>
                      <span>支持文本、图像、音频、视频文件，跨模态交叉验证</span>
                    </div>
                  </div>
                  <div class="feature-item">
                    <span class="feature-dot"></span>
                    <div class="feature-text">
                      <strong>深度伪造检测</strong>
                      <span>AI换脸、语音合成识别，GAN生成内容检测</span>
                    </div>
                  </div>
                  <div class="feature-item">
                    <span class="feature-dot"></span>
                    <div class="feature-text">
                      <strong>数据分析</strong>
                      <span>生成详细检测报告，包含模型解释性文本，分析伪造痕迹</span>
                    </div>
                  </div>
                  <div class="feature-item">
                    <span class="feature-dot"></span>
                    <div class="feature-text">
                      <strong>结果导出</strong>
                      <span>支持PDF报告导出、JSON数据导出、结果分享</span>
                    </div>
                  </div>
                </div>

                <!-- 检测步骤说明 -->
                <div class="detect-steps">
                  <div class="step">
                    <span class="step-num">1</span>
                    <div class="step-content">
                      <strong>选择文件类型</strong>
                      <span>根据待检测内容选择对应类型，系统将采用专用模型进行分析，提高检测准确率。</span>
                    </div>
                  </div>
                  <div class="step">
                    <span class="step-num">2</span>
                    <div class="step-content">
                      <strong>上传文件或输入文本</strong>
                      <span>支持拖拽或点击上传文件，文本类型可直接输入内容。</span>
                    </div>
                  </div>
                  <div class="step">
                    <span class="step-num">3</span>
                    <div class="step-content">
                      <strong>开始检测</strong>
                      <span>系统进行多模态分析，包括元数据提取、特征比对、深度伪造检测等环节。</span>
                    </div>
                  </div>
                  <div class="step">
                    <span class="step-num">4</span>
                    <div class="step-content">
                      <strong>查看结果</strong>
                      <span>获取详细真伪报告，包含多维度的可信度评分和具体的伪造痕迹分析。</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 检测结果详情 -->
              <div v-else class="result-detail">
                <!-- 文件信息卡片 -->
                <div class="file-info-card">
                  <div class="file-icon">
                    <i :class="getFileIcon(currentResult.fileType)"></i>
                  </div>
                  <div class="file-details">
                    <div class="file-name">{{ currentResult.fileName }}</div>
                    <div class="file-meta">
                      <div class="meta-row">
                        <span class="meta-item">
                          <i class="far fa-calendar-alt"></i>
                          <span class="meta-text">{{ currentResult.detectTime }}</span>
                        </span>
                        <span class="meta-item">
                          <i class="far fa-file"></i>
                          <span class="meta-text file-size-text">{{ currentResult.fileSize }}</span>
                        </span>
                        <span class="meta-item">
                          <i class="fas fa-tag"></i>
                          <span class="meta-text">{{ currentResult.fileTypeName }}</span>
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="file-score" :class="getScoreClass(currentResult.overallScore)">
                    <div class="score-value">{{ currentResult.overallScore }}%</div>
                    <div class="score-label">可信度</div>
                  </div>
                </div>

                <!-- 分析标签页 -->
                <div class="analysis-tabs">
                  <button 
                    class="tab-btn" 
                    :class="{ active: activeAnalysisTab === 'overview' }"
                    @click="activeAnalysisTab = 'overview'"
                  >
                    概览
                  </button>
                  <button 
                    class="tab-btn" 
                    :class="{ active: activeAnalysisTab === 'details' }"
                    @click="activeAnalysisTab = 'details'"
                  >
                    详细分析
                  </button>
                  <button 
                    class="tab-btn" 
                    :class="{ active: activeAnalysisTab === 'features' }"
                    @click="activeAnalysisTab = 'features'"
                  >
                    特征分析
                  </button>
                </div>

                <!-- 概览内容 -->
                <div v-if="activeAnalysisTab === 'overview'" class="tab-content">
                  <div class="metrics-grid">
                    <div class="metric-item" v-for="metric in currentResult.metrics" :key="metric.name">
                      <div class="metric-header">
                        <span class="metric-name">{{ metric.name }}</span>
                        <span class="metric-value" :style="{ color: getMetricColor(metric.value) }">
                          {{ metric.value }}%
                        </span>
                      </div>
                      <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: metric.value + '%', backgroundColor: getMetricColor(metric.value) }"></div>
                      </div>
                      <div class="metric-desc">{{ metric.description }}</div>
                    </div>
                  </div>

                  <div v-if="currentResult.fileType === 'image'" class="image-analysis">
                    <div class="analysis-subtitle">
                      <i class="fas fa-image"></i> 图像分析细节
                    </div>
                    <div class="image-features">
                      <div class="feature" v-for="feature in currentResult.imageFeatures" :key="feature.name">
                        <i :class="feature.icon"></i>
                        <span>{{ feature.name }}: {{ feature.value }}</span>
                      </div>
                    </div>
                  </div>

                  <div v-if="currentResult.fileType === 'text'" class="text-analysis">
                    <div class="analysis-subtitle">
                      <i class="fas fa-font"></i> 文本分析细节
                    </div>
                    <div class="text-features">
                      <div class="feature" v-for="feature in currentResult.textFeatures" :key="feature.name">
                        <i :class="feature.icon"></i>
                        <span>{{ feature.name }}: {{ feature.value }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 详细分析内容 -->
                <div v-if="activeAnalysisTab === 'details'" class="tab-content">
                  <div class="detail-analysis">
                    <div class="analysis-section" v-for="section in currentResult.detailSections" :key="section.title">
                      <div class="section-title">{{ section.title }}</div>
                      <div class="section-items">
                        <div class="section-item" v-for="item in section.items" :key="item.label">
                          <span class="item-label">{{ item.label }}</span>
                          <span class="item-value" :class="item.status">{{ item.value }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 特征分析内容 -->
                <div v-if="activeAnalysisTab === 'features'" class="tab-content">
                  <div class="features-analysis">
                    <div class="feature-block" v-for="(feature, index) in currentResult.deepFeatures" :key="index">
                      <div class="feature-title">
                        <i :class="feature.icon"></i>
                        {{ feature.title }}
                      </div>
                      <div class="feature-desc">{{ feature.description }}</div>
                      <div class="feature-confidence">
                        准确度: 
                        <span class="accuracy-tag" :class="getAccuracyLevelClass(feature.confidence)">
                          {{ getAccuracyLevel(feature.confidence) }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ==================== 检测记录 ==================== -->
      <div v-if="currentNav === 'records'" class="content-page">
        <div class="filter-section">
          <div class="filter-header">
            <h3 class="filter-title"><i class="fas fa-filter"></i> 筛选条件</h3>
            <button class="export-records-btn" @click="exportRecords">
              <i class="fas fa-download"></i> 导出记录
            </button>
          </div>
          
          <div class="filter-grid">
            <div class="filter-item">
              <label>时间范围</label>
              <select v-model="tempFilters.timeRange">
                <option>今日</option>
                <option>近7天</option>
                <option>本月</option>
                <option>自定义</option>
              </select>
            </div>
            <div class="filter-item">
              <label>文件类型</label>
              <select v-model="tempFilters.fileType">
                <option>全部</option>
                <option>文本</option>
                <option>图片</option>
                <option>音频</option>
                <option>视频</option>
              </select>
            </div>
            <div class="filter-item">
              <label>检测结果</label>
              <select v-model="tempFilters.result">
                <option>全部</option>
                <option>可信</option>
                <option>疑似伪造</option>
                <option>待复核</option>
              </select>
            </div>
            <div class="filter-item">
              <label>图片子类</label>
              <select v-model="tempFilters.imageSubtype">
                <option>全部</option>
                <option>人脸</option>
                <option>聊天记录</option>
              </select>
            </div>
            <div class="filter-item search-item">
              <label>搜索</label>
              <div class="search-box">
                <i class="fas fa-search"></i>
                <input type="text" placeholder="输入文件名搜索" v-model="tempFilters.search">
              </div>
            </div>
            <div class="filter-item buttons-item">
              <button class="search-btn" @click="applyFilters">
                <i class="fas fa-search"></i> 查询
              </button>
              <button class="reset-btn" @click="resetFilters">
                <i class="fas fa-undo"></i> 重置
              </button>
            </div>
          </div>
        </div>

        <div class="records-table-container">
          <table class="records-table">
            <thead>
              <tr>
                <th>文件名</th>
                <th>文件类型</th>
                <th>子类</th>
                <th>检测时间</th>
                <th>可信度</th>
                <th>结果</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in paginatedRecords" :key="record.id">
                <td>
                  <div class="file-cell">
                    <i :class="getFileIcon(record.type)"></i>
                    <span>{{ record.name }}</span>
                  </div>
                </td>
                <td><span class="badge type">{{ record.type }}</span></td>
                <td><span v-if="record.subtype" class="badge subtype">{{ record.subtype }}</span></td>
                <td>{{ record.time }}</td>
                <td>
                  <div class="score-cell">
                    <span class="score-text">{{ record.score }}%</span>
                    <div class="score-bar">
                      <div class="score-fill" :style="{ width: record.score + '%', backgroundColor: getScoreColor(record.score) }"></div>
                    </div>
                  </div>
                </td>
                <td>
                  <span :class="['badge', 'result', record.resultClass]">{{ record.resultText }}</span>
                </td>
                <td>
                  <button class="action-btn" title="查看详情" @click="viewRecordDetail(record)">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button class="action-btn" title="重新检测" @click="redetectFile(record)">
                    <i class="fas fa-sync-alt"></i>
                  </button>
                  <button class="action-btn" title="导出报告" @click="exportSingleReport(record)">
                    <i class="fas fa-download"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="paginatedRecords.length === 0">
                <td colspan="7" class="empty-table">暂无符合条件的记录</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination" v-if="filteredRecords.length > 0">
          <div class="pagination-info">
            显示 {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, filteredRecords.length) }} 条，共 {{ filteredRecords.length }} 条记录
          </div>
          <div class="pagination-controls">
            <button @click="currentPage = 1" :disabled="currentPage === 1">
              <i class="fas fa-angle-double-left"></i>
            </button>
            <button @click="currentPage--" :disabled="currentPage === 1">
              <i class="fas fa-chevron-left"></i>
            </button>
            
            <button 
              v-for="page in displayedPages" 
              :key="page"
              @click="currentPage = page"
              :class="{ active: currentPage === page }"
            >
              {{ page }}
            </button>
            
            <button @click="currentPage++" :disabled="currentPage === totalPages">
              <i class="fas fa-chevron-right"></i>
            </button>
            <button @click="currentPage = totalPages" :disabled="currentPage === totalPages">
              <i class="fas fa-angle-double-right"></i>
            </button>
          </div>
          <div class="pagination-go">
            <span>跳至</span>
            <input type="number" v-model.number="jumpPage" min="1" :max="totalPages" @keyup.enter="goToPage">
            <span>页</span>
          </div>
        </div>
      </div>

      <!-- ==================== 数据统计 ==================== -->
      <div v-if="currentNav === 'statistics'" class="content-page">
        <div class="stats-overview">
          <div class="stat-card">
            <div class="stat-icon blue">
              <i class="fas fa-file-alt"></i>
            </div>
            <div class="stat-content">
              <div class="stat-label">累计检测</div>
              <div class="stat-value">1,247</div>
              <div class="stat-trend">本月 +128</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon green">
              <i class="fas fa-check-circle"></i>
            </div>
            <div class="stat-content">
              <div class="stat-label">可信文件</div>
              <div class="stat-value">1,082</div>
              <div class="stat-trend">占比 86.8%</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon orange">
              <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="stat-content">
              <div class="stat-label">疑似伪造</div>
              <div class="stat-value">124</div>
              <div class="stat-trend">占比 9.9%</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon purple">
              <i class="fas fa-clock"></i>
            </div>
            <div class="stat-content">
              <div class="stat-label">待复核</div>
              <div class="stat-value">41</div>
              <div class="stat-trend">占比 3.3%</div>
            </div>
          </div>
        </div>

        <div class="charts-grid">
          <div class="chart-card">
            <div class="chart-header">
              <h4><i class="fas fa-chart-line"></i> 检测趋势（近30天）</h4>
              <select class="time-range-select" v-model="trendRange">
                <option>近7天</option>
                <option>近30天</option>
                <option>近90天</option>
              </select>
            </div>
            <div class="chart-wrapper">
              <div ref="trendChart" class="chart-container" style="width:100%; height:250px;"></div>
              <div v-if="chartError.trend" class="chart-error">
                <i class="fas fa-exclamation-triangle"></i>
                <span>图表加载失败，请刷新重试</span>
              </div>
            </div>
          </div>

          <div class="chart-card">
            <div class="chart-header">
              <h4><i class="fas fa-chart-pie"></i> 文件类型分布</h4>
            </div>
            <div class="chart-wrapper">
              <div ref="pieChart" class="chart-container" style="width:100%; height:250px;"></div>
              <div v-if="chartError.pie" class="chart-error">
                <i class="fas fa-exclamation-triangle"></i>
                <span>图表加载失败，请刷新重试</span>
              </div>
            </div>
          </div>

          <div class="chart-card full-width">
            <div class="chart-header">
              <h4><i class="fas fa-chart-bar"></i> 各类文件检测结果</h4>
            </div>
            <div class="chart-wrapper">
              <div ref="barChart" class="chart-container" style="width:100%; height:300px;"></div>
              <div v-if="chartError.bar" class="chart-error">
                <i class="fas fa-exclamation-triangle"></i>
                <span>图表加载失败，请刷新重试</span>
              </div>
            </div>
          </div>
        </div>

        <div class="stats-habits">
          <div class="habit-card">
            <h4><i class="fas fa-clock"></i> 常用检测时段</h4>
            <div class="time-distribution">
              <div class="time-slot">
                <span>00:00 - 08:00</span>
                <div class="slot-bar">
                  <div class="slot-fill" style="width: 12%"></div>
                </div>
                <span>12%</span>
              </div>
              <div class="time-slot">
                <span>08:00 - 12:00</span>
                <div class="slot-bar">
                  <div class="slot-fill" style="width: 28%"></div>
                </div>
                <span>28%</span>
              </div>
              <div class="time-slot">
                <span>12:00 - 18:00</span>
                <div class="slot-bar">
                  <div class="slot-fill" style="width: 35%"></div>
                </div>
                <span>35%</span>
              </div>
              <div class="time-slot">
                <span>18:00 - 24:00</span>
                <div class="slot-bar">
                  <div class="slot-fill" style="width: 25%"></div>
                </div>
                <span>25%</span>
              </div>
            </div>
          </div>
          <div class="habit-card">
            <h4><i class="fas fa-chart-simple"></i> 常用检测类型</h4>
            <div class="type-ranking">
              <div class="rank-item">
                <span class="rank-num rank-1">1</span>
                <span class="rank-type">图片</span>
                <span class="rank-count">486次</span>
                <div class="rank-bar">
                  <div class="rank-bar-fill" style="width: 86%"></div>
                </div>
              </div>
              <div class="rank-item">
                <span class="rank-num rank-2">2</span>
                <span class="rank-type">文本</span>
                <span class="rank-count">352次</span>
                <div class="rank-bar">
                  <div class="rank-bar-fill" style="width: 62%"></div>
                </div>
              </div>
              <div class="rank-item">
                <span class="rank-num rank-3">3</span>
                <span class="rank-type">音频</span>
                <span class="rank-count">247次</span>
                <div class="rank-bar">
                  <div class="rank-bar-fill" style="width: 44%"></div>
                </div>
              </div>
              <div class="rank-item">
                <span class="rank-num rank-4">4</span>
                <span class="rank-type">视频</span>
                <span class="rank-count">162次</span>
                <div class="rank-bar">
                  <div class="rank-bar-fill" style="width: 29%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ==================== 意见反馈 ==================== -->
      <div v-if="currentNav === 'feedback'" class="content-page">
        <div class="feedback-layout">
          <div class="feedback-form-section">
            <div class="form-card">
              <div class="section-header-balanced">
                <h3 class="section-title-large"><i class="fas fa-edit"></i> 提交反馈</h3>
              </div>
              
              <div class="form-group">
                <label>反馈类型 <span class="required">*</span></label>
                <div class="feedback-type-options">
                  <label class="type-option" :class="{ active: feedback.type === 'suggestion' }">
                    <input type="radio" name="feedbackType" value="suggestion" v-model="feedback.type">
                    <i class="fas fa-lightbulb"></i>
                    <span>功能建议</span>
                  </label>
                  <label class="type-option" :class="{ active: feedback.type === 'bug' }">
                    <input type="radio" name="feedbackType" value="bug" v-model="feedback.type">
                    <i class="fas fa-bug"></i>
                    <span>问题报告</span>
                  </label>
                  <label class="type-option" :class="{ active: feedback.type === 'question' }">
                    <input type="radio" name="feedbackType" value="question" v-model="feedback.type">
                    <i class="fas fa-question-circle"></i>
                    <span>使用咨询</span>
                  </label>
                  <label class="type-option" :class="{ active: feedback.type === 'other' }">
                    <input type="radio" name="feedbackType" value="other" v-model="feedback.type">
                    <i class="fas fa-ellipsis-h"></i>
                    <span>其他</span>
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label>关联检测（选填）</label>
                <select v-model="feedback.relatedFile">
                  <option value="">请选择关联的检测记录</option>
                  <option value="1">身份证照片.jpg - 2026-03-02</option>
                  <option value="2">通话录音.mp3 - 2026-03-01</option>
                  <option value="3">聊天截图.png - 2026-02-28</option>
                </select>
              </div>

              <div class="form-group with-counter">
                <label>反馈标题 <span class="required">*</span></label>
                <input 
                  type="text" 
                  v-model="feedback.title" 
                  placeholder="例：人脸检测结果不准确"
                  maxlength="100"
                  class="full-width-input"
                >
                <span class="char-counter">{{ feedback.title.length }}/100</span>
              </div>

              <div class="form-group with-counter">
                <label>详细描述 <span class="required">*</span></label>
                <textarea 
                  v-model="feedback.description" 
                  rows="5"
                  placeholder="请详细描述您遇到的问题或建议..."
                  maxlength="500"
                  class="full-width-textarea"
                ></textarea>
                <span class="char-counter">{{ feedback.description.length }}/500</span>
              </div>

              <div class="form-group">
                <label>附件上传（选填）</label>
                <div class="attachment-upload">
                  <input type="file" ref="attachmentInput" @change="handleAttachment" accept="image/*" multiple style="display: none;">
                  <button type="button" class="upload-btn" @click="$refs.attachmentInput.click()">
                    <i class="fas fa-cloud-upload-alt"></i> 点击上传截图
                  </button>
                  <span class="upload-hint">支持JPG、PNG格式，最多5张，每张不超过5MB</span>
                </div>
                <div v-if="attachments.length > 0" class="attachment-list">
                  <div v-for="(file, index) in attachments" :key="index" class="attachment-item">
                    <i class="fas fa-image"></i>
                    <span class="name">{{ file.name }}</span>
                    <span class="size">{{ formatFileSize(file.size) }}</span>
                    <button class="remove" @click="removeAttachment(index)">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label>联系方式</label>
                <input 
                  type="text" 
                  v-model="feedback.contact" 
                  placeholder="邮箱或手机号，便于我们回复您"
                  class="full-width-input"
                >
              </div>

              <div class="form-actions">
                <button class="submit-btn" @click="submitFeedback">
                  <i class="fas fa-paper-plane"></i> 提交反馈
                </button>
                <button class="reset-btn" @click="resetFeedback">
                  <i class="fas fa-undo"></i> 清空
                </button>
              </div>
            </div>
          </div>

          <div class="feedback-history-section">
            <div class="history-card">
              <div class="section-header-balanced">
                <h3 class="section-title-large"><i class="fas fa-history"></i> 我的反馈记录</h3>
              </div>
              
              <div class="history-list">
                <div v-for="item in userFeedbackHistory" :key="item.id" class="history-item">
                  <div class="history-header">
                    <span class="feedback-type" :class="item.typeClass">
                      <i :class="item.typeIcon"></i> {{ item.typeText }}
                    </span>
                    <span class="feedback-status" :class="item.statusClass">
                      {{ item.statusText }}
                    </span>
                  </div>
                  <div class="feedback-title">{{ item.title }}</div>
                  <div class="feedback-time">{{ item.time }}</div>
                  <div v-if="item.reply" class="feedback-reply">
                    <i class="fas fa-reply"></i>
                    <div class="reply-content">
                      <span class="reply-label">官方回复：</span>
                      {{ item.reply }}
                    </div>
                  </div>
                </div>
              </div>

              <div class="view-more">
                <a href="#">查看全部反馈记录 <i class="fas fa-arrow-right"></i></a>
              </div>
            </div>

            <div class="tip-card">
              <h4><i class="fas fa-lightbulb"></i> 反馈提示</h4>
              <ul>
                <li><i class="fas fa-check-circle"></i> 功能建议：告诉我们您希望增加的功能</li>
                <li><i class="fas fa-check-circle"></i> 问题报告：检测结果异常或系统错误</li>
                <li><i class="fas fa-check-circle"></i> 使用咨询：对检测功能有疑问</li>
                <li><i class="fas fa-check-circle"></i> 我们会在24小时内回复您的反馈</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- ==================== 使用指南 ==================== -->
      <div v-if="currentNav === 'guide'" class="content-page">
        <div class="guide-content">
          <div class="guide-section">
            <div class="section-header-balanced">
              <h3 class="section-title-large"><i class="fas fa-rocket"></i> 快速入门</h3>
            </div>
            <div class="steps-grid">
              <div class="step-card">
                <div class="step-number">1</div>
                <i class="fas fa-file-upload"></i>
                <h4>上传文件</h4>
                <p>支持拖拽或点击上传，单次最多10个文件，支持多种格式</p>
              </div>
              <div class="step-card">
                <div class="step-number">2</div>
                <i class="fas fa-sliders-h"></i>
                <h4>选择类型</h4>
                <p>指定文件类型，提高检测准确率，可选用专精检测模型</p>
              </div>
              <div class="step-card">
                <div class="step-number">3</div>
                <i class="fas fa-play"></i>
                <h4>开始检测</h4>
                <p>点击检测按钮，系统自动进行多模态深度分析</p>
              </div>
              <div class="step-card">
                <div class="step-number">4</div>
                <i class="fas fa-chart-bar"></i>
                <h4>查看结果</h4>
                <p>获取详细的真伪分析报告，包含多维度的可信度评分</p>
              </div>
            </div>
          </div>

          <div class="guide-section">
            <div class="section-header-balanced">
              <h3 class="section-title-large"><i class="fas fa-file-alt"></i> 支持的文件类型</h3>
            </div>
            <div class="file-types-grid">
              <div class="file-type-card">
                <i class="fas fa-file-alt"></i>
                <h4>文本文件</h4>
                <ul>
                  <li>TXT、DOC、DOCX、PDF</li>
                  <li>最大100MB</li>
                  <li>支持语义分析</li>
                </ul>
              </div>
              <div class="file-type-card">
                <i class="fas fa-file-image"></i>
                <h4>图片文件</h4>
                <ul>
                  <li>JPG、PNG、BMP、GIF</li>
                  <li>人脸照片、聊天记录截图</li>
                  <li>最大50MB</li>
                </ul>
              </div>
              <div class="file-type-card">
                <i class="fas fa-file-audio"></i>
                <h4>音频文件</h4>
                <ul>
                  <li>MP3、WAV、AAC、M4A</li>
                  <li>支持语音伪造检测</li>
                  <li>最大200MB</li>
                </ul>
              </div>
              <div class="file-type-card">
                <i class="fas fa-file-video"></i>
                <h4>视频文件</h4>
                <ul>
                  <li>MP4、AVI、MOV、MKV</li>
                  <li>支持音视频同步检测</li>
                  <li>最大500MB</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="guide-section">
            <div class="section-header-balanced">
              <h3 class="section-title-large"><i class="fas fa-microscope"></i> 多模态识别技术</h3>
            </div>
            <div class="features-grid">
              <div class="feature-card">
                <i class="fas fa-brain"></i>
                <h4>深度伪造检测</h4>
                <p>基于深度学习算法，识别AI生成的虚假内容，包括DeepFake换脸、语音合成等</p>
              </div>
              <div class="feature-card">
                <i class="fas fa-fingerprint"></i>
                <h4>元数据分析</h4>
                <p>提取文件元数据，分析创建时间、修改记录、设备信息等，发现伪造痕迹</p>
              </div>
              <div class="feature-card">
                <i class="fas fa-wave-square"></i>
                <h4>噪声特征分析</h4>
                <p>分析图像和音频的噪声分布，识别异常的人工痕迹</p>
              </div>
              <div class="feature-card">
                <i class="fas fa-link"></i>
                <h4>一致性校验</h4>
                <p>检测多模态内容的一致性，如音视频同步、人脸与背景匹配度</p>
              </div>
              <div class="feature-card">
                <i class="fas fa-database"></i>
                <h4>跨模态比对</h4>
                <p>支持文本、图像、音频的交叉验证，发现语义不一致</p>
              </div>
              <div class="feature-card">
                <i class="fas fa-chart-line"></i>
                <h4>时序分析</h4>
                <p>分析视频帧间变化、音频频谱演化，检测异常跳变</p>
              </div>
            </div>
          </div>

          <div class="guide-section">
            <div class="section-header-balanced">
              <h3 class="section-title-large"><i class="fas fa-question-circle"></i> 常见问题</h3>
            </div>
            <div class="faq-list">
              <div class="faq-item" v-for="(faq, index) in faqs" :key="index">
                <div class="faq-question" @click="toggleFaq(index)">
                  <i class="fas fa-chevron-right" :class="{ rotated: activeFaq === index }"></i>
                  <span>{{ faq.question }}</span>
                </div>
                <div class="faq-answer" v-show="activeFaq === index">
                  {{ faq.answer }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import html2pdf from 'html2pdf.js';

export default {
  name: 'FraudDetectionPlatform',
  data() {
    return {
      // 导航项
      navItems: [
        { id: 'detect', name: '检测中心', icon: 'fas fa-search' },
        { id: 'records', name: '检测记录', icon: 'fas fa-history' },
        { id: 'statistics', name: '数据统计', icon: 'fas fa-chart-pie' },
        { id: 'feedback', name: '意见反馈', icon: 'fas fa-comment-dots' },
        { id: 'guide', name: '使用指南', icon: 'fas fa-book-open' }
      ],
      currentNav: 'detect',
      currentDate: new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '-'),
      
      // 检测中心数据
      fileTypes: [
        { value: 'text', name: '文本', icon: 'fas fa-file-alt' },
        { value: 'image', name: '图片', icon: 'fas fa-file-image' },
        { value: 'audio', name: '音频', icon: 'fas fa-file-audio' },
        { value: 'video', name: '视频', icon: 'fas fa-file-video' }
      ],
      selectedFileType: 'image',
      imageSubtype: 'face',
      selectedModel: 'standard',
      uploadedFiles: [],
      textContent: '',
      
      // 检测状态
      isDetecting: false,
      detectStep: 0,
      detectTimer: null,
      
      // 检测结果
      hasResult: false,
      currentResult: null,
      activeAnalysisTab: 'overview',
      
      // 检测记录筛选
      recordFilters: {
        timeRange: '近7天',
        fileType: '全部',
        result: '全部',
        imageSubtype: '全部',
        search: ''
      },
      tempFilters: {
        timeRange: '近7天',
        fileType: '全部',
        result: '全部',
        imageSubtype: '全部',
        search: ''
      },
      
      records: [
        { id: 1, name: '陌生来电录音.mp3', type: '音频', subtype: '', time: '2026-03-02 14:23', score: 23, resultClass: 'suspicious', resultText: '疑似伪造' },
        { id: 2, name: '身份证照片.jpg', type: '图片', subtype: '人脸', time: '2026-03-02 13:47', score: 97, resultClass: 'trust', resultText: '可信' },
        { id: 3, name: '微信聊天截图.png', type: '图片', subtype: '聊天记录', time: '2026-03-02 12:08', score: 45, resultClass: 'review', resultText: '待复核' },
        { id: 4, name: '诈骗短信.txt', type: '文本', subtype: '', time: '2026-03-02 11:32', score: 12, resultClass: 'suspicious', resultText: '疑似伪造' },
        { id: 5, name: '会议录像.mp4', type: '视频', subtype: '', time: '2026-03-02 09:55', score: 88, resultClass: 'trust', resultText: '可信' },
        { id: 6, name: '通话记录.txt', type: '文本', subtype: '', time: '2026-03-02 08:20', score: 76, resultClass: 'trust', resultText: '可信' },
        { id: 7, name: '会议录音.wav', type: '音频', subtype: '', time: '2026-03-01 16:30', score: 92, resultClass: 'trust', resultText: '可信' },
        { id: 8, name: '自拍照.jpg', type: '图片', subtype: '人脸', time: '2026-03-01 11:15', score: 98, resultClass: 'trust', resultText: '可信' },
        { id: 9, name: '短信截图.png', type: '图片', subtype: '聊天记录', time: '2026-03-01 09:42', score: 34, resultClass: 'suspicious', resultText: '疑似伪造' },
        { id: 10, name: '文档.docx', type: '文本', subtype: '', time: '2026-02-28 17:20', score: 95, resultClass: 'trust', resultText: '可信' },
        { id: 11, name: '视频通话.mp4', type: '视频', subtype: '', time: '2026-02-28 14:10', score: 67, resultClass: 'review', resultText: '待复核' },
        { id: 12, name: '语音消息.m4a', type: '音频', subtype: '', time: '2026-02-28 10:05', score: 81, resultClass: 'trust', resultText: '可信' },
      ],
      
      // 分页
      currentPage: 1,
      pageSize: 8,
      jumpPage: 1,
      
      // 图表相关
      trendRange: '近30天',
      trendChart: null,
      pieChart: null,
      barChart: null,
      chartError: {
        trend: false,
        pie: false,
        bar: false
      },
      chartData: {
        trend: [42, 38, 45, 52, 48, 63, 58, 71, 65, 82, 78],
        trendDates: ['03-01', '03-04', '03-07', '03-10', '03-13', '03-16', '03-19', '03-22', '03-25', '03-28', '03-31'],
        pieData: [
          { value: 486, name: '图片' },
          { value: 352, name: '文本' },
          { value: 247, name: '音频' },
          { value: 162, name: '视频' }
        ],
        barData: {
          categories: ['文本', '图片', '音频', '视频'],
          trust: [302, 418, 198, 124],
          suspicious: [32, 48, 32, 28],
          review: [18, 20, 17, 10]
        }
      },
      
      // 反馈表单
      feedback: {
        type: 'suggestion',
        relatedFile: '',
        title: '',
        description: '',
        contact: ''
      },
      attachments: [],
      
      // 用户反馈历史
      userFeedbackHistory: [
        {
          id: 1,
          type: 'suggestion',
          typeClass: 'type-suggestion',
          typeIcon: 'fas fa-lightbulb',
          typeText: '功能建议',
          title: '建议增加批量检测功能',
          time: '2026-02-28 14:30',
          status: 'replied',
          statusClass: 'status-replied',
          statusText: '已回复',
          reply: '感谢您的建议，批量检测功能正在开发中，预计下周上线。'
        },
        {
          id: 2,
          type: 'bug',
          typeClass: 'type-bug',
          typeIcon: 'fas fa-bug',
          typeText: '问题报告',
          title: '人脸检测结果不准确',
          time: '2026-02-25 09:15',
          status: 'processing',
          statusClass: 'status-processing',
          statusText: '处理中'
        }
      ],
      
      // 常见问题
      faqs: [
        {
          question: '检测结果的准确率有多高？',
          answer: '我们的检测系统经过大量数据训练，对常见类型的伪造检测准确率在95%以上。但请注意，没有任何检测系统能保证100%准确，建议结合其他证据综合判断。'
        },
        {
          question: '支持哪些文件格式？',
          answer: '支持文本（TXT、DOC、DOCX、PDF）、图片（JPG、PNG、BMP、GIF）、音频（MP3、WAV、AAC、M4A）、视频（MP4、AVI、MOV、MKV）等常见格式。'
        },
        {
          question: '检测需要多长时间？',
          answer: '检测时间取决于文件大小和类型，通常图片和文本在几秒内完成，音频和视频可能需要几十秒到几分钟。'
        },
        {
          question: '我的文件会上传到服务器吗？安全吗？',
          answer: '不会上传到服务器。所有检测均在本地完成，您的文件不会离开您的设备，确保数据隐私和安全。'
        },
        {
          question: '为什么有些文件检测结果显示"待复核"？',
          answer: '当系统对检测结果置信度不足时，会标记为"待复核"，由人工专家进行二次确认，通常在24小时内完成复核。'
        }
      ],
      activeFaq: null
    };
  },
  
  computed: {
    canStartDetection() {
      if (this.selectedFileType === 'text') {
        return this.textContent.trim().length > 0;
      }
      return this.uploadedFiles.length > 0;
    },
    
    filteredRecords() {
      let list = this.records;
      if (this.recordFilters.fileType !== '全部') {
        list = list.filter(item => item.type === this.recordFilters.fileType);
      }
      if (this.recordFilters.result !== '全部') {
        const map = { '可信': 'trust', '疑似伪造': 'suspicious', '待复核': 'review' };
        list = list.filter(item => item.resultClass === map[this.recordFilters.result]);
      }
      if (this.recordFilters.imageSubtype !== '全部' && this.recordFilters.fileType === '图片') {
        list = list.filter(item => item.subtype === this.recordFilters.imageSubtype);
      }
      if (this.recordFilters.search) {
        list = list.filter(item => item.name.toLowerCase().includes(this.recordFilters.search.toLowerCase()));
      }
      return list;
    },
    
    totalPages() {
      return Math.ceil(this.filteredRecords.length / this.pageSize);
    },
    
    paginatedRecords() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredRecords.slice(start, end);
    },
    
    displayedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
      
      let pages = [];
      
      if (total <= 7) {
        pages = Array.from({ length: total }, (_, i) => i + 1);
      } else {
        if (current <= 4) {
          pages = [1, 2, 3, 4, 5, '...', total];
        } else if (current >= total - 3) {
          pages = [1, '...', total - 4, total - 3, total - 2, total - 1, total];
        } else {
          pages = [1, '...', current - 1, current, current + 1, '...', total];
        }
      }
      
      return pages;
    }
  },
  
  watch: {
    currentNav: {
      handler(newVal) {
        if (newVal === 'statistics') {
          this.$nextTick(() => {
            setTimeout(() => {
              this.initCharts();
            }, 100);
          });
        } else {
          this.disposeCharts();
        }
      },
      immediate: true
    },
    
    trendRange() {
      if (this.currentNav === 'statistics' && this.trendChart) {
        this.updateTrendChart();
      }
    }
  },
  
  mounted() {
    window.addEventListener('resize', this.handleResize);
    
    if (this.currentNav === 'statistics') {
      setTimeout(() => {
        this.initCharts();
      }, 200);
    }
  },
  
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    this.disposeCharts();
    if (this.detectTimer) {
      clearInterval(this.detectTimer);
    }
    // 清理预览URL
    this.uploadedFiles.forEach(file => {
      if (file.previewUrl) {
        URL.revokeObjectURL(file.previewUrl);
      }
    });
  },
  
  methods: {
    // ==================== 图表相关方法 ====================
    initCharts() {
      console.log('开始初始化ECharts图表');
      
      this.chartError = {
        trend: false,
        pie: false,
        bar: false
      };
      
      this.initTrendChart();
      this.initPieChart();
      this.initBarChart();
    },
    
    initTrendChart() {
      const container = this.$refs.trendChart;
      if (!container) {
        console.warn('趋势图容器未找到');
        this.chartError.trend = true;
        return;
      }
      
      try {
        if (this.trendChart) {
          this.trendChart.dispose();
        }
        
        this.trendChart = echarts.init(container);
        
        const option = {
          tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(255,255,255,0.95)',
            borderColor: '#3b7cff',
            borderWidth: 2,
            textStyle: { color: '#1e293b', fontSize: 13 },
            formatter: function(params) {
              return params[0].name + '<br/>' +
                     `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#3b7cff;"></span>` +
                     `检测次数: ${params[0].value}次`;
            }
          },
          grid: {
            left: '8%',
            right: '5%',
            bottom: '10%',
            top: '10%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: this.chartData.trendDates,
            axisLabel: {
              color: '#64748b',
              fontSize: 12,
              rotate: this.chartData.trendDates.length > 10 ? 30 : 0
            },
            axisLine: { lineStyle: { color: '#e2e8f0' } },
            axisTick: { show: false }
          },
          yAxis: {
            type: 'value',
            name: '检测次数',
            nameTextStyle: { color: '#64748b', fontSize: 12 },
            axisLabel: { color: '#64748b', fontSize: 12 },
            splitLine: {
              lineStyle: { color: '#edf2f7', type: 'dashed' }
            }
          },
          series: [
            {
              name: '检测次数',
              type: 'line',
              data: this.chartData.trend,
              color: '#3b7cff',
              smooth: true,
              symbol: 'circle',
              symbolSize: 8,
              lineStyle: { width: 3 },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(59,124,255,0.3)' },
                  { offset: 1, color: 'rgba(59,124,255,0.05)' }
                ])
              },
              label: {
                show: true,
                position: 'top',
                color: '#3b7cff',
                fontSize: 12,
                fontWeight: 'bold',
                formatter: function(params) {
                  return params.value;
                }
              },
              emphasis: {
                focus: 'series',
                itemStyle: {
                  borderColor: '#fff',
                  borderWidth: 2
                }
              },
              markPoint: {
                data: [
                  { type: 'max', name: '最大值' },
                  { type: 'min', name: '最小值' }
                ]
              }
            }
          ]
        };
        
        this.trendChart.setOption(option);
        console.log('趋势图初始化成功');
      } catch (error) {
        console.error('趋势图初始化失败:', error);
        this.chartError.trend = true;
      }
    },
    
    initPieChart() {
      const container = this.$refs.pieChart;
      if (!container) {
        console.warn('饼图容器未找到');
        this.chartError.pie = true;
        return;
      }
      
      try {
        if (this.pieChart) {
          this.pieChart.dispose();
        }
        
        this.pieChart = echarts.init(container);
        
        const option = {
          tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(255,255,255,0.95)',
            borderColor: '#3b7cff',
            borderWidth: 2,
            textStyle: { color: '#1e293b', fontSize: 13 },
            formatter: function(params) {
              return `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${params.color};"></span>` +
                     `${params.name}<br/>` +
                     `数量: ${params.value}次<br/>` +
                     `占比: ${params.percent}%`;
            }
          },
          series: [
            {
              name: '文件类型分布',
              type: 'pie',
              radius: ['40%', '70%'],
              center: ['50%', '50%'],
              avoidLabelOverlap: true,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: true,
                position: 'outside',
                formatter: '{b}: {d}%',
                color: '#1e293b',
                fontSize: 12,
                fontWeight: 'normal'
              },
              labelLine: {
                length: 10,
                length2: 10,
                smooth: true
              },
              data: this.chartData.pieData.map(item => {
                let color = '#5470c6';
                if (item.name === '图片') color = '#91cc75';
                if (item.name === '音频') color = '#fac858';
                if (item.name === '视频') color = '#ee6666';
                return { ...item, itemStyle: { color } };
              }),
              emphasis: {
                scale: true,
                label: {
                  show: true,
                  fontWeight: 'bold',
                  fontSize: 14
                }
              }
            }
          ],
          legend: {
            show: false
          }
        };
        
        this.pieChart.setOption(option);
        console.log('饼图初始化成功');
      } catch (error) {
        console.error('饼图初始化失败:', error);
        this.chartError.pie = true;
      }
    },
    
    initBarChart() {
      const container = this.$refs.barChart;
      if (!container) {
        console.warn('柱状图容器未找到');
        this.chartError.bar = true;
        return;
      }
      
      try {
        if (this.barChart) {
          this.barChart.dispose();
        }
        
        this.barChart = echarts.init(container);
        
        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            backgroundColor: 'rgba(255,255,255,0.95)',
            borderColor: '#4198AC',
            borderWidth: 2,
            textStyle: { color: '#1e293b', fontSize: 13 },
            formatter: function(params) {
              let result = params[0].name + '<br/>';
              let total = 0;
              params.forEach(item => {
                total += item.value;
                result += `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${item.color};"></span>`;
                result += `${item.seriesName}: ${item.value}次<br/>`;
              });
              result += `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#4361ee;"></span>`;
              result += `总计: ${total}次`;
              return result;
            }
          },
          legend: {
            data: ['可信', '疑似伪造', '待复核'],
            bottom: 0,
            itemWidth: 14,
            itemHeight: 14,
            textStyle: { color: '#334155', fontSize: 13, fontWeight: 500 }
          },
          grid: {
            left: '8%',
            right: '5%',
            bottom: '18%',
            top: '10%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: this.chartData.barData.categories,
            axisLabel: { color: '#475569', fontSize: 13, fontWeight: 500 },
            axisLine: { lineStyle: { color: '#cbd5e1', width: 2 } },
            axisTick: { show: false }
          },
          yAxis: {
            type: 'value',
            name: '数量 (次)',
            nameTextStyle: { color: '#475569', fontSize: 13, fontWeight: 500 },
            axisLabel: { color: '#475569', fontSize: 12 },
            splitLine: {
              lineStyle: { color: '#e2e8f0', type: 'dashed', width: 1.5 }
            }
          },
          series: [
            {
              name: '可信',
              type: 'bar',
              data: this.chartData.barData.trust,
              color: '#4198AC', 
              barWidth: 50,
              itemStyle: {
                borderRadius: [8, 8, 0, 0],
                shadowColor: 'rgba(65, 152, 172, 0.3)',
                shadowBlur: 8,
                shadowOffsetY: 3
              },
              emphasis: {
                focus: 'series',
                itemStyle: {
                  shadowColor: 'rgba(65, 152, 172, 0.6)',
                  shadowBlur: 12,
                  shadowOffsetY: 5
                }
              },
              label: {
                show: true,
                position: 'top',
                color: '#4198AC',
                fontSize: 13,
                fontWeight: 'bold',
                formatter: function(params) {
                  return params.value;
                }
              }
            },
            {
              name: '疑似伪造',
              type: 'bar',
              data: this.chartData.barData.suspicious,
              color: '#ECB66C', 
              barWidth: 50,
              itemStyle: {
                borderRadius: [8, 8, 0, 0],
                shadowColor: 'rgba(236, 182, 108, 0.3)',
                shadowBlur: 8,
                shadowOffsetY: 3
              },
              emphasis: {
                focus: 'series',
                itemStyle: {
                  shadowColor: 'rgba(236, 182, 108, 0.6)',
                  shadowBlur: 12,
                  shadowOffsetY: 5
                }
              },
              label: {
                show: true,
                position: 'top',
                color: '#ECB66C',
                fontSize: 13,
                fontWeight: 'bold',
                formatter: function(params) {
                  return params.value;
                }
              }
            },
            {
              name: '待复核',
              type: 'bar',
              data: this.chartData.barData.review,
              color: '#ED8D5A',
              barWidth: 50,
              itemStyle: {
                borderRadius: [8, 8, 0, 0],
                shadowColor: 'rgba(237, 141, 90, 0.3)',
                shadowBlur: 8,
                shadowOffsetY: 3
              },
              emphasis: {
                focus: 'series',
                itemStyle: {
                  shadowColor: 'rgba(76, 201, 240, 0.6)',
                  shadowBlur: 12,
                  shadowOffsetY: 5
                }
              },
              label: {
                show: true,
                position: 'top',
                color: '#ED8D5A',
                fontSize: 13,
                fontWeight: 'bold',
                formatter: function(params) {
                  return params.value;
                }
              }
            }
          ]
        };
        
        this.barChart.setOption(option);
        console.log('柱状图初始化成功');
      } catch (error) {
        console.error('柱状图初始化失败:', error);
        this.chartError.bar = true;
      }
    },
    
    updateTrendChart() {
      let newData = [];
      let newDates = [];
      
      if (this.trendRange === '近7天') {
        newData = [42, 38, 45, 52, 48, 63, 58];
        newDates = ['03-01', '03-02', '03-03', '03-04', '03-05', '03-06', '今日'];
      } else if (this.trendRange === '近30天') {
        newData = [42, 38, 45, 52, 48, 63, 58, 71, 65, 82, 78];
        newDates = ['03-01', '03-04', '03-07', '03-10', '03-13', '03-16', '03-19', '03-22', '03-25', '03-28', '03-31'];
      } else {
        newData = [42, 38, 45, 52, 48, 63, 58, 71, 65, 82, 78, 85, 90, 88, 92];
        newDates = ['01', '05', '09', '13', '17', '21', '25', '29', '33', '37', '41', '45', '49', '53', '57'];
      }
      
      this.chartData.trend = newData;
      this.chartData.trendDates = newDates;
      
      if (this.trendChart) {
        this.trendChart.setOption({
          xAxis: { data: newDates },
          series: [{ 
            data: newData,
            label: {
              show: true,
              position: 'top',
              color: '#3b7cff',
              fontSize: 12,
              fontWeight: 'bold',
              formatter: function(params) {
                return params.value;
              }
            }
          }]
        });
      }
    },
    
    handleResize() {
      if (this.currentNav === 'statistics') {
        this.trendChart?.resize();
        this.pieChart?.resize();
        this.barChart?.resize();
      }
    },
    
    disposeCharts() {
      if (this.trendChart) {
        this.trendChart.dispose();
        this.trendChart = null;
      }
      if (this.pieChart) {
        this.pieChart.dispose();
        this.pieChart = null;
      }
      if (this.barChart) {
        this.barChart.dispose();
        this.barChart = null;
      }
    },
    
    // ==================== 文件上传相关 ====================
    handleDrop(e) {
      if (this.selectedFileType === 'text') return;
      const files = Array.from(e.dataTransfer.files);
      this.addFiles(files);
    },
    
    handleFileSelect(e) {
      if (this.selectedFileType === 'text') return;
      const files = Array.from(e.target.files);
      this.addFiles(files);
      e.target.value = '';
    },
    
    addFiles(files) {
      if (this.uploadedFiles.length + files.length > 10) {
        alert('最多只能上传10个文件');
        return;
      }
      
      files.forEach(file => {
        const fileType = this.getFileTypeFromMime(file.type);
        if (fileType && fileType === this.selectedFileType) {
          // 生成预览URL
          let previewUrl = null;
          if (fileType === 'image' || fileType === 'video' || fileType === 'audio') {
            previewUrl = URL.createObjectURL(file);
          }
          
          this.uploadedFiles.push({
            name: file.name,
            size: file.size,
            type: fileType,
            file: file,
            previewUrl: previewUrl
          });
        } else {
          alert(`文件类型不匹配，请上传${this.getFileTypeName(this.selectedFileType)}文件`);
        }
      });
    },
    
    getFileTypeFromMime(mime) {
      if (mime.startsWith('text/')) return 'text';
      if (mime.startsWith('image/')) return 'image';
      if (mime.startsWith('audio/')) return 'audio';
      if (mime.startsWith('video/')) return 'video';
      return null;
    },
    
    getFileTypeName(value) {
      const type = this.fileTypes.find(t => t.value === value);
      return type ? type.name : '';
    },
    
    getFileIcon(type) {
      const map = {
        'text': 'fas fa-file-alt',
        'image': 'fas fa-file-image',
        'audio': 'fas fa-file-audio',
        'video': 'fas fa-file-video'
      };
      return map[type] || 'fas fa-file';
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    removeFile(index) {
      // 释放预览URL
      if (this.uploadedFiles[index].previewUrl) {
        URL.revokeObjectURL(this.uploadedFiles[index].previewUrl);
      }
      this.uploadedFiles.splice(index, 1);
    },
    
    clearAll() {
      // 释放所有预览URL
      this.uploadedFiles.forEach(file => {
        if (file.previewUrl) {
          URL.revokeObjectURL(file.previewUrl);
        }
      });
      this.uploadedFiles = [];
      this.textContent = '';
      this.hasResult = false;
      this.currentResult = null;
    },
    
    // ==================== 检测相关 ====================
    startDetection() {
      if (!this.canStartDetection) return;
      
      if (this.detectTimer) {
        clearInterval(this.detectTimer);
      }
      
      this.isDetecting = true;
      this.hasResult = false;
      this.detectStep = 0;
      
      this.detectTimer = setInterval(() => {
        if (this.detectStep < 4) {
          this.detectStep++;
        } else {
          clearInterval(this.detectTimer);
          this.isDetecting = false;
          this.hasResult = true;
          this.mockDetectionResult();
        }
      }, 800);
    },
    
    mockDetectionResult() {
      const isText = this.selectedFileType === 'text';
      const file = this.uploadedFiles[0];
      const isFace = this.selectedFileType === 'image' && this.imageSubtype === 'face';
      
      if (isText) {
        this.currentResult = {
          fileName: '文本输入',
          fileType: 'text',
          fileTypeName: '文本',
          fileSize: `${this.textContent.length} 字`,
          detectTime: new Date().toLocaleString('zh-CN'),
          overallScore: Math.floor(Math.random() * 30) + 70,
          
          metrics: [
            { name: '语义连贯性', value: 92, description: '文本语义连贯，逻辑清晰' },
            { name: '语言模式分析', value: 88, description: '符合自然语言模式' },
            { name: 'AI生成检测', value: 85, description: 'AI生成痕迹检测' },
            { name: '异常模式识别', value: 90, description: '未发现异常语言模式' }
          ],
          
          textFeatures: [
            { name: '文本长度', value: `${this.textContent.length}字`, icon: 'fas fa-text-height' },
            { name: '语言复杂性', value: '中等', icon: 'fas fa-chart-line' },
            { name: '情感倾向', value: '中性', icon: 'fas fa-smile' },
            { name: '关键词提取', value: '8个关键词', icon: 'fas fa-key' }
          ],
          
          detailSections: [
            {
              title: '文本基本信息',
              items: [
                { label: '字符数', value: `${this.textContent.length}字`, status: 'normal' },
                { label: '段落数', value: Math.max(1, Math.floor(this.textContent.length / 100)), status: 'normal' },
                { label: '句子数', value: Math.max(1, Math.floor(this.textContent.length / 20)), status: 'normal' },
                { label: '唯一词汇', value: Math.floor(this.textContent.length / 3), status: 'normal' }
              ]
            },
            {
              title: '真伪检测结果',
              items: [
                { label: 'AI生成检测', value: '未发现', status: 'success' },
                { label: '语义一致性', value: '良好', status: 'success' },
                { label: '异常模式', value: '未发现', status: 'success' },
                { label: '语言自然度', value: '自然', status: 'success' }
              ]
            }
          ],
          
          deepFeatures: [
            { icon: 'fas fa-brain', title: '语义分析', description: '文本语义连贯，符合人类表达习惯', confidence: 92 },
            { icon: 'fas fa-robot', title: 'AI生成检测', description: '未检测到明显的AI生成痕迹', confidence: 88 },
            { icon: 'fas fa-chart-line', title: '语言模式分析', description: '语言模式分布自然，无异常', confidence: 85 },
            { icon: 'fas fa-tag', title: '关键词提取', description: '关键词分布合理，无堆砌现象', confidence: 90 }
          ]
        };
      } else {
        this.currentResult = {
          fileName: file?.name || '身份证照片.jpg',
          fileType: this.selectedFileType,
          fileTypeName: this.fileTypes.find(t => t.value === this.selectedFileType)?.name || '图片',
          fileSize: this.formatFileSize(file?.size || 2400000),
          detectTime: new Date().toLocaleString('zh-CN'),
          overallScore: isFace ? 97 : (this.selectedFileType === 'image' ? 45 : 82),
          
          metrics: [
            { name: '完整性分析', value: isFace ? 98 : 92, description: '文件结构完整，无损坏痕迹' },
            { name: '元数据分析', value: isFace ? 95 : 88, description: '元数据一致性分析' },
            { name: '内容一致性', value: isFace ? 92 : 76, description: '内容逻辑自洽性' },
            { name: '伪造痕迹检测', value: isFace ? 12 : 54, description: '异常痕迹检测' }
          ],
          
          imageFeatures: isFace ? [
            { name: '人脸特征点', value: '68个特征点匹配', icon: 'fas fa-smile' },
            { name: '光照一致性', value: '良好', icon: 'fas fa-sun' },
            { name: '边缘检测', value: '自然过渡', icon: 'fas fa-border-all' },
            { name: '噪声分析', value: '符合自然图像分布', icon: 'fas fa-wave-square' }
          ] : [
            { name: '文字清晰度', value: '良好', icon: 'fas fa-font' },
            { name: '截图完整性', value: '完整', icon: 'fas fa-crop-alt' },
            { name: '时间戳一致性', value: '一致', icon: 'fas fa-clock' },
            { name: '界面元素', value: '符合官方样式', icon: 'fas fa-mobile-alt' }
          ],
          
          detailSections: [
            {
              title: '文件基本信息',
              items: [
                { label: '文件格式', value: file?.name.split('.').pop()?.toUpperCase() || 'JPG', status: 'normal' },
                { label: '文件大小', value: this.formatFileSize(file?.size || 2400000), status: 'normal' },
                { label: '分辨率/时长', value: isFace ? '3024 x 4032' : '1080 x 2340', status: 'normal' },
                { label: '创建时间', value: '2026-03-01 14:23:45', status: 'normal' }
              ]
            },
            {
              title: '真伪检测结果',
              items: [
                { label: 'AI生成检测', value: '未发现', status: 'success' },
                { label: '篡改痕迹', value: '未发现', status: 'success' },
                { label: '元数据一致性', value: '通过', status: 'success' },
                { label: '内容逻辑', value: '自洽', status: 'success' }
              ]
            }
          ],
          
          deepFeatures: [
            { icon: 'fas fa-brain', title: '深度伪造检测', description: '未检测到明显的AI生成痕迹，人脸特征点分布自然', confidence: 98 },
            { icon: 'fas fa-fingerprint', title: '元数据分析', description: 'EXIF信息完整，拍摄设备与声称一致', confidence: 95 },
            { icon: 'fas fa-wave-square', title: '噪声特征分析', description: '图像噪声分布符合自然照片特征', confidence: 92 },
            { icon: 'fas fa-link', title: '一致性校验', description: '人脸与背景光照方向一致，阴影合理', confidence: 96 }
          ]
        };
      }
      
      this.addToRecords();
    },
    
    addToRecords() {
      const newRecord = {
        id: this.records.length + 1,
        name: this.currentResult.fileName,
        type: this.getFileTypeName(this.currentResult.fileType),
        subtype: this.imageSubtype !== 'face' && this.currentResult.fileType === 'image' ? this.imageSubtype : '',
        time: this.currentResult.detectTime,
        score: this.currentResult.overallScore,
        resultClass: this.getScoreClass(this.currentResult.overallScore) === 'score-high' ? 'trust' : 
                    (this.getScoreClass(this.currentResult.overallScore) === 'score-medium' ? 'review' : 'suspicious'),
        resultText: this.getScoreClass(this.currentResult.overallScore) === 'score-high' ? '可信' : 
                    (this.getScoreClass(this.currentResult.overallScore) === 'score-medium' ? '待复核' : '疑似伪造')
      };
      this.records.unshift(newRecord);
    },
    
    getScoreClass(score) {
      if (score >= 80) return 'score-high';
      if (score >= 50) return 'score-medium';
      return 'score-low';
    },
    
    getScoreColor(score) {
      if (score < 30) return '#f56c6c';
      if (score < 60) return '#e6a23c';
      return '#67c23a';
    },
    
    getMetricColor(value) {
      if (value >= 80) return '#67c23a';
      if (value >= 50) return '#e6a23c';
      return '#f56c6c';
    },
    
    // ==================== 置信度转程度词 ====================
    getAccuracyLevel(confidence) {
      if (confidence >= 95) return '非常准确';
      if (confidence >= 85) return '很准确';
      if (confidence >= 75) return '较准确';
      if (confidence >= 60) return '基本准确';
      if (confidence >= 40) return '有一定参考价值';
      return '参考价值有限';
    },
    
    getAccuracyLevelClass(confidence) {
      if (confidence >= 85) return 'accuracy-high';
      if (confidence >= 60) return 'accuracy-medium';
      return 'accuracy-low';
    },
    
    // ==================== 导出报告功能 ====================
    async exportReport() {
      if (!this.hasResult || !this.currentResult) return;
      
      try {
        const element = document.createElement('div');
        element.innerHTML = this.generateReportHTML();
        
        const opt = {
          margin: [0.5, 0.5, 0.5, 0.5],
          filename: `检测报告_${this.currentResult.fileName}_${new Date().getTime()}.pdf`,
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { scale: 2, letterRendering: true },
          jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' }
        };
        
        await html2pdf().from(element).set(opt).save();
        
        this.$message?.success('报告导出成功');
      } catch (error) {
        console.error('导出报告失败:', error);
        alert('报告导出失败，请重试');
      }
    },
    
    generateReportHTML() {
      const result = this.currentResult;
      const scoreClass = this.getScoreClass(result.overallScore);
      const scoreText = scoreClass === 'score-high' ? '可信' : (scoreClass === 'score-medium' ? '待复核' : '疑似伪造');
      
      return `
        <div style="font-family: 'Microsoft YaHei', sans-serif; padding: 20px; max-width: 800px; margin: 0 auto;">
          <div style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid #3b7cff; padding-bottom: 20px;">
            <h1 style="color: #3b7cff; font-size: 24px; margin: 0;">多模态伪造检测报告</h1>
            <p style="color: #666; margin-top: 10px;">生成时间：${new Date().toLocaleString('zh-CN')}</p>
          </div>
          
          <div style="background: #f8fafc; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
            <h2 style="font-size: 18px; color: #1e293b; margin-top: 0;">基本信息</h2>
            <table style="width: 100%; border-collapse: collapse;">
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #edf2f7; width: 30%;">文件名称</td>
                <td style="padding: 10px; border-bottom: 1px solid #edf2f7;">${result.fileName}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #edf2f7;">文件类型</td>
                <td style="padding: 10px; border-bottom: 1px solid #edf2f7;">${result.fileTypeName}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #edf2f7;">文件大小</td>
                <td style="padding: 10px; border-bottom: 1px solid #edf2f7;">${result.fileSize}</td>
              </tr>
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #edf2f7;">检测时间</td>
                <td style="padding: 10px; border-bottom: 1px solid #edf2f7;">${result.detectTime}</td>
              </tr>
              <tr>
                <td style="padding: 10px;">可信度评分</td>
                <td style="padding: 10px;">
                  <span style="background: ${scoreClass === 'score-high' ? '#e8f5e8' : (scoreClass === 'score-medium' ? '#fff3e0' : '#ffebee')}; 
                               color: ${scoreClass === 'score-high' ? '#2e7d32' : (scoreClass === 'score-medium' ? '#ef6c00' : '#c62828')}; 
                               padding: 5px 15px; border-radius: 20px; font-weight: bold;">
                    ${result.overallScore}% - ${scoreText}
                  </span>
                </td>
              </tr>
            </table>
          </div>
          
          <div style="background: #f8fafc; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
            <h2 style="font-size: 18px; color: #1e293b; margin-top: 0;">详细指标</h2>
            ${result.metrics.map(metric => `
              <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                  <span style="color: #64748b;">${metric.name}</span>
                  <span style="color: ${this.getMetricColor(metric.value)}; font-weight: bold;">${metric.value}%</span>
                </div>
                <div style="background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
                  <div style="background: ${this.getMetricColor(metric.value)}; width: ${metric.value}%; height: 100%;"></div>
                </div>
                <p style="color: #94a3b8; font-size: 12px; margin: 5px 0 0;">${metric.description}</p>
              </div>
            `).join('')}
          </div>
          
          <div style="background: #f8fafc; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
            <h2 style="font-size: 18px; color: #1e293b; margin-top: 0;">深度分析</h2>
            ${result.deepFeatures.map(feature => `
              <div style="margin-bottom: 15px; border-left: 3px solid #3b7cff; padding-left: 15px;">
                <h3 style="font-size: 16px; color: #1e293b; margin: 0 0 5px;">${feature.title}</h3>
                <p style="color: #475569; margin: 0 0 8px;">${feature.description}</p>
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span style="color: #64748b; font-size: 13px;">准确度: ${this.getAccuracyLevel(feature.confidence)}</span>
                </div>
              </div>
            `).join('')}
          </div>
          
          <div style="background: #f8fafc; border-radius: 10px; padding: 20px;">
            <h2 style="font-size: 18px; color: #1e293b; margin-top: 0;">检测结论</h2>
            <p style="color: #1e293b; line-height: 1.6;">
              ${result.overallScore >= 80 ? '经多模态分析，该文件真实性较高，未发现明显伪造痕迹。' : 
                (result.overallScore >= 50 ? '经分析，该文件部分特征存在可疑之处，建议人工复核。' : 
                 '经分析，该文件存在明显的伪造痕迹，可信度较低。')}
            </p>
            <div style="background: #e6f0ff; border-radius: 8px; padding: 15px; margin-top: 15px;">
              <p style="color: #3b7cff; margin: 0; font-weight: bold;">免责声明</p>
              <p style="color: #475569; font-size: 12px; margin: 10px 0 0;">
                本报告仅供参考，检测结果基于当前算法模型，不能作为唯一判断依据。建议结合其他证据综合判断。
              </p>
            </div>
          </div>
          
          <div style="text-align: center; margin-top: 30px; color: #94a3b8; font-size: 12px;">
            <p>本报告由多模态伪造检测平台生成</p>
            <p>检测平台 © 2026</p>
          </div>
        </div>
      `;
    },
    
    // ==================== 记录相关 ====================
    applyFilters() {
      this.recordFilters = { ...this.tempFilters };
      this.currentPage = 1;
    },
    
    resetFilters() {
      this.tempFilters = {
        timeRange: '近7天',
        fileType: '全部',
        result: '全部',
        imageSubtype: '全部',
        search: ''
      };
      this.recordFilters = { ...this.tempFilters };
      this.currentPage = 1;
    },
    
    viewRecordDetail(record) {
      this.currentNav = 'detect';
      this.hasResult = true;
      this.currentResult = {
        fileName: record.name,
        fileType: record.type === '文本' ? 'text' : 
                  (record.type === '图片' ? 'image' : 
                   (record.type === '音频' ? 'audio' : 'video')),
        fileTypeName: record.type,
        fileSize: record.type === '文本' ? '500字' : '2.3 MB',
        detectTime: record.time,
        overallScore: record.score,
        
        metrics: [
          { name: '完整性分析', value: record.score > 80 ? 98 : (record.score > 50 ? 76 : 45), description: '文件结构分析' },
          { name: '元数据分析', value: record.score > 80 ? 95 : (record.score > 50 ? 68 : 32), description: '元数据一致性分析' },
          { name: '内容一致性', value: record.score > 80 ? 92 : (record.score > 50 ? 72 : 28), description: '内容逻辑自洽性' },
          { name: '伪造痕迹检测', value: record.score > 80 ? 12 : (record.score > 50 ? 45 : 78), description: '异常痕迹检测' }
        ],
        
        imageFeatures: record.type === '图片' ? [
          { name: '特征分析', value: record.score > 80 ? '正常' : '可疑', icon: 'fas fa-smile' },
          { name: '一致性', value: record.score > 80 ? '良好' : '异常', icon: 'fas fa-sun' }
        ] : [],
        
        detailSections: [
          {
            title: '文件基本信息',
            items: [
              { label: '文件名', value: record.name, status: 'normal' },
              { label: '检测时间', value: record.time, status: 'normal' }
            ]
          }
        ],
        
        deepFeatures: [
          { icon: 'fas fa-brain', title: '综合评估', description: record.resultText, confidence: record.score }
        ]
      };
    },
    
    redetectFile(record) {
      alert(`重新检测：${record.name}`);
    },
    
    exportSingleReport(record) {
      this.currentResult = {
        fileName: record.name,
        fileType: record.type === '文本' ? 'text' : 
                  (record.type === '图片' ? 'image' : 
                   (record.type === '音频' ? 'audio' : 'video')),
        fileTypeName: record.type,
        fileSize: '2.3 MB',
        detectTime: record.time,
        overallScore: record.score,
        
        metrics: [
          { name: '完整性分析', value: record.score, description: '文件结构分析' }
        ],
        
        deepFeatures: [
          { icon: 'fas fa-brain', title: '检测结果', description: record.resultText, confidence: record.score }
        ]
      };
      this.exportReport();
    },
    
    exportRecords() {
      alert('批量导出记录功能开发中');
    },
    
    goToPage() {
      if (this.jumpPage >= 1 && this.jumpPage <= this.totalPages) {
        this.currentPage = this.jumpPage;
      } else {
        this.jumpPage = this.currentPage;
      }
    },
    
    // ==================== 反馈相关 ====================
    handleAttachment(e) {
      const files = Array.from(e.target.files);
      if (this.attachments.length + files.length > 5) {
        alert('最多只能上传5张图片');
        return;
      }
      
      files.forEach(file => {
        if (file.size > 5 * 1024 * 1024) {
          alert(`文件 ${file.name} 超过5MB限制`);
          return;
        }
        if (file.type.startsWith('image/')) {
          this.attachments.push(file);
        }
      });
      
      e.target.value = '';
    },
    
    removeAttachment(index) {
      this.attachments.splice(index, 1);
    },
    
    submitFeedback() {
      if (!this.feedback.type || !this.feedback.title || !this.feedback.description) {
        alert('请填写必填项');
        return;
      }
      
      alert('反馈提交成功，感谢您的支持！我们会在24小时内处理您的反馈。');
      this.resetFeedback();
    },
    
    resetFeedback() {
      this.feedback = {
        type: 'suggestion',
        relatedFile: '',
        title: '',
        description: '',
        contact: ''
      };
      this.attachments = [];
    },
    
    // ==================== FAQ相关 ====================
    toggleFaq(index) {
      this.activeFaq = this.activeFaq === index ? null : index;
    }
  }
};
</script>

<style scoped>
/* ==================== 原有样式保持不变 ==================== */

/* 检测中心 - 结果头部样式调整 */
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.result-header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 日期标签样式 - 适配放在结果区域 */
.result-header .date-badge {
  background: #f8fafc;
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 13px;
  color: #64748b;
  border: 1px solid #edf2f7;
  display: flex;
  align-items: center;
  gap: 6px;
}

.result-header .date-badge i {
  color: #94a3b8;
  font-size: 12px;
}

/* 检测记录 - 筛选区域头部样式 */
.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #edf2f7;
}

.filter-title {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.filter-title i {
  color: #3b7cff;
  font-size: 16px;
}

.export-records-btn {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.export-records-btn:hover {
  border-color: #3b7cff;
  color: #3b7cff;
  background: #f0f4fe;
}

/* ==================== 新增样式 ==================== */

/* 右侧主内容区 - 无间距版本 */
.main-content-no-gap {
  padding-top: 0 !important; /* 移除了上边距，与顶部导航栏相接 */
}

/* 标题区域 - 平衡上下空白 */
.section-header-balanced {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0 0 20px 0;
  padding: 0 0 16px 0;
  border-bottom: 1px solid #edf2f7;
}

/* 标题区域样式 - 放大字号和图标 */
.section-title-large {
  font-size: 20px !important; /* 放大标题字号 */
  font-weight: 600;
  color: #0f172a;
  margin: 0 !important;
  padding: 0 !important;
  border-bottom: none !important;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title-large i {
  font-size: 24px !important; /* 放大图标 */
  color: #3b7cff;
}

/* 调整卡片内边距，使上下空白一致 */
.section-card {
  background: white;
  border-radius: 16px;
  padding: 24px 28px 28px 28px; /* 上边距减少，下边距保持不变 */
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
  border: 1px solid #edf2f7;
  height: fit-content;
}

/* 文件预览样式 */
.file-preview {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  margin-right: 12px;
  flex-shrink: 0;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-audio {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-icon-large {
  font-size: 30px;
  color: #94a3b8;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: #f8fafc;
  border-radius: 10px;
  margin-bottom: 8px;
}

.file-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.file-name {
  font-size: 14px;
  color: #1e293b;
  font-weight: 500;
}

.file-size {
  font-size: 12px;
  color: #94a3b8;
}

.remove-file {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.2s;
}

.remove-file:hover {
  background: #fee2e2;
  color: #ef4444;
}

/* 文本输入区域样式 */
.text-input-section {
  margin-bottom: 24px;
}

.text-input-section label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #475569;
}

.text-input-container {
  position: relative;
  width: 100%;
}

.text-input-area {
  width: 100%;
  height: 200px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  color: #1e293b;
  background: #f8fafc;
  resize: vertical;
  box-sizing: border-box;
  font-family: inherit;
  transition: border-color 0.2s;
}

.text-input-area:focus {
  outline: none;
  border-color: #3b7cff;
  box-shadow: 0 0 0 3px rgba(59,124,255,0.1);
}

.text-counter {
  position: absolute;
  right: 12px;
  bottom: 12px;
  font-size: 12px;
  color: #94a3b8;
  background: rgba(255,255,255,0.9);
  padding: 2px 8px;
  border-radius: 12px;
}

/* 文本分析样式 */
.text-analysis {
  margin-top: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 10px;
}

.text-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

/* 确保查询和重置按钮大小一致 */
.search-btn,
.reset-btn {
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  height: 40px;
  min-width: 80px;
  justify-content: center;
  box-sizing: border-box;
}

.search-btn {
  background: #3b7cff;
  color: white;
}

.search-btn:hover {
  background: #2563eb;
}

.reset-btn {
  background: #f1f5f9;
  color: #64748b;
}

.reset-btn:hover {
  background: #e2e8f0;
}

/* ==================== 优化后的功能特点样式 ==================== */

.feature-description-result {
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
  margin: 24px 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.feature-description-result .feature-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  min-width: 0; /* 防止内容溢出 */
}

.feature-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: #3b7cff;
  border-radius: 50%;
  margin-top: 8px;
  flex-shrink: 0;
}

.feature-text {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.feature-text strong {
  font-size: 15px;
  color: #1e293b;
  margin-bottom: 4px;
  line-height: 1.4;
}

.feature-text span {
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}

/* 确保四个版块严格对齐 */
@media (min-width: 768px) {
  .feature-description-result {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .feature-item {
    min-height: 70px;
  }
}

/* 准确度标签样式 - 恢复原来的样子 */
.accuracy-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 30px;
  font-size: 13px;
  font-weight: 600;
  margin-left: 8px;
}

.accuracy-high {
  background: #e8f5e8;
  color: #2e7d32;
}

.accuracy-medium {
  background: #fff3e0;
  color: #ef6c00;
}

.accuracy-low {
  background: #ffebee;
  color: #c62828;
}

.feature-confidence {
  margin-top: 12px;
  font-size: 13px;
  color: #1e293b;
  display: flex;
  align-items: center;
}

/* 常用检测类型样式 - 美化版 */
.type-ranking {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.rank-item {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.rank-num {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.rank-1 {
  background: #fef9c3;
  color: #854d0e;
}

.rank-2 {
  background: #e0f2fe;
  color: #0369a1;
}

.rank-3 {
  background: #ffe4e6;
  color: #9f1239;
}

.rank-4 {
  background: #f1f5f9;
  color: #475569;
}

.rank-type {
  flex: 1;
  font-size: 15px;
  color: #1e293b;
  font-weight: 500;
  min-width: 60px;
}

.rank-count {
  font-weight: 600;
  color: #3b7cff;
  background: #f0f4fe;
  padding: 4px 12px;
  border-radius: 30px;
  font-size: 14px;
  min-width: 70px;
  text-align: center;
}

.rank-bar {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  min-width: 120px;
}

.rank-bar-fill {
  height: 100%;
  background: #3b7cff;
  border-radius: 4px;
  transition: width 0.3s;
}

/* ==================== 优化后的文件信息卡片样式 - 解决排版问题 ==================== */
.file-info-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 14px;
  margin-bottom: 24px;
}

.file-icon i {
  font-size: 44px;
  color: #3b7cff;
}

.file-details {
  flex: 1;
  min-width: 0; /* 防止flex子项溢出 */
}

.file-name {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
  word-break: break-word;
}

.file-meta {
  width: 100%;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: center;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
  color: #64748b;
  font-size: 13px;
}

.meta-item i {
  margin-right: 6px;
  color: #94a3b8;
  font-size: 12px;
  width: 14px;
  text-align: center;
}

.meta-text {
  white-space: nowrap;
}

.file-size-text {
  /* 确保文件大小文本不换行 */
  white-space: nowrap;
}

.file-score {
  text-align: center;
  padding: 8px 20px;
  border-radius: 10px;
  min-width: 100px;
  flex-shrink: 0;
}

.file-score.score-high {
  background: #e8f5e8;
  color: #2e7d32;
}

.file-score.score-medium {
  background: #fff3e0;
  color: #ef6c00;
}

.file-score.score-low {
  background: #ffebee;
  color: #c62828;
}

.score-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
}

.score-label {
  font-size: 12px;
  opacity: 0.8;
}

/* 响应式调整 - 小屏幕时元数据换行 */
@media (max-width: 768px) {
  .file-info-card {
    flex-wrap: wrap;
  }
  
  .meta-row {
    gap: 16px;
  }
  
  .file-score {
    margin-left: auto;
  }
}

/* 全局样式 */
.fraud-platform {
  display: flex;
  height: 100vh;
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #1e293b;
  background-color: #f8fafc;
}

/* 左侧导航栏 */
.sidebar {
  width: 280px;
  background: white;
  box-shadow: 2px 0 10px rgba(0,0,0,0.03);
  display: flex;
  flex-direction: column;
  z-index: 10;
  border-right: 1px solid #edf2f7;
}

.logo-area {
  padding: 28px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #edf2f7;
}

.logo-area i {
  font-size: 32px;
  color: #3b7cff;
}

.logo-area span {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
}

.nav-menu {
  flex: 1;
  padding: 24px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 14px 24px;
  margin: 4px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}

.nav-item i {
  width: 24px;
  font-size: 18px;
  margin-right: 12px;
}

.nav-item span {
  flex: 1;
  font-size: 15px;
  font-weight: 500;
}

.nav-item:hover {
  background-color: #f0f4fe;
  color: #3b7cff;
}

.nav-item.active {
  background-color: #3b7cff;
  color: white;
  box-shadow: 0 4px 12px rgba(59,124,255,0.25);
}


/* 右侧主内容区 */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 36px;
}

.content-page {
  max-width: 1600px;
  margin: 0 auto;
}

/* 检测中心布局 */
.detect-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}

.section-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
  border: 1px solid #edf2f7;
  height: fit-content;
}

.section-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #0f172a;
  padding-bottom: 16px;
  border-bottom: 1px solid #edf2f7;
}

.section-card h3 i {
  color: #3b7cff;
}

/* 文件类型选择 */
.file-type-selector {
  margin-bottom: 24px;
}

.file-type-selector label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #475569;
}

.type-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.type-btn {
  padding: 10px 20px;
  border: 1px solid #e2e8f0;
  border-radius: 40px;
  background: white;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  font-size: 14px;
}

.type-btn i {
  font-size: 14px;
}

.type-btn:hover {
  border-color: #3b7cff;
  color: #3b7cff;
}

.type-btn.active {
  background-color: #3b7cff;
  border-color: #3b7cff;
  color: white;
}

/* 子类选择 */
.subtype-selector {
  margin-bottom: 24px;
}

.subtype-selector label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #475569;
}

.subtype-options {
  display: flex;
  gap: 24px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #1e293b;
  font-size: 14px;
}

.radio-label input[type="radio"] {
  accent-color: #3b7cff;
  width: 16px;
  height: 16px;
}

/* 模型选择 */
.model-selector {
  margin-bottom: 24px;
}

.model-selector label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #475569;
}

.model-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  color: #1e293b;
  background-color: #f8fafc;
}

/* 上传区域 */
.upload-area {
  border: 2px dashed #e2e8f0;
  border-radius: 16px;
  padding: 36px 20px;
  text-align: center;
  background-color: #f8fafc;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  margin-bottom: 24px;
}

.upload-area:hover {
  border-color: #3b7cff;
  background-color: #f0f4fe;
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  cursor: pointer;
}

.upload-content i {
  font-size: 52px;
  color: #3b7cff;
  margin-bottom: 16px;
  opacity: 0.7;
}

.upload-content p {
  font-size: 16px;
  color: #1e293b;
  margin-bottom: 8px;
  font-weight: 500;
}

.upload-hint {
  font-size: 13px;
  color: #94a3b8;
  display: block;
  margin-bottom: 20px;
}

.select-file-btn {
  background: white;
  border: 1px solid #3b7cff;
  color: #3b7cff;
  padding: 10px 28px;
  border-radius: 40px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.select-file-btn:hover {
  background: #3b7cff;
  color: white;
}

/* 文件列表 */
.file-list {
  margin-bottom: 24px;
  max-height: 300px;
  overflow-y: auto;
}

/* 操作按钮 */
.upload-actions {
  display: flex;
  gap: 16px;
}

.start-detect-btn {
  flex: 1;
  background: #3b7cff;
  border: none;
  color: white;
  padding: 14px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.start-detect-btn:hover {
  background: #2563eb;
}

.start-detect-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.clear-btn {
  padding: 14px 28px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.clear-btn:hover {
  border-color: #ef4444;
  color: #ef4444;
}

/* 检测中动画 */
.detecting-animation {
  text-align: center;
  padding: 40px 20px;
}

.detecting-spinner {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #e2e8f0;
  border-top-color: #3b7cff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.detecting-animation h4 {
  font-size: 22px;
  color: #1e293b;
  margin-bottom: 10px;
}

.detecting-animation p {
  color: #64748b;
  margin-bottom: 30px;
}

.detecting-progress {
  max-width: 500px;
  margin: 0 auto;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.progress-steps::before {
  content: '';
  position: absolute;
  top: 14px;
  left: 0;
  right: 0;
  height: 2px;
  background: #e2e8f0;
  z-index: 1;
}

.progress-step {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 0 10px;
}

.progress-step i {
  width: 32px;
  height: 32px;
  background: #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 16px;
  transition: all 0.3s;
}

.progress-step.active i {
  background: #3b7cff;
  color: white;
}

.progress-step span {
  font-size: 13px;
  color: #94a3b8;
}

.progress-step.active span {
  color: #3b7cff;
  font-weight: 500;
}

/* 空状态 */
.empty-result {
  text-align: center;
  padding: 20px 20px 40px;
}

.empty-illustration i {
  font-size: 90px;
  color: #3b7cff;
  opacity: 0.2;
  margin-bottom: 24px;
}

.empty-result h4 {
  font-size: 22px;
  color: #1e293b;
  margin-bottom: 24px;
}

.detect-steps {
  max-width: 400px;
  margin: 0 auto;
  text-align: left;
}

.detect-steps .step {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.step-num {
  width: 32px;
  height: 32px;
  background: #3b7cff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content {
  display: flex;
  flex-direction: column;
}

.step-content strong {
  font-size: 16px;
  color: #1e293b;
  margin-bottom: 4px;
}

.step-content span {
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}

/* 分析标签页 */
.analysis-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 1px solid #edf2f7;
  padding-bottom: 12px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 8px 18px;
  font-size: 14px;
  color: #64748b;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #f0f4fe;
  color: #3b7cff;
}

.tab-btn.active {
  background: #3b7cff;
  color: white;
}

.tab-content {
  min-height: 320px;
}

/* 指标网格 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.metric-item {
  padding: 16px;
  background: #f8fafc;
  border-radius: 10px;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.metric-name {
  font-size: 14px;
  color: #64748b;
}

.metric-value {
  font-size: 16px;
  font-weight: 600;
}

.progress-bar {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  margin-bottom: 8px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s;
}

.metric-desc {
  font-size: 12px;
  color: #94a3b8;
}

/* 图像分析 */
.image-analysis {
  margin-top: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 10px;
}

.analysis-subtitle {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1e293b;
}

.image-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #1e293b;
}

.feature i {
  color: #3b7cff;
  width: 20px;
}

/* 详细分析 */
.detail-analysis {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.analysis-section {
  border: 1px solid #edf2f7;
  border-radius: 10px;
  overflow: hidden;
}

.section-title {
  padding: 12px 16px;
  background: #f8fafc;
  font-weight: 600;
  font-size: 14px;
  color: #1e293b;
  border-bottom: 1px solid #edf2f7;
}

.section-items {
  padding: 12px 16px;
}

.section-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f1f5f9;
}

.section-item:last-child {
  border-bottom: none;
}

.item-label {
  color: #64748b;
  font-size: 14px;
}

.item-value {
  font-weight: 500;
  font-size: 14px;
}

.item-value.success {
  color: #67c23a;
}

.item-value.warning {
  color: #e6a23c;
}

.item-value.danger {
  color: #f56c6c;
}

/* 特征分析 */
.features-analysis {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.feature-block {
  padding: 16px;
  background: #f8fafc;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.feature-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #1e293b;
}

.feature-title i {
  color: #3b7cff;
}

.feature-desc {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 12px;
  line-height: 1.5;
  flex: 1;
}

.feature-confidence {
  margin-top: 12px;
  font-size: 13px;
  color: #1e293b;
  display: flex;
  align-items: center;
}

/* 筛选栏 - 原有样式 (已调整头部) */
.filter-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  border: 1px solid #edf2f7;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
  align-items: end;
}

.filter-item {
  display: flex;
  flex-direction: column;
}

.filter-item label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.filter-item select,
.filter-item input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
  font-size: 14px;
  color: #1e293b;
  box-sizing: border-box;
}

.search-item {
  grid-column: span 2;
}

.search-box {
  position: relative;
  width: 100%;
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 14px;
}

.search-box input {
  padding-left: 35px;
  width: 100%;
  box-sizing: border-box;
}

.buttons-item {
  grid-column: span 1;
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  justify-content: flex-end;
}

/* 记录表格 */
.records-table-container {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #edf2f7;
  margin-bottom: 24px;
  overflow-x: auto;
}

.records-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 900px;
}

.records-table th {
  text-align: left;
  padding: 16px 12px;
  font-weight: 600;
  font-size: 13px;
  color: #64748b;
  border-bottom: 2px solid #edf2f7;
  background: #f8fafc;
}

.records-table td {
  padding: 16px 12px;
  border-bottom: 1px solid #edf2f7;
  font-size: 14px;
  vertical-align: middle;
}

.file-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-cell i {
  font-size: 18px;
  color: #3b7cff;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 500;
}

.badge.type {
  background: #e6f0ff;
  color: #3b7cff;
}

.badge.subtype {
  background: #f1f5f9;
  color: #475569;
}

.badge.result.trust {
  background: #e8f5e8;
  color: #2e7d32;
}

.badge.result.suspicious {
  background: #ffebee;
  color: #c62828;
}

.badge.result.review {
  background: #fff3e0;
  color: #ef6c00;
}

.score-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 130px;
}

.score-text {
  font-weight: 500;
  min-width: 40px;
  font-size: 14px;
}

.score-bar {
  flex: 1;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.2s;
}

.action-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 16px;
  margin-right: 12px;
  cursor: pointer;
  padding: 6px;
}

.action-btn:hover {
  color: #3b7cff;
}

.empty-table {
  text-align: center;
  padding: 40px !important;
  color: #94a3b8;
  font-size: 14px;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  background: white;
  padding: 16px 24px;
  border-radius: 12px;
  border: 1px solid #edf2f7;
}

.pagination-info {
  color: #64748b;
  font-size: 14px;
}

.pagination-controls {
  display: flex;
  gap: 6px;
  align-items: center;
}

.pagination-controls button {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  color: #1e293b;
  min-width: 40px;
  font-size: 14px;
  transition: all 0.2s;
}

.pagination-controls button:hover:not(:disabled) {
  border-color: #3b7cff;
  color: #3b7cff;
}

.pagination-controls button.active {
  background: #3b7cff;
  border-color: #3b7cff;
  color: white;
}

.pagination-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f1f5f9;
}

.pagination-go {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
}

.pagination-go input {
  width: 60px;
  padding: 6px 8px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  text-align: center;
  box-sizing: border-box;
}

/* 数据统计 */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 28px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid #edf2f7;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}

.stat-icon.blue {
  background: #e6f0ff;
  color: #3b7cff;
}

.stat-icon.green {
  background: #e8f5e8;
  color: #67c23a;
}

.stat-icon.orange {
  background: #fff3e0;
  color: #e6a23c;
}

.stat-icon.purple {
  background: #f3e5f5;
  color: #9c27b0;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.2;
  margin-bottom: 6px;
}

.stat-trend {
  font-size: 13px;
  color: #94a3b8;
}

/* 图表区域 */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #edf2f7;
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chart-header h4 i {
  color: #3b7cff;
}

.time-range-select {
  padding: 6px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
  font-size: 13px;
  color: #1e293b;
}

.chart-wrapper {
  position: relative;
  width: 100%;
  min-height: 250px;
}

.chart-container {
  width: 100%;
  height: 250px;
}

.chart-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.9);
  color: #ef4444;
  gap: 8px;
  z-index: 10;
}

.chart-error i {
  font-size: 24px;
}

/* 检测习惯 */
.stats-habits {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.habit-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #edf2f7;
}

.habit-card h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #0f172a;
}

.habit-card h4 i {
  color: #3b7cff;
}

.time-distribution {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.time-slot {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
}

.time-slot span:first-child {
  width: 110px;
  color: #475569;
}

.time-slot span:last-child {
  width: 45px;
  color: #1e293b;
  font-weight: 500;
}

.slot-bar {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.slot-fill {
  height: 100%;
  background: #3b7cff;
  border-radius: 4px;
}

/* 意见反馈 */
.feedback-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 24px;
}

.form-card, .history-card, .tip-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  border: 1px solid #edf2f7;
}

.form-card h3, .history-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #0f172a;
  padding-bottom: 16px;
  border-bottom: 1px solid #edf2f7;
}

.form-group {
  margin-bottom: 24px;
  position: relative;
}

.form-group.with-counter {
  margin-bottom: 32px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #1e293b;
}

.required {
  color: #ef4444;
}

.feedback-type-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.type-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.type-option:hover {
  border-color: #3b7cff;
  background: #f0f4fe;
}

.type-option.active {
  border-color: #3b7cff;
  background: #f0f4fe;
}

.type-option input[type="radio"] {
  accent-color: #3b7cff;
  width: 16px;
  height: 16px;
}

.type-option i {
  color: #3b7cff;
  font-size: 16px;
}

.full-width-input,
.full-width-textarea,
.form-group input[type="text"],
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.2s;
  background: #fafbfc;
  box-sizing: border-box;
}

.full-width-textarea,
.form-group textarea {
  resize: vertical;
  min-height: 120px;
  font-family: inherit;
}

.full-width-input:focus,
.full-width-textarea:focus,
.form-group input[type="text"]:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #3b7cff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(59,124,255,0.1);
}

.char-counter {
  position: absolute;
  right: 0;
  bottom: -24px;
  font-size: 12px;
  color: #94a3b8;
}

.attachment-upload {
  margin-bottom: 12px;
}

.upload-btn {
  background: #f8fafc;
  border: 1px dashed #3b7cff;
  color: #3b7cff;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: all 0.2s;
}

.upload-btn:hover {
  background: #e6f0ff;
}

.upload-hint {
  display: block;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 6px;
}

.attachment-list {
  margin-top: 12px;
}

.attachment-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 6px;
}

.attachment-item i {
  color: #3b7cff;
  margin-right: 8px;
}

.attachment-item .name {
  flex: 1;
  font-size: 13px;
  color: #1e293b;
}

.attachment-item .size {
  font-size: 12px;
  color: #94a3b8;
  margin-right: 8px;
}

.attachment-item .remove {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
}

.attachment-item .remove:hover {
  color: #ef4444;
}

.form-actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
}

.submit-btn {
  flex: 1;
  background: #3b7cff;
  border: none;
  color: white;
  padding: 14px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.submit-btn:hover {
  background: #2563eb;
}

.reset-btn {
  padding: 14px 28px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.reset-btn:hover {
  border-color: #ef4444;
  color: #ef4444;
}

/* 历史记录 */
.history-list {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 16px;
}

.history-item {
  padding: 16px;
  border-bottom: 1px solid #edf2f7;
}

.history-item:last-child {
  border-bottom: none;
}

.history-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.feedback-type {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.feedback-type.type-suggestion {
  background: #e6f0ff;
  color: #3b7cff;
}

.feedback-type.type-bug {
  background: #ffebee;
  color: #c62828;
}

.feedback-type.type-question {
  background: #e8f5e8;
  color: #2e7d32;
}

.feedback-status {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.feedback-status.status-replied {
  background: #e8f5e8;
  color: #2e7d32;
}

.feedback-status.status-processing {
  background: #fff3e0;
  color: #ef6c00;
}

.feedback-title {
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 4px;
  font-size: 14px;
}

.feedback-time {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 10px;
}

.feedback-reply {
  display: flex;
  gap: 10px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 13px;
}

.feedback-reply i {
  color: #3b7cff;
  font-size: 12px;
  margin-top: 2px;
}

.reply-label {
  font-weight: 500;
  color: #1e293b;
}

.view-more {
  text-align: center;
  padding: 12px;
  border-top: 1px solid #edf2f7;
}

.view-more a {
  color: #3b7cff;
  text-decoration: none;
  font-size: 14px;
}

.tip-card {
  margin-top: 24px;
}

.tip-card h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #0f172a;
}

.tip-card ul {
  list-style: none;
  padding: 0;
}

.tip-card li {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #475569;
}

.tip-card li i {
  color: #67c23a;
  font-size: 14px;
}

/* 使用指南 */
.guide-content {
  max-width: 1200px;
  margin: 0 auto;
}

.guide-section {
  background: white;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 28px;
  border: 1px solid #edf2f7;
}

.guide-section h3 {
  font-size: 22px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 28px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.guide-section h3 i {
  color: #3b7cff;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.step-card {
  text-align: center;
  padding: 28px 20px;
  background: #f8fafc;
  border-radius: 14px;
  position: relative;
}

.step-number {
  position: absolute;
  top: -12px;
  left: -12px;
  width: 36px;
  height: 36px;
  background: #3b7cff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
  box-shadow: 0 4px 8px rgba(59,124,255,0.3);
}

.step-card i {
  font-size: 44px;
  color: #3b7cff;
  margin-bottom: 16px;
}

.step-card h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #0f172a;
}

.step-card p {
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
}

.file-types-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.file-type-card {
  padding: 24px;
  background: #f8fafc;
  border-radius: 14px;
}

.file-type-card i {
  font-size: 36px;
  color: #3b7cff;
  margin-bottom: 16px;
}

.file-type-card h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #0f172a;
}

.file-type-card ul {
  list-style: none;
  padding: 0;
}

.file-type-card li {
  font-size: 13px;
  color: #475569;
  margin-bottom: 8px;
  padding-left: 16px;
  position: relative;
}

.file-type-card li:before {
  content: "•";
  position: absolute;
  left: 4px;
  color: #3b7cff;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  padding: 28px;
  background: #f8fafc;
  border-radius: 14px;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-card i {
  font-size: 36px;
  color: #3b7cff;
  margin-bottom: 16px;
}

.feature-card h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #0f172a;
}

.feature-card p {
  color: #475569;
  font-size: 14px;
  line-height: 1.6;
}

.faq-list {
  border-top: 1px solid #edf2f7;
}

.faq-item {
  border-bottom: 1px solid #edf2f7;
}

.faq-question {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 0;
  cursor: pointer;
  font-weight: 500;
  color: #1e293b;
  transition: color 0.2s;
}

.faq-question:hover {
  color: #3b7cff;
}

.faq-question i {
  color: #3b7cff;
  transition: transform 0.2s;
  font-size: 14px;
}

.faq-question i.rotated {
  transform: rotate(90deg);
}

.faq-answer {
  padding: 0 0 20px 28px;
  color: #475569;
  line-height: 1.7;
  font-size: 14px;
}

/* 响应式调整 */
@media (max-width: 1400px) {
  .filter-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .search-item {
    grid-column: span 2;
  }
  
  .buttons-item {
    grid-column: span 1;
  }
}

@media (max-width: 1200px) {
  .detect-layout {
    grid-template-columns: 1fr;
  }
  
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .feedback-layout {
    grid-template-columns: 1fr;
  }
  
  .steps-grid,
  .file-types-grid,
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 16px;
  }
  
  .feature-description-result {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .steps-grid,
  .file-types-grid,
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .filter-grid {
    grid-template-columns: 1fr;
  }
  
  .search-item,
  .buttons-item {
    grid-column: span 1;
  }
  
  .pagination {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .pagination-controls {
    order: -1;
  }
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>