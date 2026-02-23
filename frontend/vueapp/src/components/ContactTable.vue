<template>
  <div class="table-container">
    <div v-if="contacts.length === 0" class="empty-state">
      <div class="empty-icon">📂</div>
      <h3>No Contacts Found</h3>
      <p>Upload a VCF file or create your first contact to see them here.</p>
    </div>

    <table v-else class="contact-table">
      <thead>
        <tr>
          <th>Name</th>
          
          <th>Phone Numbers</th>
          <th>Emails</th>
          <th>Address</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="contact in contacts" :key="contact.id">
          <td class="name-col">
            <div class="name-inner">
              <div class="avatar">{{ contact.first_name.charAt(0) }}{{ contact.last_name.charAt(0) }}</div>
              <div class="name-text">{{ contact.first_name }} {{ contact.last_name }}</div>
            </div>
          </td>
          <td class="comm-col">
            <div class="comm-list">
              <div v-for="phone in getPhones(contact.communications)" :key="phone.id" class="comm-badge phone">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" class="badge-icon" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                {{ phone.value }}
                <span class="comm-label" v-if="phone.label">{{ formatLabel(phone.label) }}</span>
              </div>
              <span v-if="getPhones(contact.communications).length === 0" class="placeholder">—</span>
            </div>
          </td>
          <td class="comm-col">
            <div class="comm-list">
              <div v-for="email in getEmails(contact.communications)" :key="email.id" class="comm-badge email">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" class="badge-icon" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                {{ email.value }}
                <span class="comm-label" v-if="email.label">{{ formatLabel(email.label) }}</span>
              </div>
              <span v-if="getEmails(contact.communications).length === 0" class="placeholder">—</span>
            </div>
          </td>
          <td class="address-col">
            <div v-if="contact.address" class="address-text">
              <div v-for="(line, index) in contact.address.split(',').map(s => s.trim()).filter(Boolean)" :key="index">
                {{ line }}
              </div>
            </div>
            <span v-else class="placeholder">—</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  contacts: {
    type: Array,
    required: true,
    default: () => []
  }
});

// Helper functions to filter communications
const getPhones = (comms) => comms.filter(c => c.comm_type === 'phone' || c.comm_type === 'tel' || c.comm_type === 'cell');
const getEmails = (comms) => comms.filter(c => c.comm_type === 'email');

const formatLabel = (label) => {
  if (!label) return '';
  return label.split(',')[0].toUpperCase();
};
</script>

<style scoped>
.table-container {
  width: 100%;
  background: var(--surface);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--surface-border);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3);
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeUp {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.empty-state {
  padding: 80px 20px;
  text-align: center;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
}

.empty-state h3 {
  color: var(--text-primary);
  font-size: 20px;
  margin-bottom: 8px;
}

.contact-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.contact-table th {
  padding: 16px 24px;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-secondary);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.1);
}

.contact-table td {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  vertical-align: middle;
}

.contact-table tbody tr {
  transition: background 0.2s ease;
  cursor: default;
}

.contact-table tbody tr:hover {
  background: rgba(79, 70, 229, 0.1);
}

.contact-table tbody tr:last-child td {
  border-bottom: none;
}

/* Specific Columns */
.name-col {
  font-weight: 500;
}

.name-inner {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary), #818cf8);
  color: white;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);
}

.name-text {
  color: var(--text-primary);
  font-size: 15px;
}

.company-col, .address-col {
  color: var(--text-secondary);
  font-size: 14px;
}

.address-text {
  max-width: 300px;
  line-height: 1.5;
}

.address-text div {
  margin-bottom: 2px;
}

.comm-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.comm-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  width: fit-content;
}

.comm-label {
  font-size: 10px;
  opacity: 0.6;
  margin-left: -2px;
}

.badge-icon {
  opacity: 0.7;
}

.comm-badge.phone {
  background: rgba(16, 185, 129, 0.1);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.comm-badge.email {
  background: rgba(56, 189, 248, 0.1);
  color: #7dd3fc;
  border: 1px solid rgba(56, 189, 248, 0.2);
}

.placeholder {
  color: rgba(255, 255, 255, 0.2);
  font-size: 14px;
}
</style>
