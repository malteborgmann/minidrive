<template>
  <div class="dashboard-page">
    <div class="bg-shape shape-1"></div>
    
    <header class="topbar">
      <div class="logo">
         <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="12" y1="8" x2="12" y2="16"></line>
          <line x1="8" y1="12" x2="16" y2="12"></line>
        </svg>
        Minidrive
      </div>
      <button @click="logout" class="logout-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
        Logout
      </button>
    </header>

    <main class="dashboard-content">
      <div class="header-section">
        <div>
          <h1>Your Contacts</h1>
          <p>Manage and view all your synchronized data.</p>
        </div>
        <button class="primary-btn" @click="alert('VCF Upload not yet implemented in frontend')">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" class="btn-icon" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
          Import VCF
        </button>
      </div>

      <div v-if="isLoading" class="loader-wrapper">
         <div class="loader"></div>
         <p>Loading database...</p>
      </div>
      
      <div v-else-if="errorMsg" class="error-banner">
        {{ errorMsg }}
      </div>
      
      <ContactTable v-else :contacts="contacts" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import ContactTable from '../components/ContactTable.vue';

const router = useRouter();
const contacts = ref([]);
const isLoading = ref(true);
const errorMsg = ref('');

const fetchContacts = async () => {
  try {
    const response = await api.get('/contacts/');
    contacts.value = response.data;
    console.log(contacts.value);
  } catch (error) {
    if (error.response && error.response.status === 401) {
      errorMsg.value = 'Your session has expired. Please log in again.';
      logout();
    } else {
      errorMsg.value = 'Failed to load contacts from the database.';
    }
  } finally {
    isLoading.value = false;
  }
};

const logout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchContacts();
});
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  position: relative;
  display: flex;
  flex-direction: column;
}

.bg-shape {
  position: fixed;
  filter: blur(100px);
  border-radius: 50%;
  z-index: 0;
}

.shape-1 {
  width: 600px;
  height: 600px;
  background: rgba(79, 70, 229, 0.15);
  top: -200px;
  right: -200px;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--surface-border);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 700;
  color: white;
}

.logo svg {
  color: var(--primary);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--surface-border);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.dashboard-content {
  position: relative;
  z-index: 10;
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 20px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
}

.header-section h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
}

.header-section p {
  color: var(--text-secondary);
  font-size: 15px;
}

.primary-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(to right, var(--primary), #6366f1);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
  transition: all 0.2s;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
}

.loader-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
  color: var(--text-secondary);
  gap: 16px;
}

.loader {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255,255,255,0.1);
  border-radius: 50%;
  border-top-color: var(--primary);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-banner {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  padding: 16px;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 24px;
}
</style>
