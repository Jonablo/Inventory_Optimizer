<template>
  <form @submit.prevent="submit()" class="row g-3 mb-4">
    <div class="col-md-4">
      <label>Inventario inicial</label>
      <input v-model.number="form.initial_inventory" type="number" class="form-control" required />
    </div>
    <div class="col-md-4">
      <label>Max Inventario</label>
      <input v-model.number="form.max_inventory" type="number" class="form-control" required />
    </div>
    <div class="col-md-4">
      <label>Max Pedido</label>
      <input v-model.number="form.max_order" type="number" class="form-control" required />
    </div>
    <div class="col-md-4">
      <label>Horizonte</label>
      <input v-model.number="form.horizon" type="number" class="form-control" required />
    </div>
    <div class="col-md-4">
      <label>c_t (JSON)</label>
      <input v-model="form.costs.c" type="text" class="form-control" placeholder="[10,10,...]" required />
    </div>
    <div class="col-md-4">
      <label>h</label>
      <input v-model.number="form.costs.h" type="number" class="form-control" required />
    </div>
    <div class="col-md-4">
      <label>p</label>
      <input v-model.number="form.costs.p" type="number" class="form-control" required />
    </div>
    <div class="col-md-4">
      <label>Soporte demanda</label>
      <input v-model="form.demand_params.support" type="text" class="form-control" placeholder="[0,1,2]" required />
    </div>
    <div class="col-md-4">
      <label>Probabilidades</label>
      <input v-model="form.demand_params.probabilities" type="text" class="form-control" placeholder="[0.3,0.4,0.3]" required />
    </div>
    <div class="col-12">
      <button type="submit" class="btn btn-primary">Optimizar</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, defineEmits } from 'vue';
const emit = defineEmits(['submitted']);
const form = reactive({
  initial_inventory: 0,
  max_inventory: 5,
  max_order: 5,
  horizon: 3,
  costs: { c: '[10,10,10]', h: 2, p: 20 },
  demand_params: { support: '[0,1,2]', probabilities: '[0.3,0.4,0.3]' }
});

function submit() {
  const payload = {
    initial_inventory: form.initial_inventory,
    max_inventory: form.max_inventory,
    max_order: form.max_order,
    horizon: form.horizon,
    costs: { c: JSON.parse(form.costs.c), h: form.costs.h, p: form.costs.p },
    demand_params: { support: JSON.parse(form.demand_params.support), probabilities: JSON.parse(form.demand_params.probabilities) }
  };
  emit('submitted', payload);
}
</script>