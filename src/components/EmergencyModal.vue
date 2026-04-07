<template>
  <div class="emergency-modal-overlay" @click.self="$emit('close')">
    <div class="emergency-modal">
      <div class="modal-header">
        <div class="header-icon">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
        <h2>紧急求助中心</h2>
        <button class="close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="modal-body">
        <!-- 发现遭受诈骗时应该做什么 -->
        <div class="section">
          <h3 class="section-title">
            <i class="fas fa-lightbulb section-icon"></i>
            发现遭受诈骗时应该做什么
          </h3>
          <ul class="action-list">
            <li><span class="num">1</span>立即停止与诈骗分子的任何联系，不要继续转账或提供个人信息</li>
            <li><span class="num">2</span>拨打 <strong>110</strong> 报警或 <strong>96110</strong> 反诈专线求助</li>
            <li><span class="num">3</span>保存好相关证据：聊天记录、转账凭证、通话录音等</li>
            <li><span class="num">4</span>尽快前往最近的派出所报案</li>
            <li><span class="num">5</span>通知家人或监护人，寻求帮助和支持</li>
          </ul>
        </div>

        <!-- 报案所需携带材料 -->
        <div class="section">
          <h3 class="section-title">
            <i class="fas fa-folder-open section-icon"></i>
            报案所需携带材料
          </h3>
          <div class="materials-grid">
            <div class="material-item">
              <i class="fas fa-id-card material-icon"></i>
              <span>本人身份证原件</span>
            </div>
            <div class="material-item">
              <i class="fas fa-mobile-alt material-icon"></i>
              <span>涉案手机/电脑</span>
            </div>
            <div class="material-item">
              <i class="fas fa-credit-card material-icon"></i>
              <span>银行卡及交易记录</span>
            </div>
            <div class="material-item">
              <i class="fas fa-comment-dots material-icon"></i>
              <span>聊天记录截图</span>
            </div>
            <div class="material-item">
              <i class="fas fa-receipt material-icon"></i>
              <span>转账凭证/收据</span>
            </div>
            <div class="material-item">
              <i class="fas fa-phone-alt material-icon"></i>
              <span>通话录音（如有）</span>
            </div>
          </div>
        </div>

        <!-- 登记监护人信息 -->
        <div class="section guardian-section">
          <h3 class="section-title">
            <i class="fas fa-users section-icon"></i>
            登记监护人信息
            <span class="subtitle">（遭受诈骗时自动发送预警）</span>
          </h3>

          <form @submit.prevent="saveGuardian" class="guardian-form">
            <div class="form-row">
              <div class="form-group">
                <label>监护人姓名</label>
                <div class="input-with-toggle">
                  <input
                    :type="showName ? 'text' : 'password'"
                    v-model="guardianForm.name"
                    placeholder="请输入监护人姓名"
                    required
                  />
                  <button type="button" class="toggle-visibility" @click="toggleNameVisibility">
                    <i :class="showName ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>手机号码</label>
                <div class="input-with-toggle">
                  <input
                    :type="showPhone ? 'text' : 'password'"
                    v-model="guardianForm.phone"
                    placeholder="请输入手机号码"
                    pattern="[0-9]{11}"
                    required
                  />
                  <button type="button" class="toggle-visibility" @click="togglePhoneVisibility">
                    <i :class="showPhone ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                  </button>
                </div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group full-width">
                <label>与本人关系</label>
                <select v-model="guardianForm.relation" required>
                  <option value="">请选择关系</option>
                  <option value="父亲">父亲</option>
                  <option value="母亲">母亲</option>
                  <option value="配偶">配偶</option>
                  <option value="子女">子女</option>
                  <option value="兄弟姐妹">兄弟姐妹</option>
                  <option value="其他">其他</option>
                </select>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="clearForm">
                <i class="fas fa-eraser"></i> 清空
              </button>
              <button type="submit" class="btn-primary">
                <i class="fas fa-save"></i> 保存监护人信息
              </button>
            </div>
          </form>

          <div v-if="savedGuardian" class="saved-info">
            <h4><i class="fas fa-check-circle"></i> 已登记的监护人</h4>
            <div class="guardian-card">
              <div class="guardian-detail">
                <span class="label">姓名：</span>
                <span class="value">{{ savedGuardian.name }}</span>
              </div>
              <div class="guardian-detail">
                <span class="label">手机：</span>
                <span class="value">{{ savedGuardian.phone }}</span>
              </div>
              <div class="guardian-detail">
                <span class="label">关系：</span>
                <span class="value">{{ savedGuardian.relation }}</span>
              </div>
              <button class="btn-remove" @click="removeGuardian">
                <i class="fas fa-trash-alt"></i> 移除
              </button>
            </div>
          </div>
        </div>

        <!-- 紧急联系电话 -->
        <div class="emergency-contacts">
          <h3 class="section-title">
            <i class="fas fa-phone-alt section-icon"></i>
            紧急求助电话
          </h3>
          <div class="contacts-list">
            <div class="contact-card">
              <div class="contact-icon-wrapper">
                <i class="fas fa-shield-alt"></i>
              </div>
              <div class="contact-info">
                <div class="contact-name">全国反诈专线</div>
                <div class="contact-number">96110</div>
                <div class="contact-description">反诈预警劝阻、咨询举报专用热线，遇到可疑情况第一时间拨打</div>
              </div>
              <a href="tel:96110" class="contact-call">
                <i class="fas fa-phone-alt"></i> 拨打
              </a>
            </div>

            <div class="contact-card">
              <div class="contact-icon-wrapper">
                <i class="fas fa-gavel"></i>
              </div>
              <div class="contact-info">
                <div class="contact-name">报警服务台</div>
                <div class="contact-number">110</div>
                <div class="contact-description">已经遭受诈骗或遇到紧急危险时立即拨打，警方将快速出警处理</div>
              </div>
              <a href="tel:110" class="contact-call">
                <i class="fas fa-phone-alt"></i> 拨打
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['close'])

