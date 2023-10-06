<template>
  <div class="q-pa-md col-auto">
    <q-expansion-item expand-separator icon="add" class="shadow-1 overflow-hidden" style="border-radius: 30px"
      label="Add units to queue" header-class="bg-primary text-white" expand-icon-class="text-white">
      <q-list bordered separator>
        <q-item v-for="opt in opts" :key="opt.val">
          <q-item-section>
            <q-item-label>{{ opt.label }}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-btn label="Add 1" @click="addToQueue(opt.val, 1)" color="positive"></q-btn>
            <q-btn label="Add 5" @click="addToQueue(opt.val, 5)" color="positive"></q-btn>
          </q-item-section>
          <q-separator></q-separator>
        </q-item>
      </q-list>
    </q-expansion-item>
  </div>
</template>

<script setup>
import { inject } from 'vue'

const props = defineProps(['fac'])
const emit = defineEmits(['addToQueue'])
const UnitRefs = inject('UnitRefs')
const UnitData = UnitRefs.data
const nameFromId = UnitRefs.refNameFromId

const opts = []

const builds = UnitData[props.fac].builds

for (const id of builds) {
  const unit = nameFromId[id]
  opts.push({ val: unit, label: UnitData[unit].name })
}

const addToQueue = (val, qty) => {
  emit('addToQueue', val, qty)
}

</script>

