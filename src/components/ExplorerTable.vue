<template>
  <div class="q-pa-md">
    <q-table flat bordered title="BAR Explorer" :rows="originalRows" :columns="columns" row-key="id"
      :visible-columns="visibleColumns" :filter="filter" :filter-method="filterSelection"
      :rows-per-page-options="[20, 50, 100, 200, 0]">
      <template v-slot:top="props">

        <q-space />
        <div class="col">
          <div class="col">
            <strong>Column toggles:</strong>
            <q-toggle v-for="col in optionalColumns" :key="col.name" v-model="visibleColumns" :val="col.name"
              :label="col.label"></q-toggle>
            <!-- <q-toggle v-model="visibleColumns" />
            <q-toggle v-model="visibleColumns" val="category" label="Category" />
            <q-toggle v-model="visibleColumns" val="type" label="Type" />
            <q-toggle v-model="visibleColumns" val="desc" label="Description" />
            <q-toggle v-model="visibleColumns" val="faction" label="Faction" />
            <q-toggle v-model="visibleColumns" val="energy" label="Energy Cost" />
            <q-toggle v-model="visibleColumns" val="metal" label="Metal Cost" />
            <q-toggle v-model="visibleColumns" val="build" label="Build cost" />
            <q-toggle v-model="visibleColumns" val="epb" label="Energy per buildcost (EPB)" />
            <q-toggle v-model="visibleColumns" val="mpb" label="Metal per buildcost (MPB)" />
            <q-toggle v-model="visibleColumns" val="bp" label="Buildpower" />
            <q-toggle v-model="visibleColumns" val="los" label="Line of Sight" />
            <q-toggle v-model="visibleColumns" val="speed" label="Speed" />
            <q-toggle v-model="visibleColumns" val="hp" label="HP" />
            <q-toggle v-model="visibleColumns" val="radar" label="Radar" /> -->
          </div>
          <div class="col">
            <strong>Filter toggles:</strong>
            <q-toggle v-model="filteredFactions" val="armada" label="Armada" />
            <q-toggle v-model="filteredFactions" val="cortex" label="Cortex" />
            <q-toggle v-model="filteredTiers" val="1" label="T1" />
            <q-toggle v-model="filteredTiers" val="2" label="T2" />
            <q-toggle v-model="filteredTiers" val="3" label="T3" />
            <q-toggle v-model="filteredTypes" val="unit" label="Units" />
            <q-toggle v-model="filteredTypes" val="building" label="Building" />
            <q-toggle v-for="(subtypeLabel, subtypeKey) in filterableSubtypes" :key="subtypeKey" v-model="filteredSubypes"
              :val="subtypeKey" :label="subtypeLabel" />
          </div>
        </div>
        <q-input class="q-pl-xl" dense debounce="400" color="primary" v-model="search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-btn flat round dense :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
          @click="props.toggleFullscreen" class="q-ml-md" />
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
  </div>
  <div class="q-pa-md" style="padding-bottom: 220px">
    <div>
      <q-fab v-model="fab1" label="Actions" label-position="left" color="positive" icon="keyboard_arrow_right"
        direction="right">
        <q-fab-action color="secondary" @click="exportTable(false)" icon="archive" label="Export to CSV (all)" />
        <q-fab-action color="secondary" @click="exportTable(true)" icon="archive"
          label="Export to CSV (apply filtered rows/columns)" />
      </q-fab>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { exportFile, useQuasar } from 'quasar'

const fab1 = ref(true)

const compareInts = (a, b) => parseInt(a, 10) - parseInt(b, 10)

const compareFloats = (a, b) => parseFloat(a) - parseFloat(b)

const formatBool = (bool) => bool ? 'Yes' : 'No'

