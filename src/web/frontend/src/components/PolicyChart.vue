<template>
  <div>
    <h3>Resumen de Política (s_t, S_t)</h3>
    <canvas ref="chart"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref, defineProps } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({ summary: Array });
const chart = ref(null);

onMounted(() => {
  const ctx = chart.value.getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: props.summary.map(s => `t=${s.period}`),
      datasets: [
        { label: 's_t', data: props.summary.map(s => s.s_t) },
        { label: 'S_t', data: props.summary.map(s => s.S_t) }
      ]
    }
  });
});
</script>