const guardianForm = ref({
  name: '',
  phone: '',
  relation: ''
})

const savedGuardian = ref(null)
const showName = ref(false)
const showPhone = ref(false)

onMounted(() => {
  const saved = localStorage.getItem('guardianInfo')
  if (saved) {
    savedGuardian.value = JSON.parse(saved)
  }
})

const toggleNameVisibility = () => {
  showName.value = !showName.value
}

const togglePhoneVisibility = () => {
  showPhone.value = !showPhone.value
}

const saveGuardian = () => {
  const guardian = {
    ...guardianForm.value,
    savedAt: new Date().toISOString()
  }
  localStorage.setItem('guardianInfo', JSON.stringify(guardian))
  savedGuardian.value = guardian
  guardianForm.value = { name: '', phone: '', relation: '' }
  alert('监护人信息已保存！当您遭受诈骗时，系统将自动向监护人发送预警通知。')
}

const clearForm = () => {
  guardianForm.value = { name: '', phone: '', relation: '' }
  showName.value = false
  showPhone.value = false
}

const removeGuardian = () => {
  if (confirm('确定要移除监护人信息吗？')) {
    localStorage.removeItem('guardianInfo')
    savedGuardian.value = null
  }
}
</script>

<style scoped>
/* 引入字体图标 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.emergency-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(189, 69, 60, 0.15);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.emergency-modal {
  background: #FFFFFF;
  border-radius: 24px;
  width: 90%;
  max-width: 800px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(189, 69, 60, 0.25);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  background: linear-gradient(135deg, #BD453C, #A03A32);
  padding: 24px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 24px 24px 0 0;
}

.header-icon {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.header-icon i {
  font-size: 24px;
  color: #DFD1B7;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.6rem;
  color: #FFFFFF;
  font-weight: 600;
  flex: 1;
}

.close-btn {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: white;
  font-size: 1.4rem;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.modal-body {
  padding: 28px;
}

.section {
  margin-bottom: 28px;
  padding-bottom: 24px;
  border-bottom: 1px solid #F5EFE5;
}

.section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.2rem;
  color: #BD453C;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.section-icon {
  font-size: 1.3rem;
  color: #DFD1B7;
}

.section-title .subtitle {
  font-size: 0.8rem;
  color: #DFD1B7;
  font-weight: normal;
  background: #F5EFE5;
  padding: 2px 8px;
  border-radius: 20px;
}

.action-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.action-list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #F5EFE5;
  color: #5A6B7A;
  line-height: 1.5;
}

.action-list li:last-child {
  border-bottom: none;
}

.action-list .num {
  background: linear-gradient(135deg, #BD453C, #A03A32);
  color: white;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: bold;
  flex-shrink: 0;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.material-item {
  background: #FDFBF8;
  padding: 16px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  text-align: center;
  font-size: 0.9rem;
  color: #5A6B7A;
  transition: all 0.3s ease;
  border: 1px solid #F5EFE5;
}

.material-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(189, 69, 60, 0.1);
  border-color: #DFD1B7;
}

.material-icon {
  font-size: 2rem;
  color: #BD453C;
}

.guardian-section {
  background: #FDFBF8;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 28px;
  border-left: 4px solid #BD453C;
}

.guardian-form {
  margin-top: 20px;
}

.form-row {
  display: flex;
  gap: 18px;
  margin-bottom: 18px;
}

.form-group {
  flex: 1;
}

.form-group.full-width {
  flex: 1;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  color: #BD453C;
  margin-bottom: 8px;
  font-weight: 500;
}

.input-with-toggle {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-toggle input,
.form-group select {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #F5EFE5;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.2s;
  background: white;
  color: #2C3E4E;
}

.input-with-toggle input:focus,
.form-group select:focus {
  outline: none;
  border-color: #DFD1B7;
  box-shadow: 0 0 0 3px rgba(223, 209, 183, 0.2);
}

.toggle-visibility {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #DFD1B7;
  cursor: pointer;
  padding: 0;
  font-size: 1.1rem;
  transition: color 0.2s;
}

.toggle-visibility:hover {
  color: #BD453C;
}

.form-actions {
  display: flex;
  gap: 14px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-primary,
.btn-secondary {
  padding: 10px 22px;
  border-radius: 10px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.btn-primary {
  background: linear-gradient(135deg, #BD453C, #A03A32);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(189, 69, 60, 0.3);
}

.btn-secondary {
  background: #F5EFE5;
  color: #BD453C;
}

.btn-secondary:hover {
  background: #DFD1B7;
  transform: translateY(-2px);
}

.saved-info {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 2px dashed #F5EFE5;
}

.saved-info h4 {
  font-size: 1rem;
  color: #BD453C;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.guardian-card {
  background: white;
  padding: 18px;
  border-radius: 12px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 8px rgba(189, 69, 60, 0.08);
  border: 1px solid #F5EFE5;
}

.guardian-detail {
  display: flex;
  gap: 8px;
}

.guardian-detail .label {
  color: #DFD1B7;
  font-size: 0.9rem;
  font-weight: 500;
}

.guardian-detail .value {
  color: #2C3E4E;
  font-weight: 500;
}

.btn-remove {
  margin-left: auto;
  padding: 8px 16px;
  background: #FFFFFF;
  border: 1px solid #BD453C;
  color: #BD453C;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-remove:hover {
  background: #BD453C;
  color: white;
}

.emergency-contacts {
  margin-top: 28px;
}

.contacts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contact-card {
  background: linear-gradient(135deg, #FFFFFF, #FDFBF8);
  border-radius: 14px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 18px;
  transition: all 0.3s ease;
  border: 1px solid #F5EFE5;
  position: relative;
}

.contact-card:hover {
  transform: translateX(4px);
  box-shadow: 0 6px 16px rgba(189, 69, 60, 0.1);
  border-color: #DFD1B7;
}

.contact-icon-wrapper {
  width: 56px;
  height: 56px;
  background: #F5EFE5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.contact-icon-wrapper i {
  font-size: 28px;
  color: #BD453C;
}

.contact-info {
  flex: 1;
}

.contact-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #BD453C;
  margin-bottom: 4px;
}

.contact-number {
  font-size: 1.3rem;
  font-weight: bold;
  color: #DFD1B7;
  margin-bottom: 6px;
  font-family: monospace;
}

.contact-description {
  font-size: 0.85rem;
  color: #7A8A9A;
  line-height: 1.4;
}

.contact-call {
  background: #BD453C;
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 40px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.contact-call:hover {
  background: #A03A32;
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .emergency-modal {
    width: 95%;
    max-height: 90vh;
  }

  .modal-header {
    padding: 18px 20px;
  }

  .modal-header h2 {
    font-size: 1.3rem;
  }

  .modal-body {
    padding: 20px;
  }

  .materials-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .form-row {
    flex-direction: column;
    gap: 14px;
  }

  .contact-card {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .contact-call {
    width: 100%;
    justify-content: center;
  }

  .guardian-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .btn-remove {
    margin-left: 0;
    margin-top: 8px;
  }
}
</style>