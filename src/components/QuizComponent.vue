<template>
  <div class="quiz-container">
    <div v-if="!quizFinished" class="quiz-content">
      <div class="quiz-header">
        <h3 class="quiz-title">防骗小测试</h3>
        <div class="quiz-progress">
          <span class="question-num">问题 {{ currentQuestionIndex + 1 }} / {{ localQuizzes.length }}</span>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: ((currentQuestionIndex + 1) / localQuizzes.length * 100) + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="quiz-question">
        <p class="question-text">{{ currentQuiz.question }}</p>
      </div>

      <div class="quiz-options">
        <div
          v-for="(option, index) in currentQuiz.options"
          :key="index"
          class="quiz-option"
          :class="{
            'selected': currentQuiz.selected === index && !currentQuiz.answered,
            'correct': currentQuiz.answered && index === currentQuiz.correct,
            'wrong': currentQuiz.answered && currentQuiz.selected === index && index !== currentQuiz.correct
          }"
          @click="selectOption(index)"
        >
          <span class="option-label">{{ ['A', 'B', 'C', 'D'][index] }}</span>
          <span class="option-text">{{ option }}</span>
        </div>
      </div>

      <div v-if="currentQuiz.answered" class="quiz-explanation">
        <div class="explanation-header">
          <span v-if="currentQuiz.selected === currentQuiz.correct" class="result-icon correct">✓</span>
          <span v-else class="result-icon wrong">✗</span>
          <span class="result-text">
            {{ currentQuiz.selected === currentQuiz.correct ? '回答正确！' : '回答错误' }}
          </span>
        </div>
        <p class="explanation-content">{{ currentQuiz.explanation }}</p>
      </div>

      <div class="quiz-footer">
        <button
          class="quiz-btn secondary"
          @click="prevQuestion"
          :disabled="currentQuestionIndex === 0"
        >
          上一题
        </button>
        <button
          v-if="!currentQuiz.answered"
          class="quiz-btn primary"
          @click="confirmAnswer"
          :disabled="currentQuiz.selected === null"
        >
          确认答案
        </button>
        <button
          v-else
          class="quiz-btn primary"
          @click="nextQuestion"
        >
          {{ currentQuestionIndex === localQuizzes.length - 1 ? '查看成绩' : '下一题' }}
        </button>
      </div>
    </div>

    <div v-else class="quiz-result">
      <div class="result-header">
        <div class="score-circle">
          <span class="score-number">{{ quizScore }}</span>
          <span class="score-label">分</span>
        </div>
        <h3 class="result-title">测试完成！</h3>
        <p class="result-subtitle">
          共 {{ localQuizzes.length }} 题，答对 {{ correctCount }} 题
        </p>
      </div>

      <div class="result-message">
        <span v-if="quizScore === 100" class="message excellent">🎉 太棒了！满分！你是防骗小达人！</span>
        <span v-else-if="quizScore >= 80" class="message good">👍 不错！继续保持警惕！</span>
        <span v-else-if="quizScore >= 60" class="message average">💪 还需努力，多学习防骗知识哦！</span>
        <span v-else class="message poor">⚠️ 需要加强防骗意识，建议重新学习！</span>
      </div>

      <div class="wrong-answers" v-if="wrongAnswers.length > 0">
        <h4 class="wrong-title">错题解析</h4>
        <div class="wrong-item" v-for="(answer, index) in wrongAnswers" :key="index">
          <div class="wrong-question">
            <span class="wrong-num">{{ index + 1 }}.</span>
            <span class="wrong-text">{{ answer.question }}</span>
          </div>
          <div class="wrong-detail">
            <div class="wrong-choice">
              <span class="choice-label">您的答案：</span>
              <span class="choice-text wrong">{{ answer.selected }}</span>
            </div>
            <div class="correct-choice">
              <span class="choice-label">正确答案：</span>
              <span class="choice-text correct">{{ answer.correct }}</span>
            </div>
            <div class="explanation-box">
              <span class="explanation-label">解析：</span>
              <span class="explanation-text">{{ answer.explanation }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="result-actions">
        <button class="quiz-btn primary" @click="restartQuiz">再测一次</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  quizzes: {
    type: Array,
    required: true
  }
})

const currentQuestionIndex = ref(0)
const quizFinished = ref(false)
const localQuizzes = ref([])

watch(() => props.quizzes, (newQuizzes) => {
  localQuizzes.value = newQuizzes.map(q => ({
    ...q,
    selected: null,
    answered: false
  }))
}, { immediate: true, deep: true })

const currentQuiz = computed(() => localQuizzes.value[currentQuestionIndex.value] || { question: '', options: [], correct: 0, selected: null, answered: false, explanation: '' })

const correctCount = computed(() => {
  return localQuizzes.value.filter(q => q.selected === q.correct).length
})

const quizScore = computed(() => {
  if (localQuizzes.value.length === 0) return 0
  return Math.round((correctCount.value / localQuizzes.value.length) * 100)
})

const wrongAnswers = computed(() => {
  return localQuizzes.value
    .filter(q => q.selected !== q.correct)
    .map(q => ({
      question: q.question,
      selected: q.options[q.selected] || '未作答',
      correct: q.options[q.correct],
      explanation: q.explanation
    }))
})

const selectOption = (index) => {
  if (!currentQuiz.value.answered) {
    currentQuiz.value.selected = index
  }
}

