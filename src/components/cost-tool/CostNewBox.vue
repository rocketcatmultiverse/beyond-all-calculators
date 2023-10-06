<template>
  <div class="q-pa-md">
    <q-stepper v-model="step" ref="stepper" color="primary" animated>
      <q-step :name="1" title="Select a build source" icon="settings" :done="step > 1">
        <BaseSelectFilter label="Builders" :propOptions="builderOpts" v-model="builderValue"></BaseSelectFilter>
      </q-step>

      <q-step :name="2" title="What to build" icon="build" :done="step > 2">
        <BaseSelectFilter label="Build options" :propOptions="buildOptions" v-model="toBuildValue"></BaseSelectFilter>
      </q-step>

      <q-step :name="3" title="Calculate" icon="calculate" :done="step > 3">
        {{ UnitData[builderValue.value].name }} has <strong>{{ UnitData[builderValue.value].bp }}</strong> buildpower.
        <br />
        <strong>Total buildpower including selection:</strong> {{ totalBp }}<br />
        {{ UnitData[toBuildValue.value].name }} costs {{ costsToBuild.metal }} Metal, {{ costsToBuild.energy }} Energy,
        and {{
          costsToBuild.build }} Buildpower.
        <br />
        With {{ totalBp }} Buildpower you will spend {{ massPerSecondRounded }}
        m/s and {{
          energyPerSecondRounded }} e/s to complete <strong>{{ UnitData[toBuildValue.value].name }}</strong> in
        {{ timeToBuildRounded }} seconds.
        <BuildpowerTable dense @bpUpdate="updateBuildpower" />
      </q-step>

      <template v-slot:navigation>
        <q-stepper-navigation>
          <q-btn v-if="step < 3" :disabled="inputInvalid" @click="$refs.stepper.next()" color="primary"
            :label="step === 3 ? 'Finish' : 'Continue'" />
          <q-btn v-if="step > 1" flat color="primary" @click="$refs.stepper.previous()" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </template>
    </q-stepper>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseSelectFilter from '../base/BaseSelectFilter.vue'
import UnitRefs from '../../data/unitRefs.js'
import BuildpowerTable from '../BuildpowerTable.vue'

const builderValue = ref(null)

const builderOpts = []
const validBuilderOpts = []
const bpValues = {}
const UnitData = UnitRefs.data


function upperFirst(val) {
  return val.charAt(0).toUpperCase() + val.slice(1)
}

function unitRefToExpandedName(ref) {
  return UnitData[ref].name + " (" + upperFirst(UnitData[ref].faction) + ")"
}

function unitIdToExpandedName(id) {
  const ref = UnitRefs.refNameFromId[id]
  return unitRefToExpandedName(ref)
}

for (const unit in UnitData) {
  if (UnitData[unit].builds.length) builderOpts.push({
    label: unitRefToExpandedName(unit),
    value: unit
  })
  validBuilderOpts.push(unit)
  if (UnitData[unit].bp) bpValues[unit] = UnitData[unit].bp;
}

const inputInvalid = computed(() => {
  if (step.value === 1) {
    if (!builderValue.value) return true;
    return !validBuilderOpts.includes(builderValue.value.value)
  }
  if (step.value === 2) {
    if (!toBuildValue.value) return true;
    return !UnitData[builderValue.value.value].builds.includes(UnitData[toBuildValue.value.value].id)
  }
  if (step.value === 3 || step.value === 4) {
    return false;
  }
  return true;
})

const toBuildValue = ref(null)

const buildOptions = computed(() => {
  if (step.value <= 1) return null;
  const res = []
  //.builds contains the numerical ids, so convert them to the 'string ids' called refs here
  UnitData[builderValue.value.value].builds.forEach(id => {
    const ref = UnitRefs.refNameFromId[id]
    if (!UnitData[ref]) return
    res.push({ value: ref, label: unitRefToExpandedName(ref) })
  })
  return res
})

const additionalBp = ref(0)

const updateBuildpower = (bp) => {
  additionalBp.value = bp
}

const totalBp = computed(() => {
  if (!builderValue.value) return 0
  return UnitData[builderValue.value.value].bp + additionalBp.value
})

const costsToBuild = computed(() => {
  if (!toBuildValue.value) return 0;
  return UnitData[toBuildValue.value.value].costs
})

const massPerSecondPerBp = computed(() => {
  if (!toBuildValue.value) return 0;
  return costsToBuild.value.metal / totalBp.value
})

const energyPerSecondPerBp = computed(() => {
  if (!toBuildValue.value) return 0;
  return costsToBuild.value.energy / totalBp.value
})

const timeToBuild = computed(() => {
  if (!toBuildValue.value) return 0;
  return costsToBuild.value.build / totalBp.value
})

const massPerSecond = computed(() => {
  if (!toBuildValue.value) return 0;
  return totalBp.value * massPerSecondPerBp.value / timeToBuild.value
})

const energyPerSecond = computed(() => {
  if (!toBuildValue.value) return 0;
  return totalBp.value * energyPerSecondPerBp.value / timeToBuild.value
})

const massPerSecondRounded = computed(() => {
  if (!toBuildValue.value) return 0;
  return Math.round(totalBp.value * massPerSecondPerBp.value * 100 / timeToBuild.value) / 100
})

const energyPerSecondRounded = computed(() => {
  if (!toBuildValue.value) return 0;
  return Math.round(totalBp.value * energyPerSecondPerBp.value * 100 / timeToBuild.value) / 100
})

const timeToBuildRounded = computed(() => {
  if (!toBuildValue.value) return 0;
  return Math.round(costsToBuild.value.build * 100 / totalBp.value) / 100
})

const step = ref(1)

</script>
