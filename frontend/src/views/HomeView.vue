<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <div class="flex-grow flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-2xl relative overflow-hidden my-8">
        <!-- Decorative background element -->
        <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-500 to-purple-600"></div>
        
        <div>
          <img src="/logo.png" alt="Logo" class="mx-auto h-20 w-20 rounded-full object-cover mb-4" />
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Submit Anonymously
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Your opinion matters to us. Share your thoughts anonymously. We never collect your personal information.
          </p>
        </div>
        
        <form class="mt-8 space-y-6" @submit.prevent="submit">
          <div class="rounded-md shadow-sm -space-y-px">
            <div>
              <label for="feedback" class="sr-only">Your Feedback</label>
              <textarea
                id="feedback"
                name="feedback"
                rows="5"
                required
                v-model="text"
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="What's on your mind?"
              ></textarea>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
            >
              <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                <!-- Heroicon name: solid/paper-airplane -->
                <svg class="h-5 w-5 text-blue-500 group-hover:text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
              </span>
              <span v-if="!loading">Submit Your Feedback</span>
              <span v-else>Sending...</span>
            </button>
          </div>
          
          <div v-if="message" :class="`text-center text-sm ${error ? 'text-red-500' : 'text-green-500'}`">
              {{ message }}
          </div>
        </form>
      </div>
    </div>
    
    <footer class="w-full py-6 text-center text-sm text-gray-500 bg-gray-100 border-t border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p>For concerns or any queries requiring direct assistance or official follow-ups, please contact us at - <a href="mailto:wayanad-studrel@ds.study.iitm.ac.in" class="text-blue-600 hover:text-blue-500">wayanad-studrel@ds.study.iitm.ac.in</a>.</p>
        <p class="mt-2 font-medium">Credit: Wayanad Web Admin & the WebOps team.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../api';

const text = ref('');
const loading = ref(false);
const message = ref('');
const error = ref(false);

const submit = async () => {
    if (!text.value.trim()) return;
    
    loading.value = true;
    message.value = '';
    error.value = false;
    
    try {
        await api.submitFeedback({ text: text.value });
        message.value = 'Thank you! Your feedback has been sent anonymously.';
        text.value = '';
    } catch (err) {
        error.value = true;
        message.value = 'Something went wrong. Please try again.';
    } finally {
        loading.value = false;
    }
};
</script>
