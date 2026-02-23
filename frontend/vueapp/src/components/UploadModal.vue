<template>
  <Teleport to="body">
    <transition name="modal">
      <div v-if="visible" class="modal-overlay" @click.self="close" @dragover.prevent @drop.prevent>
        <div class="modal-card">
          <!-- Header -->
          <div class="modal-header">
            <h2>Import VCF File</h2>
            <button class="close-btn" @click="close">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>

          <!-- Drop Zone -->
          <div
            class="drop-zone"
            :class="{ 'drag-over': isDragging, 'has-file': selectedFile }"
            @dragenter.prevent="onDragEnter"
            @dragover.prevent="onDragOver"
            @dragleave.prevent="onDragLeave"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <input
              ref="fileInput"
              type="file"
              accept=".vcf,text/vcard"
              hidden
              @change="handleFileSelect"
            />

            <div v-if="!selectedFile" class="drop-content">
              <div class="drop-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
              </div>
              <p class="drop-title">Drag & Drop your VCF file here</p>
              <p class="drop-sub">or click to browse · Only <strong>.vcf</strong> files accepted</p>
            </div>

            <div v-else class="file-preview">
              <div class="file-icon">📇</div>
              <div class="file-info">
                <span class="file-name">{{ selectedFile.name }}</span>
                <span class="file-size">{{ formatSize(selectedFile.size) }}</span>
              </div>
              <button class="remove-file" @click.stop="removeFile">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </button>
            </div>
          </div>

          <!-- Error -->
          <div v-if="errorMsg" class="upload-error">{{ errorMsg }}</div>

          <!-- Success -->
          <div v-if="successMsg" class="upload-success">{{ successMsg }}</div>

          <!-- Footer -->
          <div class="modal-footer">
            <button class="cancel-btn" @click="close">Cancel</button>
            <button
              class="upload-btn"
              :class="{ loading: isUploading }"
              :disabled="!selectedFile || isUploading"
              @click="uploadFile"
            >
              <span v-if="!isUploading">Upload</span>
              <span v-else class="loader"></span>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue';
import api from '../services/api';

const props = defineProps({
  visible: { type: Boolean, default: false }
});

const emit = defineEmits(['close', 'uploaded']);

const fileInput = ref(null);
const selectedFile = ref(null);
const isDragging = ref(false);
const dragCount = ref(0);
const isUploading = ref(false);
const errorMsg = ref('');
const successMsg = ref('');

const triggerFileInput = () => {
  if (!selectedFile.value) {
    fileInput.value.click();
  }
};

const handleFileSelect = (e) => {
  const file = e.target.files[0];
  if (file) validateAndSet(file);
};

const onDragEnter = () => {
  dragCount.value++;
  isDragging.value = true;
};

const onDragOver = () => {
  isDragging.value = true;
};

const onDragLeave = () => {
  dragCount.value--;
  if (dragCount.value <= 0) {
    dragCount.value = 0;
    isDragging.value = false;
  }
};

const handleDrop = (e) => {
  dragCount.value = 0;
  isDragging.value = false;
  const file = e.dataTransfer.files && e.dataTransfer.files[0];
  if (file) validateAndSet(file);
};

const validateAndSet = (file) => {
  errorMsg.value = '';
  successMsg.value = '';

  if (!file.name.toLowerCase().endsWith('.vcf')) {
    errorMsg.value = 'Only .vcf files are supported.';
    return;
  }

  selectedFile.value = file;
};

const removeFile = () => {
  selectedFile.value = null;
  errorMsg.value = '';
  successMsg.value = '';
  if (fileInput.value) fileInput.value.value = '';
};

const uploadFile = async () => {
  if (!selectedFile.value) return;

  isUploading.value = true;
  errorMsg.value = '';
  successMsg.value = '';

  try {
    const formData = new FormData();
    formData.append('file', selectedFile.value);

    const response = await api.post('/files/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    successMsg.value = `Successfully imported ${response.data.contacts_imported} contact(s)!`;
    
    // Emit event so the parent refreshes the table
    setTimeout(() => {
      emit('uploaded');
      close();
    }, 1500);
  } catch (error) {
    if (error.response) {
      errorMsg.value = error.response.data.detail || 'Upload failed.';
    } else {
      errorMsg.value = 'Network error. Is the backend running?';
    }
  } finally {
    isUploading.value = false;
  }
};

const close = () => {
  removeFile();
  emit('close');
};

const formatSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B';
  return (bytes / 1024).toFixed(1) + ' KB';
};
</script>

<style scoped>
/* Overlay */
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

/* Transition */
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

/* Card */
.modal-card {
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 700;
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 8px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Drop Zone */
.drop-zone {
  border: 2px dashed rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(0, 0, 0, 0.15);
}

.drop-zone:hover {
  border-color: rgba(79, 70, 229, 0.4);
  background: rgba(79, 70, 229, 0.05);
}

.drop-zone.drag-over {
  border-color: var(--primary);
  background: rgba(79, 70, 229, 0.1);
  transform: scale(1.01);
}

.drop-zone.has-file {
  border-style: solid;
  border-color: rgba(79, 70, 229, 0.3);
  padding: 20px;
  cursor: default;
}

.drop-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  pointer-events: none;
}

.drop-sub {
  font-size: 13px;
  color: var(--text-secondary);
  pointer-events: none;
}

.drop-icon {
  color: var(--primary);
  margin-bottom: 16px;
  animation: float 3s ease-in-out infinite;
  pointer-events: none;
}

/* File Preview */
.file-preview {
  display: flex;
  align-items: center;
  gap: 14px;
}

.file-icon {
  font-size: 32px;
}

.file-info {
  flex: 1;
  text-align: left;
}

.file-name {
  display: block;
  font-weight: 600;
  font-size: 15px;
  color: var(--text-primary);
}

.file-size {
  font-size: 13px;
  color: var(--text-secondary);
}

.remove-file {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border-radius: 8px;
  padding: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-file:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* Messages */
.upload-error {
  margin-top: 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  padding: 12px;
  border-radius: 10px;
  font-size: 13px;
  text-align: center;
}

.upload-success {
  margin-top: 16px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: #34d399;
  padding: 12px;
  border-radius: 10px;
  font-size: 13px;
  text-align: center;
}

/* Footer */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
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

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.upload-btn {
  background: linear-gradient(to right, var(--primary), #6366f1);
  color: white;
  border: none;
  padding: 10px 28px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
  transition: all 0.2s;
  min-width: 100px;
}

.upload-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
}

.upload-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.upload-btn.loading {
  cursor: wait;
}

.loader {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s ease-in-out infinite;
  display: inline-block;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
