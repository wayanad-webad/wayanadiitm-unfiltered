<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold text-gray-800">Admin Dashboard</h1>
            </div>
          </div>
          <div class="flex items-center">
             <button @click="downloadCSV" class="mr-4 px-3 py-2 rounded-md text-sm font-medium text-white bg-green-600 hover:bg-green-700 transition-colors">
              Download CSV
            </button>
            <button @click="logout" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="py-10">
      <header>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold leading-tight text-gray-900">
            Feedbacks
          </h1>
        </div>
      </header>
      <main>
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <div class="px-4 py-8 sm:px-0">
            <div v-if="loading" class="text-center text-gray-500">Loading...</div>
            <div v-else-if="feedbacks.length === 0" class="text-center text-gray-500">No feedbacks yet.</div>
            
            <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <div v-for="feedback in feedbacks" :key="feedback._id" class="bg-white overflow-hidden shadow rounded-lg relative group">
                <button 
                    @click="deleteFeedback(feedback._id)"
                    class="absolute top-2 right-2 text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                    title="Delete Feedback"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                </button>
                <div class="px-4 py-5 sm:p-6">
                  <p class="text-gray-900 text-lg whitespace-pre-wrap">{{ feedback.text }}</p>
                  <p class="mt-2 text-xs text-gray-400">
                    {{ formatDate(feedback.created_at) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const feedbacks = ref([]);
const loading = ref(true);
const router = useRouter();

const fetchFeedbacks = async () => {
    loading.value = true;
    try {
        const response = await api.getFeedbacks();
        feedbacks.value = response.data;
    } catch (err) {
        if (err.response && err.response.status === 401) {
            router.push('/admin/login');
        } else {
            console.error(err);
        }
    } finally {
        loading.value = false;
    }
};

const deleteFeedback = async (id) => {
    if (!confirm('Are you sure you want to delete this feedback?')) return;
    try {
        await api.deleteFeedback(id);
        feedbacks.value = feedbacks.value.filter(f => f._id !== id);
    } catch (err) {
        console.error(err);
        alert('Failed to delete feedback');
    }
};

const downloadCSV = async () => {
    if (!confirm('This will download all data and delete it from the database. Are you sure?')) return;
    try {
        const response = await api.exportFeedbacks();
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `feedbacks_${new Date().toISOString()}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Refresh list (should be empty now)
        fetchFeedbacks();
    } catch (err) {
        console.error(err);
        alert('Failed to download CSV');
    }
};

const formatDate = (dateString) => {
    if (!dateString) return 'Invalid Date';
    return new Date(dateString).toLocaleString();
};

const logout = () => {
    localStorage.removeItem('token');
    router.push('/admin/login');
};

onMounted(() => {
    fetchFeedbacks();
});
</script>
