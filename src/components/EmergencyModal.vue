<template>
  <div class="emergency-modal-overlay" @click.self="$emit('close')">
    <div class="emergency-modal">
      <div class="modal-header">
        <h2>紧急求助</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <div class="modal-body">
        <div class="section">
          <h3 class="section-title">
            <span class="icon">🚨</span>
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

        <div class="section">
          <h3 class="section-title">
            <span class="icon">📋</span>
            报案所需携带材料
          </h3>
          <div class="materials-grid">
            <div class="material-item">
              <span class="material-icon">🪪</span>
              <span>本人身份证原件</span>
            </div>
            <div class="material-item">
              <span class="material-icon">📱</span>
              <span>涉案手机/电脑</span>
            </div>
            <div class="material-item">
              <span class="material-icon">💳</span>
              <span>银行卡及交易记录</span>
            </div>
            <div class="material-item">
              <span class="material-icon">📸</span>
              <span>聊天记录截图</span>
            </div>
            <div class="material-item">
              <span class="material-icon">📝</span>
              <span>转账凭证/收据</span>
            </div>
            <div class="material-item">
              <span class="material-icon">📞</span>
              <span>通话录音（如有）</span>
            </div>
          </div>
        </div>

        <div class="section guardian-section">
          <h3 class="section-title">
            <span class="icon">👨‍👩‍👧</span>
            登记监护人信息
            <span class="subtitle">（遭受诈骗时自动发送预警）</span>
          </h3>

          <form @submit.prevent="saveGuardian" class="guardian-form">
            <div class="form-row">
              <div class="form-group">
                <label>监护人姓名</label>
                <input
                  type="text"
                  v-model="guardianForm.name"
                  placeholder="请输入监护人姓名"
                  required
                />
              </div>
              <div class="form-group">
                <label>手机号码</label>
                <input
                  type="tel"
                  v-model="guardianForm.phone"
                  placeholder="请输入手机号码"
                  pattern="[0-9]{11}"
                  required
                />
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
              <button type="button" class="btn-secondary" @click="clearForm">清空</button>
              <button type="submit" class="btn-primary">保存监护人信息</button>
            </div>
          </form>

          <div v-if="savedGuardian" class="saved-info">
            <h4>已登记的监护人</h4>
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
              <button class="btn-remove" @click="removeGuardian">移除</button>
            </div>
          </div>
        </div>

        <div class="emergency-contacts">
          <h3 class="section-title">
            <span class="icon">📞</span>
            紧急联系电话
          </h3>
          <div class="contacts-grid">
            <a href="tel:110" class="contact-card police">
              <span class="contact-icon">🚔</span>
              <span class="contact-name">报警电话</span>
              <span class="contact-number">110</span>
            </a>
            <a href="tel:96110" class="contact-card anti-fraud">
              <span class="contact-icon">🛡️</span>
              <span class="contact-name">反诈专线</span>
              <span class="contact-number">96110</span>
            </a>
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

onMounted(() => {
  const saved = localStorage.getItem('guardianInfo')
  if (saved) {
    savedGuardian.value = JSON.parse(saved)
  }
})

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
}

const removeGuardian = () => {
  if (confirm('确定要移除监护人信息吗？')) {
    localStorage.removeItem('guardianInfo')
    savedGuardian.value = null
  }
}
</script>

<style scoped>
.emergency-modal-overlay {
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
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.emergency-modal {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 700px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 16px 16px 0 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.8rem;
  cursor: pointer;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.modal-body {
  padding: 24px;
}

.section {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title .icon {
  font-size: 1.3rem;
}

.section-title .subtitle {
  font-size: 0.85rem;
  color: #888;
  font-weight: normal;
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
  border-bottom: 1px dashed #eee;
  color: #555;
  line-height: 1.5;
}

.action-list li:last-child {
  border-bottom: none;
}

.action-list .num {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  width: 24px;
  height: 24px;
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
  gap: 12px;
}

.material-item {
  background: #f8f9fa;
  padding: 14px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-align: center;
  font-size: 0.9rem;
  color: #555;
  transition: transform 0.2s, box-shadow 0.2s;
}

.material-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.material-icon {
  font-size: 1.8rem;
}

.guardian-section {
  background: #fff5f5;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.guardian-form {
  margin-top: 16px;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
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
  color: #666;
  margin-bottom: 6px;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #e74c3c;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

.btn-secondary {
  background: #f0f0f0;
  color: #666;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.saved-info {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px dashed #e0e0e0;
}

.saved-info h4 {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 12px;
}

.guardian-card {
  background: white;
  padding: 16px;
  border-radius: 10px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.guardian-detail {
  display: flex;
  gap: 6px;
}

.guardian-detail .label {
  color: #888;
  font-size: 0.9rem;
}

.guardian-detail .value {
  color: #333;
  font-weight: 500;
}

.btn-remove {
  margin-left: auto;
  padding: 6px 14px;
  background: #fff;
  border: 1px solid #e74c3c;
  color: #e74c3c;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: #e74c3c;
  color: white;
}

.emergency-contacts {
  margin-top: 24px;
}

.contacts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.contact-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-radius: 12px;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
}

.contact-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.contact-card.police {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
}

.contact-card.anti-fraud {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.contact-icon {
  font-size: 2.5rem;
  margin-bottom: 8px;
}

.contact-name {
  font-size: 0.95rem;
  opacity: 0.9;
  margin-bottom: 4px;
}

.contact-number {
  font-size: 1.8rem;
  font-weight: bold;
}

@media (max-width: 768px) {
  .emergency-modal {
    width: 95%;
    max-height: 90vh;
  }

  .materials-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-row {
    flex-direction: column;
    gap: 12px;
  }

  .contacts-grid {
    grid-template-columns: 1fr;
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
