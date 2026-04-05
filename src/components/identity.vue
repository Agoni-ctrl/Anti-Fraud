<template>
  <div class="identity-customization">
    <div class="identity-container">
      <div class="identity-left">
        <div class="identity-image">
          <img src="/identityimage.png" alt="身份定制" class="side-image">
        </div>
        <div class="identity-welcome">
          <p class="welcome-text">请完善您的个人信息<br>我们将为您推荐个性化专属反诈服务</p>
        </div>
      </div>
      
      <div class="identity-right">
        <div class="identity-header">
          <h1>身份定制</h1>
        </div>

        <form @submit.prevent="submitIdentity" class="identity-form">
          <div class="form-section">
          <h2>
            <font-awesome-icon icon="shield" class="section-icon" />
            基本信息
          </h2>
            <div class="form-group">
              <label>昵称</label>
              <input 
                v-model="identityData.nickname" 
                type="text" 
                placeholder="请输入您的昵称" 
                required
              >
            </div>

            <div class="form-group">
              <label>性别</label>
              <div class="radio-group">
                <label class="radio-option">
                  <input 
                    v-model="identityData.gender" 
                    type="radio" 
                    value="male"
                  >
                  <span>男</span>
                </label>
                <label class="radio-option">
                  <input 
                    v-model="identityData.gender" 
                    type="radio" 
                    value="female"
                  >
                  <span>女</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>年龄段</label>
              <select v-model="identityData.ageGroup" required>
                <option value="">请选择年龄段</option>
                <option value="0-18">0-18岁</option>
                <option value="18-25">18-25岁</option>
                <option value="26-35">26-35岁</option>
                <option value="36-45">36-45岁</option>
                <option value="46-55">46-55岁</option>
                <option value="56+">56岁以上</option>
              </select>
            </div>

            <div class="form-group">
              <label>身份</label>
              <select v-model="identityData.occupation" required>
                <option value="">请选择身份</option>
                <option value="student">学生</option>
                <option value="elderly">老年人</option>
                <option value="job_seeker">待业</option>
                <option value="finance">金融行业</option>
                <option value="other">其他</option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="submit-btn">
              完成定制
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const identityData = ref({
  nickname: '',
  gender: '',
  ageGroup: '',
  occupation: ''
})

const submitIdentity = () => {
  // 验证表单
  if (!identityData.value.nickname || !identityData.value.gender || 
      !identityData.value.ageGroup || !identityData.value.occupation) {
    alert('请填写所有必填信息')
    return
  }

  // 保存身份信息到本地存储
  localStorage.setItem('userIdentity', JSON.stringify(identityData.value))
  localStorage.setItem('userNickname', identityData.value.nickname)
  
  // 跳转到首页
  router.push('/')
}

onMounted(() => {
  // 检查是否已登录
  if (!localStorage.getItem('isLoggedIn')) {
    router.push('/')
  }
})
</script>

<style scoped>
.identity-customization {
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 30px;
  padding-bottom: 40px;
  padding-left: 40px;
  padding-right: 40px;
}

.identity-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  display: flex;
  overflow: hidden;
  max-width: 900px;
  width: 100%;
  max-height: 85vh;
  animation: slideUp 0.5s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.identity-left {
  flex: 1;
  background: linear-gradient(135deg, #0064b2 0%, #0099ff 100%);
  padding: 40px 35px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  position: relative;
  overflow: hidden;
}

.identity-left::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.identity-image {
  position: relative;
  z-index: 1;
  margin-bottom: 25px;
  overflow: hidden;
  border-radius: 12px;
  display: inline-block;
  width: 280px;
  height: 210px;
}

.side-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.3s ease;
  display: block;
}

.side-image:hover {
  transform: scale(1.02);
}

.identity-welcome {
  position: relative;
  z-index: 1;
  text-align: center;
}

.welcome-text {
  font-size: 1rem;
  font-weight: normal;
  line-height: 1.7;
  margin-bottom: 0;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  max-width: 280px;
}

.identity-right {
  flex: 1.2;
  padding: 35px 45px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.identity-header {
  text-align: center;
  margin-bottom: 25px;
}

.identity-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #0064b2;
  margin-bottom: 0;
}

.form-section {
  margin-bottom: 20px;
}

.form-section h2 {
  font-size: 1.15rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-icon {
  font-size: 1.2rem;
  color: #0064b2;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.form-group input[type="text"],
.form-group select {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: #f7fafc;
}

.form-group input[type="text"]:focus,
.form-group select:focus {
  outline: none;
  border-color: #0064b2;
  background: white;
  box-shadow: 0 0 0 4px rgba(0, 100, 178, 0.1);
}

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  color: #333;
  padding: 8px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.radio-option:hover {
  border-color: #0064b2;
  background: rgba(0, 100, 178, 0.05);
}

.radio-option input[type="radio"] {
  width: 20px;
  height: 20px;
  accent-color: #0064b2;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 25px;
}

.submit-btn {
  background: linear-gradient(135deg, #0064b2 0%, #0099ff 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 14px 40px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 100, 178, 0.3);
}

.submit-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 100, 178, 0.4);
  background: linear-gradient(135deg, #0055a0 0%, #0088ee 100%);
}

@media (max-width: 968px) {
  .identity-container {
    flex-direction: column;
    max-width: 600px;
  }
  
  .identity-left {
    padding: 40px 30px;
    min-height: 300px;
  }
  
  .side-image {
    width: 220px;
  }
  
  .welcome-text {
    font-size: 0.9rem;
    max-width: 240px;
  }
  
  .identity-right {
    padding: 40px 30px;
  }
}

@media (max-width: 480px) {
  .identity-customization {
    padding: 20px;
  }
  
  .identity-right {
    padding: 30px 20px;
  }
  
  .identity-header h1 {
    font-size: 1.8rem;
  }
  
  .radio-group {
    flex-direction: column;
    gap: 15px;
  }
  
  .side-image {
    width: 220px;
  }
}
</style>
