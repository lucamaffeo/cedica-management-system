<script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="greetings">
    <h1 class="text-green-500 font-medium text-4xl relative -top-2">{{ msg }}</h1>
  </div>
</template>