const columns = ref([
  {
    name: 'id',
    required: true,
    label: 'ID',
    field: row => row.id,
    format: val => `${val}`,
    sortable: true
  },
  {
    name: 'name',
    required: true,
    label: 'Name',
    align: 'left',
    field: row => row.name,
    format: val => `${val}`,
    sortable: true
  },
  {
    name: 'desc',
    label: 'Description',
    field: row => row.desc,
    format: val => `${val}`,
    sortable: true
  },
  {
    name: 'category',
    label: 'Category',
    field: "category",
    sortable: true
  },
  {
    name: 'faction',
    label: 'Faction',
    field: row => row.faction,
    format: val => val.charAt(0).toUpperCase() + val.slice(1),
    sortable: true
  },
  {
    name: 'type',
    label: 'Type',
    field: row => row.type,
    format: val => val.charAt(0).toUpperCase() + val.slice(1),
    sortable: true
  },
  {
    name: 'subtype',
    label: 'Subtype',
    field: row => row.subtype,
    format: val => val.charAt(0).toUpperCase() + val.slice(1),
    sortable: true
  },
  {
    name: 'tier',
    label: 'Tier',
    field: "tier",
    format: val => `T${val}`,
    sortable: true
  },
  { name: 'energy', label: 'Energy cost', field: 'energy', sortable: true, compareInts },
  { name: 'metal', label: 'Metal cost', field: 'metal', sortable: true, compareInts },
  { name: 'build', label: 'Build cost', field: 'build', sortable: true, compareInts },
  { name: 'epb', label: 'EPB', field: 'epb', sortable: true, compareFloats },
  { name: 'mpb', label: 'MPB', field: 'mpb', sortable: true, compareFloats },
  { name: 'bp', label: 'Buildpower', field: 'bp', sortable: true, compareInts },
  { name: 'hp', label: 'HP', field: 'hp', sortable: true, compareInts },
  { name: 'speed', label: 'Speed', field: 'speed', sortable: true, compareInts },
  { name: 'radar', label: 'Radar Range', field: 'radar', sortable: true, compareInts },
  { name: 'jam', label: 'Jamming Range', field: 'jam', sortable: true, compareInts },
  { name: 'sonar', label: 'Sonar Range', field: 'sonar', sortable: true, compareInts },
  { name: 'los', label: 'Line of sight', field: 'los', sortable: true, compareInts },
  { name: 'stealth', label: 'Radar Stealth', field: 'stealth', format: formatBool, sortable: true },
  { name: 'sonarstealth', label: 'Sonar Stealth', field: 'sonarStealth', format: formatBool, sortable: true },
  { name: 'cloak', label: 'Cloakable', field: 'cloak', format: formatBool, sortable: true },
  { name: 'reclaim', label: 'Can Reclaim', field: 'reclaim', format: formatBool, sortable: true },
  { name: 'resurrect', label: 'Can Resurrect', field: 'resurrect', format: formatBool, sortable: true },
])

const optionalColumns = ref(columns.value.filter(col => !col.required))

let unitRows = [];

const UnitRefs = inject('UnitRefs')

for (const unit in UnitRefs.data) {
  unitRows.push({
    id: unit,
    name: UnitRefs.data[unit].name,
    desc: UnitRefs.data[unit].desc,
    faction: UnitRefs.data[unit].faction,
    tier: UnitRefs.data[unit].tier,
    category: UnitRefs.data[unit].category,
    energy: UnitRefs.data[unit].costs.energy,
    metal: UnitRefs.data[unit].costs.metal,
    build: UnitRefs.data[unit].costs.build,
    epb: Math.round(UnitRefs.data[unit].costs.energy / UnitRefs.data[unit].costs.build * 1000) / 1000,
    mpb: Math.round(UnitRefs.data[unit].costs.metal / UnitRefs.data[unit].costs.build * 1000) / 1000,
    bp: UnitRefs.data[unit].bp,
    hp: UnitRefs.data[unit].hp,
    speed: UnitRefs.data[unit].speed,
    radar: UnitRefs.data[unit].radar,
    los: UnitRefs.data[unit].los,
    jam: UnitRefs.data[unit].jam,
    sonar: UnitRefs.data[unit].sonar,
    stealth: UnitRefs.data[unit].stealth,
    sonarStealth: UnitRefs.data[unit].sonarStealth,
    cloak: UnitRefs.data[unit].cloak,
    reclaim: UnitRefs.data[unit].reclaim && !UnitRefs.data[unit].categories.isFactory,
    resurrect: UnitRefs.data[unit].canResurrect,
    type: UnitRefs.data[unit].type,
    subtype: UnitRefs.data[unit].subtype
  })
}
const visibleColumns = ref(['id', 'name', 'desc', 'type', 'subtype', 'tier', 'faction', 'energy', 'metal', 'build'])

