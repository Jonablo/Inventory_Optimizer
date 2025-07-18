// --- src/App.vue ---
<template>
  <div class="container py-4">
    <h1 class="mb-4">Inventory Optimizer</h1>
    <OptimizationForm @submitted="onSubmit" />
    <ResultsTable v-if="results" :data="results" />
    <PolicyChart v-if="policySummary" :summary="policySummary" />
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import OptimizationForm from './components/OptimizationForm.vue';
import ResultsTable from './components/ResultsTable.vue';
import PolicyChart from './components/PolicyChart.vue';

const results = ref(null);
const policySummary = ref(null);

function onSubmit(payload) {
  axios.post('/api/optimization/', payload)
    .then(r => {
      results.value = r.data.value_function;
      return axios.get(`/api/optimization/${r.data.optimization_id}/policy-summary`);
    })
    .then(r => policySummary.value = r.data)
    .catch(err => console.error(err));
}
</script>