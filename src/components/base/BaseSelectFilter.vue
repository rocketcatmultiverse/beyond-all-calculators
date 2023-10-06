<template>
  <q-select filled v-model="model" clearable use-input hide-selected fill-input input-debounce="0" :label="label"
    :options="options" @filter="filterFnAutoselect" @filter-abort="abortFilterFn" style="max-width: 350px;">
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-grey">
          No results
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script>
import { Loading } from 'quasar'
import { ref, reactive, toRef } from 'vue'

export default {
  props: ['label', 'propOptions'],
  setup(props) {
    const options = ref(props.propOptions.map(a => ({ ...a })))

    return {
      model: ref(null),
      options,

      filterFn(val, update, abort) {
        // call abort() at any time if you can't retrieve data somehow

        setTimeout(() => {
          console.log('hi')
          update(
            () => {
              if (val === '') {
                options.value = props.propOptions
              }
              else {
                const needle = val.toLowerCase()
                options.value = props.propOptions.filter(v => v.label.toLowerCase().indexOf(needle) > -1)
              }
            },

            // "ref" is the Vue reference to the QSelect
            ref => {
              if (val !== '' && ref.options.length > 0) {
                ref.setOptionIndex(-1) // reset optionIndex in case there is something selected
                ref.moveOptionSelection(1, true) // focus the first selectable option and do not update the input-value
              }
            }
          )
        }, 100)
      },

      filterFnAutoselect(val, update, abort) {
        // call abort() at any time if you can't retrieve data somehow
        setTimeout(() => {
          update(
            () => {
              if (val === '') {
                options.value = props.propOptions
              }
              else {
                const needle = val.toLowerCase()
                options.value = props.propOptions.filter(v => v.label.toLowerCase().indexOf(needle) > -1)
              }
            },

            // "ref" is the Vue reference to the QSelect
            ref => {
              if (val !== '' && ref.options.length > 0 && ref.getOptionIndex() === -1) {
                ref.moveOptionSelection(1, true) // focus the first selectable option and do not update the input-value
                ref.toggleOption(ref.options[ref.optionIndex], true) // toggle the focused option
              }
            }
          )
        }, 100)
      },

      abortFilterFn() {
        // console.log('delayed filter aborted')
      }
    }
  }
}
</script>
