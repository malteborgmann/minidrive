<template>
  <div class="login-page">
    <!-- Animated background elements -->
    <div class="bg-shape shape-1"></div>
    <div class="bg-shape shape-2"></div>
    
    <div class="login-wrapper">
      <div class="glass-card">
        <div class="card-header">
          <div class="logo-circle">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="12" y1="8" x2="12" y2="16"></line>
              <line x1="8" y1="12" x2="16" y2="12"></line>
            </svg>
          </div>
          <h1>Minidrive</h1>
          <p>Login to access your contacts</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <label for="username">Username</label>
            <div class="input-field">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              <input type="text" id="username" v-model="form.username" placeholder="john_doe" required autocomplete="username" />
            </div>
          </div>

          <div class="input-group">
            <label for="password">Password</label>
            <div class="input-field">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
              <input type="password" id="password" v-model="form.password" placeholder="••••••••" required autocomplete="current-password" />
            </div>
          </div>

          <div class="error-box" v-if="errorMsg">
            {{ errorMsg }}
          </div>

          <button type="submit" class="submit-btn" :class="{ 'loading': isLoading }" :disabled="isLoading">
            <span v-if="!isLoading">Sign In</span>
            <span v-else class="loader"></span>
          </button>
        </form>
        
        <div class="card-footer">
          Don't have an account? <a href="#" @click.prevent="alert('Registration view placeholder')">Register here</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const router = useRouter();

const form = ref({
  username: '',
  password: ''
});

const errorMsg = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  errorMsg.value = '';
  isLoading.value = true;
  
  try {
    // FastAPI expects application/x-www-form-urlencoded for OAuth2 /token login
    const formData = new URLSearchParams();
    formData.append('username', form.value.username);
    formData.append('password', form.value.password);

    const response = await api.post('/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    // Save token and navigate
    localStorage.setItem('token', response.data.access_token);
    router.push('/contacts');
  } catch (error) {
    if (error.response && error.response.status === 401) {
      errorMsg.value = 'Invalid username or password.';
    } else {
      errorMsg.value = 'An error occurred while trying to log in.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  width: 100%;
  position: relative;
}

/* Background Animations */
.bg-shape {
  position: absolute;
  filter: blur(80px);
  border-radius: 50%;
  z-index: 0;
  animation: float 20s ease-in-out infinite alternate;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: rgba(79, 70, 229, 0.4);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 500px;
  height: 500px;
  background: rgba(217, 70, 239, 0.3);
  bottom: -150px;
  right: -100px;
  animation-delay: -5s;
}

@keyframes float {
  0% { transform: translateY(0) scale(1); }
  100% { transform: translateY(-50px) scale(1.1); }
}

/* Glassmorphism Card */
.login-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  padding: 0 20px;
  perspective: 1000px;
}

.glass-card {
  background: var(--surface);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--surface-border);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  transform-style: preserve-3d;
  animation: cardEntrance 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}

@keyframes cardEntrance {
  0% { opacity: 0; transform: translateY(30px) rotateX(10deg); }
  100% { opacity: 1; transform: translateY(0) rotateX(0deg); }
}

.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-circle {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, var(--primary), #d946ef);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.5);
}

.logo-circle svg {
  color: white;
}

.card-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  background: linear-gradient(to right, #fff, #cbd5e1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.card-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input-field {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: #64748b;
  transition: color 0.3s ease;
}

.input-field input {
  width: 100%;
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  padding: 14px 14px 14px 44px;
  color: white;
  font-size: 15px;
  font-family: inherit;
  transition: all 0.3s ease;
  outline: none;
}

.input-field input:focus {
  border-color: var(--primary);
  background: rgba(15, 23, 42, 0.6);
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.15);
}

.input-field input:focus + .input-icon,
.input-field input:valid + .input-icon {
  color: var(--primary);
}

.error-box {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  padding: 12px;
  border-radius: 8px;
  font-size: 13px;
  text-align: center;
  animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
}

.submit-btn {
  background: linear-gradient(to right, var(--primary), #6366f1);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 16px;
  font-size: 16px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 20px -10px rgba(79, 70, 229, 0.5);
  margin-top: 8px;
  position: relative;
  overflow: hidden;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 25px -10px rgba(79, 70, 229, 0.6);
}

.submit-btn:active {
  transform: translateY(1px);
}

.submit-btn.loading {
  background: var(--primary-hover);
  cursor: wait;
}

.loader {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  display: inline-block;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.card-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--text-secondary);
}

.card-footer a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.card-footer a:hover {
  color: #818cf8;
  text-decoration: underline;
}
</style>