const confirmAnswer = () => {
  if (currentQuiz.value.selected !== null) {
    currentQuiz.value.answered = true
  }
}

const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < localQuizzes.value.length - 1) {
    currentQuestionIndex.value++
  } else {
    quizFinished.value = true
  }
}

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  quizFinished.value = false
  localQuizzes.value.forEach(q => {
    q.selected = null
    q.answered = false
  })
}
</script>

<style scoped>
.quiz-container {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.quiz-header {
  margin-bottom: 25px;
}

.quiz-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 15px;
  font-weight: 600;
}

.quiz-progress {
  display: flex;
  align-items: center;
  gap: 15px;
}

.question-num {
  font-size: 0.95rem;
  color: #666;
  font-weight: 500;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #84CBF3, #4AEBE1);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.quiz-question {
  margin-bottom: 25px;
}

.question-text {
  font-size: 1.1rem;
  color: #333;
  line-height: 1.6;
  font-weight: 500;
}

.quiz-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 25px;
}

.quiz-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
}

.quiz-option:hover:not(.selected):not(.correct):not(.wrong) {
  border-color: #84CBF3;
  background: #f0f9ff;
}

.quiz-option.selected {
  border-color: #84CBF3;
  background: #e3f2fd;
}

.quiz-option.correct {
  border-color: #4CAF50;
  background: #e8f5e9;
}

.quiz-option.wrong {
  border-color: #f44336;
  background: #ffebee;
}

.option-label {
  width: 28px;
  height: 28px;
  background: #f0f0f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #666;
  flex-shrink: 0;
}

.quiz-option.correct .option-label {
  background: #4CAF50;
  color: white;
}

.quiz-option.wrong .option-label {
  background: #f44336;
  color: white;
}

.quiz-option.selected .option-label {
  background: #84CBF3;
  color: white;
}

.option-text {
  flex: 1;
  color: #333;
  font-size: 0.95rem;
}

.quiz-explanation {
  background: #fff8e1;
  border-left: 4px solid #ff9800;
  padding: 18px;
  border-radius: 8px;
  margin-bottom: 25px;
}

.explanation-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.result-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
}

.result-icon.correct {
  background: #4CAF50;
  color: white;
}

.result-icon.wrong {
  background: #f44336;
  color: white;
}

.result-text {
  font-weight: 600;
  color: #333;
}

.explanation-content {
  color: #666;
  line-height: 1.6;
  font-size: 0.95rem;
}

.quiz-footer {
  display: flex;
  justify-content: space-between;
  gap: 15px;
}

.quiz-btn {
  padding: 12px 28px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.quiz-btn.primary {
  background: linear-gradient(135deg, #84CBF3, #4AEBE1);
  color: white;
}

.quiz-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(132, 203, 243, 0.4);
}

.quiz-btn.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quiz-btn.secondary {
  background: #f0f0f0;
  color: #666;
}

.quiz-btn.secondary:hover:not(:disabled) {
  background: #e0e0e0;
}

.quiz-btn.secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quiz-result {
  text-align: center;
}

.result-header {
  margin-bottom: 30px;
}

.score-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: linear-gradient(135deg, #84CBF3, #4AEBE1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 4px 20px rgba(132, 203, 243, 0.3);
}

.score-number {
  font-size: 3rem;
  font-weight: 700;
  color: white;
  line-height: 1;
}

.score-label {
  font-size: 1.2rem;
  color: white;
  font-weight: 500;
}

.result-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 10px;
  font-weight: 600;
}

.result-subtitle {
  color: #666;
  font-size: 1rem;
}

.result-message {
  margin-bottom: 30px;
}

.message {
  font-size: 1.1rem;
  font-weight: 500;
  padding: 15px 25px;
  border-radius: 8px;
  display: inline-block;
}

.message.excellent {
  background: #e8f5e9;
  color: #2e7d32;
}

.message.good {
  background: #e3f2fd;
  color: #1565c0;
}

.message.average {
  background: #fff8e1;
  color: #f57c00;
}

.message.poor {
  background: #ffebee;
  color: #c62828;
}

.wrong-answers {
  text-align: left;
  margin-bottom: 30px;
}

.wrong-title {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 20px;
  font-weight: 600;
}

.wrong-item {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
}

.wrong-question {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.wrong-num {
  font-weight: 600;
  color: #666;
  flex-shrink: 0;
}

.wrong-text {
  color: #333;
  font-weight: 500;
}

.wrong-detail {
  margin-left: 30px;
}

.wrong-choice,
.correct-choice {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.choice-label {
  color: #666;
  font-weight: 500;
}

.choice-text {
  font-weight: 500;
}

.choice-text.wrong {
  color: #c62828;
}

.choice-text.correct {
  color: #2e7d32;
}

.explanation-box {
  background: white;
  padding: 12px;
  border-radius: 6px;
  margin-top: 10px;
}

.explanation-label {
  color: #666;
  font-weight: 500;
}

.explanation-text {
  color: #333;
  line-height: 1.5;
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

@media (max-width: 768px) {
  .quiz-options {
    grid-template-columns: 1fr;
  }

  .quiz-footer {
    flex-direction: column;
  }

  .quiz-btn {
    width: 100%;
  }

  .result-actions {
    flex-direction: column;
  }

  .result-actions .quiz-btn {
    width: 100%;
  }
}
</style>