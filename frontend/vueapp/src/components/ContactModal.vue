<template>
  <Teleport to="body">
    <transition name="modal">
      <div v-if="visible && contact" class="modal-overlay" @click.self="close">
        <div class="modal-card">
          <!-- Header -->
          <div class="modal-header">
            <div class="header-left">
              <div class="avatar-large">{{ initialLetters }}</div>
              <div>
                <h2>
                  <template v-if="!isEditing">{{ contact.first_name }} {{ contact.last_name }}</template>
                  <template v-else>
                    <div class="edit-name-row">
                      <input v-model="editForm.first_name" class="edit-input" placeholder="First Name" />
                      <input v-model="editForm.last_name" class="edit-input" placeholder="Last Name" />
                    </div>
                  </template>
                </h2>
                <div class="company-sub">
                  <span v-if="!isEditing">{{ contact.company || 'No Company' }}</span>
                  <input v-else v-model="editForm.company" class="edit-input w-full" placeholder="Company Name" />
                </div>
              </div>
            </div>

            <div class="header-actions">
              <button v-if="!isEditing" @click="startEditing" class="action-btn edit" title="Edit Contact">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                Edit
              </button>
              <button class="action-btn close" @click="close" title="Close">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </button>
            </div>
          </div>

          <!-- Content Body -->
          <div class="modal-body">
            <!-- Loading overlay when communicating with backend -->
            <div v-if="isLoading" class="loading-overlay">
              <div class="loader"></div>
            </div>

            <!-- Address Section -->
            <div class="detail-section">
              <h3>Address</h3>
              <div class="detail-card">
                <p v-if="!isEditing" class="multiline-text">{{ contact.address || '—' }}</p>
                <textarea v-else v-model="editForm.address" class="edit-textarea" placeholder="Full Address..." rows="3"></textarea>
              </div>
            </div>

            <!-- Notes Section -->
            <div class="detail-section">
              <h3>Notes</h3>
              <div class="detail-card">
                <p v-if="!isEditing" class="multiline-text">{{ contact.notes || 'No notes added.' }}</p>
                <textarea v-else v-model="editForm.notes" class="edit-textarea" placeholder="Add some notes about this contact..." rows="4"></textarea>
              </div>
            </div>

            <!-- Communications Section (Read-Only for now) -->
            <div class="detail-section" v-if="!isEditing && contact.communications && contact.communications.length > 0">
              <h3>Connected Channels</h3>
              <div class="comm-grid">
                <div v-for="comm in contact.communications" :key="comm.id" class="comm-item">
                  <span class="comm-type">{{ formatLabel(comm.label) || comm.comm_type.toUpperCase() }}</span>
                  <span class="comm-value">{{ comm.value }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="errorMsg" class="error-banner">{{ errorMsg }}</div>

          <!-- Footer Actions (Only in Edit Mode) -->
          <div class="modal-footer" v-if="isEditing">
            <button class="delete-btn" @click="confirmDelete" :disabled="isLoading">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
              Delete
            </button>
            <div class="right-actions">
              <button class="cancel-btn" @click="cancelEdit" :disabled="isLoading">Cancel</button>
              <button class="primary-btn" @click="saveContact" :disabled="isLoading">Save Changes</button>
            </div>
          </div>

        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import api from '../services/api';

const props = defineProps({
  visible: { type: Boolean, default: false },
  contact: { type: Object, default: null }
});

const emit = defineEmits(['close', 'updated', 'deleted']);

const isEditing = ref(false);
const isLoading = ref(false);
const errorMsg = ref('');
const editForm = ref({
  first_name: '',
  last_name: '',
  company: '',
  address: '',
  notes: ''
});

// Watch for prop changes to reset state
watch(() => props.visible, (newVal) => {
  if (newVal) {
    isEditing.value = false;
    isLoading.value = false;
    errorMsg.value = '';
    initForm();
  }
});

const initialLetters = computed(() => {
  if (!props.contact) return '';
  return `${(props.contact.first_name || '').charAt(0)}${(props.contact.last_name || '').charAt(0)}`.toUpperCase();
});

const formatLabel = (label) => {
  if (!label) return '';
  return label.split(',')[0].toUpperCase();
};

const initForm = () => {
  if (!props.contact) return;
  editForm.value = {
    first_name: props.contact.first_name || '',
    last_name: props.contact.last_name || '',
    company: props.contact.company || '',
    address: props.contact.address || '',
    notes: props.contact.notes || ''
  };
};

const startEditing = () => {
  initForm();
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
  errorMsg.value = '';
};

const close = () => {
  if (isLoading.value) return;
  emit('close');
};

const saveContact = async () => {
  errorMsg.value = '';
  isLoading.value = true;

  try {
    const payload = {
      ...editForm.value,
      communications: props.contact.communications // Keep existing comms
    };

    await api.put(`/contacts/${props.contact.id}`, payload);
    
    emit('updated'); // Notify parent to refresh list
    isEditing.value = false;
  } catch (error) {
    if (error.response?.data?.detail) {
      errorMsg.value = Array.isArray(error.response.data.detail) ? error.response.data.detail[0].msg : error.response.data.detail;
    } else {
      errorMsg.value = 'Network error. Failed to save contact.';
    }
  } finally {
    isLoading.value = false;
  }
};

const confirmDelete = async () => {
  if (!confirm(`Are you sure you want to delete ${props.contact.first_name}? This cannot be undone.`)) return;

  errorMsg.value = '';
  isLoading.value = true;

  try {
    await api.delete(`/contacts/${props.contact.id}`);
    emit('deleted'); // Notify parent to refresh and close
  } catch (error) {
    errorMsg.value = 'Failed to delete contact.';
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Modal Structure */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-active .modal-card, .modal-leave-active .modal-card {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
.modal-enter-from .modal-card {
  transform: translateY(20px) scale(0.97);
  opacity: 0;
}

.modal-card {
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 20px;
  width: 100%;
  max-width: 550px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  position: relative;
}

/* Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 32px 32px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  gap: 20px;
  align-items: center;
  flex: 1;
}

.avatar-large {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary), #818cf8);
  color: white;
  font-size: 24px;
  font-weight: 700;
  box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
}

.modal-header h2 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
  color: var(--text-primary);
  display: flex;
  gap: 8px;
  align-items: center;
}

.company-sub {
  color: var(--text-secondary);
  font-size: 15px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-secondary);
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.close {
  padding: 8px;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.action-btn.edit:hover {
  background: rgba(79, 70, 229, 0.2);
  color: #818cf8;
  border-color: rgba(79, 70, 229, 0.4);
}

/* Edit Mode Inputs */
.edit-name-row {
  display: flex;
  gap: 8px;
  width: 100%;
}

.edit-input {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 8px 12px;
  color: white;
  font-family: inherit;
  font-size: inherit;
  width: 100%;
  transition: border-color 0.2s;
}

.edit-input:focus {
  outline: none;
  border-color: var(--primary);
  background: rgba(0,0,0,0.3);
}

.edit-input.w-full {
  width: 100%;
}

.edit-textarea {
  width: 100%;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 12px;
  color: white;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.5;
  resize: vertical;
  transition: border-color 0.2s;
}

.edit-textarea:focus {
  outline: none;
  border-color: var(--primary);
  background: rgba(0,0,0,0.3);
}

/* Body */
.modal-body {
  padding: 32px;
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(4px);
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255,255,255,0.1);
  border-radius: 50%;
  border-top-color: var(--primary);
  animation: spin 0.8s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.detail-section h3 {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  font-weight: 600;
}

.detail-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
}

.multiline-text {
  color: var(--text-primary);
  line-height: 1.6;
  font-size: 14px;
  white-space: pre-wrap;
}

.comm-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.comm-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.comm-type {
  font-size: 10px;
  color: var(--text-secondary);
  font-weight: 600;
  letter-spacing: 0.5px;
}

.comm-value {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
}

/* Errors */
.error-banner {
  margin: 0 32px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  padding: 12px;
  border-radius: 10px;
  font-size: 13px;
  text-align: center;
}

/* Footer */
.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.1);
}

.right-actions {
  display: flex;
  gap: 12px;
}

.delete-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  color: #ef4444;
  border: 1px solid transparent;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}

.delete-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cancel-btn {
  background: transparent;
  border: 1px solid var(--surface-border);
  color: var(--text-secondary);
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.primary-btn {
  background: linear-gradient(to right, var(--primary), #6366f1);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
  transition: all 0.2s;
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
}

.primary-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
