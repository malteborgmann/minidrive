<template>
  <div class="dashboard">
    <h1>Dashboard Placeholder</h1>
    <button @click="logout" class="logout-btn">Logout</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};
</script>

<style scoped>
.dashboard {
  padding: 40px;
  text-align: center;
}

.logout-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