const filteredFactions = ref(['armada', 'cortex'])
const filteredTiers = ref(['1', '2', '3'])
const filteredTypes = ref(['unit', 'building'])
const filteredSubypes = ref(['aircraft', 'bot', 'vehicle', 'hovercraft', 'seaplane', 'ship', 'experimental', 'commander',
  'defence', 'economy', 'factory', 'utility', 'sea defence', 'sea economy', 'sea factory', 'sea utility'])
const filterableSubtypes = {
  'aircraft': 'Aircraft',
  'bot': 'Bots',
  'defence': 'Land Defence Buildings',
  'economy': 'Land Economy Buildings',
  'factory': 'Land Factories',
  'utility': 'Land Utility Buildings',
  'sea defence': 'Sea Defence Buildings',
  'sea economy': 'Sea Economy Buildings',
  'sea factory': 'Sea Factories',
  'sea utility': 'Sea Utility Buildings',
  'experimental': 'Experimentals',
  'hovercraft': 'Hovercraft',
  'seaplane': 'Seaplanes',
  'ship': 'Ships',
  'vehicle': 'Vehicles',
  'commander': 'Commanders',
}

const search = ref('')
const filter = computed(() => {
  return {
    search: search.value,
    factions: filteredFactions.value,
    tier: filteredTiers.value,
    type: filteredTypes.value,
    subtype: filteredSubypes.value
  }
})

const filterSelection = (rows, terms) => {
  const lowerSearch = terms.search ? terms.search.toLowerCase() : ""
  const filteredRows = rows.filter((row, i) => {

    if (row.faction && !terms.factions.includes(row.faction.toLowerCase())) return false;
    if (!terms.tier.includes(row.tier)) return false;
    if (!terms.type.includes(row.type)) return false;
    if (!terms.subtype.includes(row.subtype)) return false;
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
  filteredExportTable.value = filteredRows
  return filteredRows
}

const originalRows = ref(unitRows)
const filteredExportTable = ref(unitRows)

function wrapCsvValue(val, formatFn, row) {
  let formatted = formatFn !== void 0
    ? formatFn(val, row)
    : val

  formatted = formatted === void 0 || formatted === null
    ? ''
    : String(formatted)

  formatted = formatted.split('"').join('""')
  /**
   * Excel accepts \n and \r in strings, but some other CSV parsers do not
   * Uncomment the next two lines to escape new lines
   */
  // .split('\n').join('\\n')
  // .split('\r').join('\\r')

  return `"${formatted}"`
}
const $q = useQuasar()
const exportTable = (filtered) => {
  // naive encoding to csv format
  const filteredColumns = !filtered ? columns.value : columns.value.filter(col => visibleColumns.value.includes(col.name))
  // const rows = !filtered ? originalRows.value : filteredExportTable.value
  const rows = !filtered ? originalRows.value : filteredExportTable.value
  const content = [filteredColumns.map(col => wrapCsvValue(col.label))].concat(
    rows.map(row => filteredColumns.map(col => wrapCsvValue(
      typeof col.field === 'function'
        ? col.field(row)
        : row[col.field === void 0 ? col.name : col.field],
      col.format,
      row
    )).join(','))
  ).join('\r\n')

  const status = exportFile(
    'bar-explorer-output.csv',
    content,
    'text/csv'
  )

  if (status !== true) {
    $q.notify({
      message: 'Browser denied file download...',
      color: 'negative',
      icon: 'warning'
    })
  }
}
</script>
<style>
.my-table-details {
  font-size: 0.85em;
  font-style: italic;
  max-width: 200px;
  white-space: normal;
  color: #555;
  margin-top: 4px;
}
</style>
