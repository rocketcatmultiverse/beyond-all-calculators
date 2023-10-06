<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          Beyond All Calculators
        </q-toolbar-title>

        <!-- <div>Quasar v{{ $q.version }}</div> -->
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header>
          Navigation
        </q-item-label>

        <EssentialLink v-for="link in internalLinks" :key="link.title" v-bind="link" :link-is-external="false" />
      </q-list>
      <q-list>
        <q-item-label header>
          Tools
        </q-item-label>

        <EssentialLink v-for="link in toolLinks" :key="link.title" v-bind="link" :link-is-external="false" />
      </q-list>
      <q-list>
        <q-item-label header>
          External Links
        </q-item-label>

        <EssentialLink v-for="link in externalLinks" :key="link.title" v-bind="link" :link-is-external="true" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const toolLinks = [
  {
    title: 'BAR Explorer',
    caption: 'Explore units and structures in filterable, tabular form',
    icon: 'school',
    link: '/explorer'
  },
  {
    title: 'Cost Calculator',
    caption: 'Calculate mass/s and energy/s given buildpower',
    icon: 'calculate',
    link: '/cost-calculator'
  },
  {
    title: 'Repeat Production Calculator',
    caption: 'Calculate repeat production queues over time',
    icon: 'functions',
    link: '/repeat-calculator'
  },
]

const internalLinks = [
  {
    title: 'Home',
    caption: 'Return to the homepage',
    icon: 'home',
    link: '/'
  },
  {
    title: 'About',
    caption: 'About Beyond All Calculators',
    icon: 'info',
    link: '/about'
  },
]

const externalLinks = [

  {
    title: 'Beyond All Reason',
    caption: 'The main website for Beyond All Reason',
    icon: 'img:https://assets.website-files.com/5c68622246b367adf6f3041d/5eda9f834bc6a541c312decd_favicon2020_V5.png',
    link: 'https://www.beyondallreason.info/'
  },
]

const leftDrawerOpen = ref(false)

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

</script>
