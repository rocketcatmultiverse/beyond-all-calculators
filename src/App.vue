<template>
  <router-view />
</template>

<script setup>
import { provide } from 'vue'
import UnitRefs from './data/unitRefs'

provide('UnitRefs', UnitRefs)
</script>
