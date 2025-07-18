<template>
  <div>
    <h3>Función de Valor</h3>
    <table class="table">
      <thead>
        <tr>
          <th>Periodo</th>
          <th v-for="(_, i) in data[0]" :key="i">I={{ i }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, t) in data" :key="t">
          <td>{{ t }}</td>
          <td v-for="(val, i) in row" :key="i">{{ val.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
const props = defineProps({ data: Array });
</script>