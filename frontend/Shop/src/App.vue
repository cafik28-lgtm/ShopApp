<script setup>
import Navbar from './components/NavBar.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
    <Navbar v-if="route.path !== '/login' 
    && route.path !== '/user/register'" />

    <router-view />
</template>