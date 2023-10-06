<template>
  <BaseSelectFilter :propOptions="factoryOpts"></BaseSelectFilter>
</template>

<script setup>
import BaseSelectFilter from '../base/BaseSelectFilter.vue'
import { inject } from 'vue'

const UnitRefs = inject('UnitRefs')
const UnitData = UnitRefs.data

const factoryOpts = []

function upperFirst(val) {
  return val.charAt(0).toUpperCase() + val.slice(1)
}

function factoryLabel(unit) {
  return UnitData[unit].name + " (" + upperFirst(UnitData[unit].faction) + ")"
}

for (const unit in UnitData) {
  if (!UnitData[unit].categories.isFactory || !UnitData[unit].builds.length) continue;
  factoryOpts.push({ label: factoryLabel(unit), value: unit })
}

</script>
