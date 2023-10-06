<template>
  <q-page padding>
    <!-- content -->
    <div class="q-pa-md q-gutter-md">
      <q-card>
        <q-card-section class="bg-primary text-white">
          <div class="text-h6 col-12">
            <label>Results</label>
          </div>
        </q-card-section>
        <q-card-section>
          <p v-if="!hasValidFactories">
            <em>Add more factories and queues for them to proceed</em>
          </p>
          <div v-else>
            <p>{{ avgRes }}</p>
            <p>{{ maxMetalRes }}</p>
            <p>{{ minMetalRes }}</p>
            <p>{{ maxEnergyRes }}</p>
            <p>{{ minEnergyRes }}</p>
          </div>
        </q-card-section>
      </q-card>
      <RepeatFactory class='q-pa-md' v-for="(fac, idx) in factories" :key="idx" :idx="idx" @deleteFactory="deleteFactory"
        @updateFactory="updateFactory"></RepeatFactory>
      <div class="q-pa-md" style="padding-bottom: 220px">
        <div>
          <q-fab v-model="fab1" label="Actions" label-position="left" color="positive" icon="keyboard_arrow_right"
            direction="right">
            <q-fab-action color="secondary" @click="addNewFactory()" icon="add" label="Add new factory" />
          </q-fab>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import RepeatFactory from '../components/repeat-tool/RepeatFactory.vue'
import { ref, watch, reactive, nextTick, inject } from 'vue';

const UnitRefs = inject('UnitRefs')
const UnitData = UnitRefs.data

const factories = reactive([{}])

function newFactoryID() {
}

const addNewFactory = () => {
  factories.push({})
}

const fab1 = ref(true)

const deleteFactory = (idx) => {
  factories.splice(idx, 1)
}

const updateFactory = (idx, newFac) => {
  console.log('hi new fac')
  factories[idx] = newFac
}

function unitLabel(unit) {
  return UnitData[unit].name
}


const hasValidFactories = ref(false)
const maxMetalRes = ref('')
const minMetalRes = ref('')
const maxEnergyRes = ref('')
const minEnergyRes = ref('')
const avgRes = ref('')

function sum(arr) {
  return arr.reduce((a, b) => a + b, 0);
}

watch(factories, () => {
  console.log('watch fac')
  const maxMetalArr = []
  const maxEnergyArr = []
  const minMetalArr = []
  const minEnergyArr = []
  const avgMetalArr = []
  const avgEnergyArr = []
  let found = false
  factories.forEach(fac => {
    console.log(fac)
    if (!fac.name) return
    if (!fac.bp) return
    if (!fac.queue) return
    if (!fac.queue.length) return
    console.log('fac is good')
    found = true
    //collect the max and mins of both metal/s and energy/s
    let maxMetal = Number.NEGATIVE_INFINITY
    let maxMetalUnit = ''
    let minMetal = Number.POSITIVE_INFINITY
    let minMetalUnit = ''
    let maxEnergy = Number.NEGATIVE_INFINITY
    let maxEnergyUnit = ''
    let minEnergy = Number.POSITIVE_INFINITY
    let minEnergyUnit = ''
    let q = {}

    for (let i = 0; i < fac.queue.length; i++) {
      q = fac.queue[i]
      if (q.mcostPerSec > maxMetal) {
        maxMetal = q.mcostPerSec
        maxMetalUnit = q.unit
      }
      if (q.mcostPerSec < minMetal) {
        minMetal = q.mcostPerSec
        minMetalUnit = q.unit
      }
      if (q.ecostPerSec > maxEnergy) {
        maxEnergy = q.ecostPerSec
        maxEnergyUnit = q.unit
      }
      if (q.ecostPerSec < minEnergy) {
        minEnergy = q.ecostPerSec
        minEnergyUnit = q.unit
      }
    }
    maxMetalArr.push({ name: fac.name, bp: fac.bp, res: maxMetal, unit: maxMetalUnit })
    minMetalArr.push({ name: fac.name, bp: fac.bp, res: minMetal, unit: minMetalUnit })
    maxEnergyArr.push({ name: fac.name, bp: fac.bp, res: maxEnergy, unit: maxEnergyUnit })
    minEnergyArr.push({ name: fac.name, bp: fac.bp, res: minEnergy, unit: minEnergyUnit })
    avgMetalArr.push(fac.avgMetal)
    avgEnergyArr.push(fac.avgEnergy)
  })
  if (!found) {
    hasValidFactories.value = false
    return
  }
  hasValidFactories.value = true
  const maxMetalStrArr = []
  let maxMetalSum = 0
  maxMetalArr.forEach(el => {
    maxMetalSum += el.res
    maxMetalStrArr.push(unitLabel(el.unit) + ' at ' + unitLabel(el.name) + " (with " + el.bp + " bp)")
  })
  let minMetalSum = 0
  const minMetalStrArr = []
  minMetalArr.forEach(el => {
    minMetalSum += el.res
    minMetalStrArr.push(unitLabel(el.unit) + ' at ' + unitLabel(el.name) + " (with " + el.bp + " bp)")
  })
  let maxEnergySum = 0
  const maxEnergyStrArr = []
  maxEnergyArr.forEach(el => {
    maxEnergySum += el.res
    maxEnergyStrArr.push(unitLabel(el.unit) + ' at ' + unitLabel(el.name) + " (with " + el.bp + " bp)")
  })
  let minEnergySum = 0
  const minEnergyStrArr = []
  minEnergyArr.forEach(el => {
    minEnergySum += el.res
    minEnergyStrArr.push(unitLabel(el.unit) + ' at ' + unitLabel(el.name) + " (with " + el.bp + " bp)")
  })
  avgRes.value = 'On average your factories in total will consume ' + Math.round(sum(avgMetalArr) * 100) / 100 + ' metal/s' +
    ' and ' + Math.round(sum(avgEnergyArr) * 100) / 100 + " energy/s"

  maxMetalRes.value = "The maximum metal/s you could potentially consume is " + Math.round(maxMetalSum * 100) / 100 +
    " when producing " + maxMetalStrArr.join(', ')
  minMetalRes.value = "The minimum metal/s you could potentially consume is " + Math.round(minMetalSum * 100) / 100 +
    " when producing " + minMetalStrArr.join(', ')
  maxEnergyRes.value = "The maximum energy/s you could potentially consume is " + Math.round(maxEnergySum * 100) / 100 +
    " when producing " + maxEnergyStrArr.join(', ')
  minEnergyRes.value = "The minimum energy/s you could potentially consume is " + Math.round(minEnergySum * 100) / 100 +
    " when producing " + minEnergyStrArr.join(', ')
})

</script>
