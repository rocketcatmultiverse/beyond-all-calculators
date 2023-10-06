<template>
  <div class="q-pa-md col-auto">
    <q-expansion-item expand-separator icon="add" class="shadow-1 overflow-hidden" style="border-radius: 30px"
      label="Add additional buildpower" header-class="bg-primary text-white" expand-icon-class="text-white">
      <q-table dense :rows-per-page-options="[0, 5, 10]" title="Add additional buildpower" :rows="rows" :columns="columns"
        row-key="id" :filter="filter" :filter-method="filterSelection">
        <template v-slot:top-left>
          <strong>Total additional buildpower</strong>: {{ totalBuildpower }}
        </template>
        <template v-slot:top-right>
          <q-input class="q-pl-xl" dense debounce="400" color="primary" v-model="search">
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>
        <template v-slot:body-cell-number="props">
          <q-td dense :props="props">
            <div class="my-table-details">
              <BaseNumberInput dense @onUpdate="onNumberInputUpdate" :val="props.row.id">
              </BaseNumberInput>
            </div>
          </q-td>
        </template>
        <template v-slot:body-cell-id="props">
          <q-td :props="props">
            <a clickable target="_blank" :href="'https://www.beyondallreason.info/unit/' + props.value">
              <div>
                <q-badge :label="props.value" :color="props.row.faction === 'armada' ? 'blue' : 'red'" />
              </div>
              <div class="my-table-details">
                {{ props.row.details }}
              </div>
            </a>
          </q-td>
        </template>
      </q-table>

    </q-expansion-item>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import UnitRefs from '../data/unitRefs.js'
import BaseNumberInput from './base/BaseNumberInput.vue';
const columns = [
  { name: 'id', align: 'right', label: 'ID', field: 'id', sortable: true },
  { name: 'name', align: 'left', label: 'Name', field: 'name', sortable: true },
  { name: 'faction', align: 'left', label: 'Faction', field: 'faction', sortable: true },
  { name: 'bp', align: 'left', label: 'Buildpower', field: 'bp', sortable: true, sort: (a, b) => parseInt(a, 10) - parseInt(b, 10) },
  { name: 'number', align: 'left', label: 'To Add', field: 'number' },
  { name: 'total', align: 'left', label: 'Total BP', field: 'total' },
]

const unitRows = []
const buildpowerSelection = ref({})
const UnitData = UnitRefs.data

for (const unit in UnitData) {
  if (!UnitData[unit].bp) continue;
  if (UnitData[unit].categories.isFactory) continue;
  unitRows.push({
    id: unit,
    name: UnitData[unit].name,
    faction: UnitData[unit].faction,
    bp: UnitData[unit].bp,
    number: 0,
    total: 0
  })
  buildpowerSelection.value[unit] = 0
}

const rows = ref(unitRows)

const emit = defineEmits(['bpUpdate'])

const totalBuildpower = computed(() => {
  let sum = 0
  for (const k in buildpowerSelection.value) {
    sum += buildpowerSelection.value[k] * UnitData[k].bp
  }
  emit('bpUpdate', sum)
  return sum
})

const onNumberInputUpdate = (k, v) => {
  buildpowerSelection.value[k] = v;
  for (let i = 0; i < rows.value.length; i++) {
    if (rows.value[i].id !== k) continue;
    rows.value[i].total = rows.value[i].bp * v
    break
  }
}

const search = ref("")

const filter = computed(() => {
  return {
    search: search.value,
  }
})

const filterSelection = (rows, terms) => {
  const lowerSearch = terms.search.toLowerCase()
  const filteredRows = rows.filter((row, i) => {

    let passedSearch = true
    if (lowerSearch !== "") {
      passedSearch = false
      //Get the values
      let passedSearch_values = Object.values(row)
      //Convert to lowercase
      let passedSearch_lower = passedSearch_values.map(x => {
        if (typeof x === 'string') return x.toString().toLowerCase();
        return x
      })
      for (let val = 0; val < passedSearch_lower.length; val++) {
        if (typeof passedSearch_lower[val] !== 'string') continue;
        if (passedSearch_lower[val].includes(lowerSearch)) {
          passedSearch = true
          break
        }
      }

    }

    return passedSearch
  })
  return filteredRows
}


</script>

<style scoped>
.armada-color {
  color: rgb(42, 69, 185) !important;
}

.cortex-color {
  color: rgb(182, 50, 50) !important;
}
</style>
