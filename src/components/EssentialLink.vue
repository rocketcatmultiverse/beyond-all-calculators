<template>
  <a style="all: unset" v-if="linkIsExternal" target="_blank" :href="link">
    <q-item clickable>
      <q-item-section v-if="icon" avatar>
        <q-icon :name="icon" />
      </q-item-section>

      <q-item-section>
        <q-item-label>{{ title }}</q-item-label>
        <q-item-label caption>{{ caption }}</q-item-label>
      </q-item-section>
    </q-item>
  </a>
  <router-link style="all: unset" v-if="!linkIsExternal" :to="link">
    <q-item clickable>
      <q-item-section v-if="icon" avatar>
        <q-icon :name="icon" />
      </q-item-section>

      <q-item-section>
        <q-item-label>{{ title }}</q-item-label>
        <q-item-label caption>{{ caption }}</q-item-label>
      </q-item-section>
    </q-item>
  </router-link>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const props = defineProps({
  title: {
    type: String,
    required: true
  },

  linkIsExternal: {
    type: Boolean,
    required: true
  },

  caption: {
    type: String,
    default: ''
  },

  link: {
    type: String,
    default: '#'
  },

  icon: {
    type: String,
    default: ''
  },
})

const goToInternal = () => {
  if (props.linkIsExternal) {
    window.open(props.link, '_blank');
    return;
  }
  router.push(props.link)
}
</script>
