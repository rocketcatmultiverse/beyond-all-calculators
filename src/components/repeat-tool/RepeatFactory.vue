<template>
  <q-card class="col-12">
    <q-card-section class="bg-primary text-white">
      <div v-if="!selectedFactory" class="text-h6 col-12">
        <label>Define factory:</label>
        <RepeatSelectFactory v-model="selectedFactoryObj"></RepeatSelectFactory>
      </div>
      <div v-else class="text-h6 col-12">
        {{ selectedFactoryName }}
        <q-btn color="negative" label="Delete Factory" @click="$emit('deleteFactory', props.idx)" />
      </div>
    </q-card-section>

    <q-separator />

    <q-card-actions v-if="selectedFactory">
      <div class="text-h6 col-12">
        <p v-if="factory.queue && factory.queue.length">This factory's repeat queue (average {{
          Math.round(factory.avgMetal * 100) / 100 }} m/s,
          {{ Math.round(factory.avgEnergy * 100) / 100 }} e/s):</p>
        <p v-else><em>Nothing in the factory's queue.</em></p>
        <q-list bordered separator>
          <q-item v-for="(q, idx) in factory.queue" :key="idx">
            <q-item-section>
              {{ idx + 1 }}) {{ q.label }} x{{ q.qty }}
              <q-item-label caption>Each takes <strong>{{ q.tRounded }}s</strong> at <strong>{{ q.mcostPerSecRounded }}
                  m/s</strong> & <strong>{{ q.ecostPerSecRounded
                  }} e/s</strong> to produce (Total: {{ Math.round(q.t * q.qty * 100) / 100 }} seconds)</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-btn label="Delete" @click="removeFromQueue(idx)" color="negative"></q-btn>
            </q-item-section>
          </q-item>
        </q-list>
        <RepeatQueue :fac="selectedFactory" @addToQueue="addToQueue"></RepeatQueue>
      </div>
      <div class="text-h6 col-12">
        This factory has {{ totalBuildpower }} buildpower in total.
        <BuildpowerTable @bpUpdate="updateBuildpower"></BuildpowerTable>
      </div>
    </q-card-actions>
  </q-card>
</template>

<script setup>
import RepeatSelectFactory from './RepeatSelectFactory.vue'
import RepeatQueue from './RepeatQueue.vue'
import BuildpowerTable from '../BuildpowerTable.vue'
import { inject, reactive, ref, computed, watch } from 'vue'

const UnitRefs = inject('UnitRefs')
const UnitData = UnitRefs.data

const props = defineProps(['idx'])
const emit = defineEmits(['deleteFactory', 'updateFactory'])

const factory = reactive({})

const selectedFactoryObj = ref(null)
const selectedFactory = computed(() => {
  if (selectedFactoryObj.value !== null && 'value' in selectedFactoryObj.value) {
    const fac = selectedFactoryObj.value.value
    //bit of extra validation
    if (!(fac in UnitData)) return null
    if (!UnitData[fac].categories.isFactory) return null
    return fac
  }
  return null
})

watch(selectedFactory, () => {
  factory.name = selectedFactory.value
})

watch(factory, () => {
  emit('updateFactory', props.idx, factory)
})

function upperFirst(val) {
  return val.charAt(0).toUpperCase() + val.slice(1)
}

function factoryLabel(unit) {
  return UnitData[unit].name + " (" + upperFirst(UnitData[unit].faction) + ")"
}

function unitLabel(unit) {
  return UnitData[unit].name
}

const selectedFactoryName = computed(() => {
  if (selectedFactory.value === null) return null
  return factoryLabel(selectedFactory.value)
})

const additionalBuildpower = ref(0)

const totalBuildpower = computed(() => {
  if (selectedFactory.value === null) return 0
  return UnitData[selectedFactory.value].bp + additionalBuildpower.value
})

const updateBuildpower = (bp) => {
  additionalBuildpower.value = bp
}

function updateQueueTotals() {
  if (!factory.queue || !factory.queue.length) return
  let t = 0
  let mcost = 0
  let ecost = 0
  for (let i = 0; i < factory.queue.length; i++) {
    const unit = factory.queue[i].unit
    mcost += UnitData[unit].costs.metal * factory.queue[i].qty
    ecost += UnitData[unit].costs.energy * factory.queue[i].qty
    t += factory.queue[i].t * factory.queue[i].qty
  }
  if (t <= 0) return
  factory.avgEnergy = ecost / t
  factory.avgMetal = mcost / t

}

watch(totalBuildpower, () => {
  if (factory.queue) {
    for (let i = 0; i < factory.queue.length; i++) {
      updateQueueValuesAtIndex(i)
    }
  }
  updateQueueTotals()
  factory.bp = totalBuildpower.value
})

const updateQueueValuesAtIndex = (idx) => {
  const unit = factory.queue[idx].unit
  const buildcost = UnitData[unit].costs.build
  const mcost = UnitData[unit].costs.metal
  const ecost = UnitData[unit].costs.energy
  const bp = totalBuildpower.value
  const t = buildcost / bp
  const mcostPerSec = mcost / t
  const ecostPerSec = ecost / t
  const tRounded = Math.round(buildcost * 100 / bp) / 100
  const mcostPerSecRounded = Math.round(mcost * 100 / t) / 100
  const ecostPerSecRounded = Math.round(ecost * 100 / t) / 100
  factory.queue[idx].t = t
  factory.queue[idx].mcostPerSec = mcostPerSec
  factory.queue[idx].ecostPerSec = ecostPerSec
  factory.queue[idx].tRounded = tRounded
  factory.queue[idx].mcostPerSecRounded = mcostPerSecRounded
  factory.queue[idx].ecostPerSecRounded = ecostPerSecRounded
}

const addToQueue = (unit, qty) => {
  if (factory.queue && factory.queue.length && factory.queue[factory.queue.length - 1].unit === unit) {
    factory.queue[factory.queue.length - 1].qty += qty

  } else {
    if (!factory.queue) factory.queue = [];
    factory.queue.push({ unit: unit, label: unitLabel(unit), qty: qty })
  }
  updateQueueValuesAtIndex(factory.queue.length - 1)
  updateQueueTotals()
}

const removeFromQueue = (idx) => {
  console.log('try slice')
  factory.queue.splice(idx, 1)
}

</script>
