<template>
  <div class="q-pa-md">
    <q-carousel arrows animated v-model="slide" height="400px">
      <q-carousel-slide name="first" img-src="../../img/bac-explorer.png">
        <div class="absolute-bottom custom-caption">
          <div class="text-h2">Explore BAR</div>
          <div class="text-subtitle1">In depth information in tabular form, exportable to CSV</div>
        </div>
      </q-carousel-slide>
      <q-carousel-slide name="second" img-src="../../img/bac-cost.png">
        <div class="absolute-bottom custom-caption">
          <div class="text-h2">Calculate Costs</div>
          <div class="text-subtitle1">Calculate metal and energy usage</div>
        </div>
      </q-carousel-slide>
      <q-carousel-slide name="third" img-src="../../img/bac-repeat.png">
        <div class="absolute-bottom custom-caption">
          <div class="text-h2">Repeat Queue Calculator</div>
          <div class="text-subtitle1">Calculate average, min, and max costs of production queues in multiple factories
          </div>
        </div>
      </q-carousel-slide>
    </q-carousel>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    return {
      slide: ref('first')
    }
  }
}
</script>

<style lang="sass" scoped>
.custom-caption
  text-align: center
  padding: 12px
  color: white
  background-color: rgba(0, 0, 0, .3)
</style>
