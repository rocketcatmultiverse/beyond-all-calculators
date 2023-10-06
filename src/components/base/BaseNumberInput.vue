<template>
  <div>
    <q-input dense v-model.number="model" @update:model-value="$emit('onUpdate', $props.val, model)" type="number"
      style="max-width: 100px" filled />
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  props: ['val'],
  setup(val) {
    return {
      model: ref(0),
    }
  }
}
</script>
