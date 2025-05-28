<script setup lang="ts">
import { ref } from 'vue'
import { useAdminStore } from '../../stores/adminStore'
import { toast } from 'vue3-toastify'

const adminStore = useAdminStore()

const settings = ref({
  siteSettings: {
    siteName: 'AIFilm',
    siteDescription: 'AI-powered movie recommendations',
    maintenanceMode: false,
    allowRegistration: true
  },
  emailSettings: {
    smtpHost: '',
    smtpPort: '',
    smtpUser: '',
    smtpPassword: '',
    senderEmail: '',
    senderName: ''
  },
  aiSettings: {
    apiKey: '',
    modelName: 'gpt-4',
    maxTokens: 2000,
    temperature: 0.7
  },
  backupSettings: {
    autoBackup: true,
    backupFrequency: 'daily',
    retentionDays: 30,
    backupTime: '00:00'
  }
})

async function saveSettings(section: string) {
  try {
    // In a real app, make API call to save settings
    await new Promise(resolve => setTimeout(resolve, 500))
    toast.success(`${section} settings saved successfully!`)
  } catch (error) {
    toast.error('Failed to save settings')
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-white mb-8">System Settings</h1>

    <div class="space-y-8">
      <!-- Site Settings -->
      <div class="glass-panel p-6">
        <h2 class="text-xl font-semibold text-white mb-6">Site Settings</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Site Name</label>
            <input 
              type="text" 
              v-model="settings.siteSettings.siteName"
              class="form-input w-full"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Site Description</label>
            <textarea 
              v-model="settings.siteSettings.siteDescription"
              class="form-input w-full"
              rows="3"
            ></textarea>
          </div>
          
          <div class="flex items-center">
            <input 
              type="checkbox" 
              v-model="settings.siteSettings.maintenanceMode"
              class="form-checkbox rounded text-primary-600"
            />
            <span class="ml-2 text-gray-300">Maintenance Mode</span>
          </div>
          
          <div class="flex items-center">
            <input 
              type="checkbox" 
              v-model="settings.siteSettings.allowRegistration"
              class="form-checkbox rounded text-primary-600"
            />
            <span class="ml-2 text-gray-300">Allow New Registrations</span>
          </div>
          
          <button @click="saveSettings('Site')" class="btn btn-primary">
            Save Site Settings
          </button>
        </div>
      </div>

      <!-- Email Settings -->
      <div class="glass-panel p-6">
        <h2 class="text-xl font-semibold text-white mb-6">Email Settings</h2>
        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">SMTP Host</label>
              <input 
                type="text" 
                v-model="settings.emailSettings.smtpHost"
                class="form-input w-full"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">SMTP Port</label>
              <input 
                type="text" 
                v-model="settings.emailSettings.smtpPort"
                class="form-input w-full"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">SMTP Username</label>
              <input 
                type="text" 
                v-model="settings.emailSettings.smtpUser"
                class="form-input w-full"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">SMTP Password</label>
              <input 
                type="password" 
                v-model="settings.emailSettings.smtpPassword"
                class="form-input w-full"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Sender Email</label>
              <input 
                type="email" 
                v-model="settings.emailSettings.senderEmail"
                class="form-input w-full"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Sender Name</label>
              <input 
                type="text" 
                v-model="settings.emailSettings.senderName"
                class="form-input w-full"
              />
            </div>
          </div>
          
          <button @click="saveSettings('Email')" class="btn btn-primary">
            Save Email Settings
          </button>
        </div>
      </div>

      <!-- AI Settings -->
      <div class="glass-panel p-6">
        <h2 class="text-xl font-semibold text-white mb-6">AI Settings</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">API Key</label>
            <input 
              type="password" 
              v-model="settings.aiSettings.apiKey"
              class="form-input w-full"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Model Name</label>
            <select 
              v-model="settings.aiSettings.modelName"
              class="form-input w-full"
            >
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Max Tokens</label>
            <input 
              type="number" 
              v-model="settings.aiSettings.maxTokens"
              class="form-input w-full"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Temperature</label>
            <input 
              type="number" 
              v-model="settings.aiSettings.temperature"
              step="0.1"
              min="0"
              max="1"
              class="form-input w-full"
            />
          </div>
          
          <button @click="saveSettings('AI')" class="btn btn-primary">
            Save AI Settings
          </button>
        </div>
      </div>

      <!-- Backup Settings -->
      <div class="glass-panel p-6">
        <h2 class="text-xl font-semibold text-white mb-6">Backup Settings</h2>
        <div class="space-y-4">
          <div class="flex items-center">
            <input 
              type="checkbox" 
              v-model="settings.backupSettings.autoBackup"
              class="form-checkbox rounded text-primary-600"
            />
            <span class="ml-2 text-gray-300">Enable Automatic Backups</span>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Backup Frequency</label>
            <select 
              v-model="settings.backupSettings.backupFrequency"
              class="form-input w-full"
            >
              <option value="hourly">Hourly</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Retention Days</label>
            <input 
              type="number" 
              v-model="settings.backupSettings.retentionDays"
              class="form-input w-full"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Backup Time</label>
            <input 
              type="time" 
              v-model="settings.backupSettings.backupTime"
              class="form-input w-full"
            />
          </div>
          
          <button @click="saveSettings('Backup')" class="btn btn-primary">
            Save Backup Settings
          </button>
        </div>
      </div>
    </div>
  </div>
</template>