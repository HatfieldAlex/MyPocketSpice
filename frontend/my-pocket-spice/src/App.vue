<template>
  <div>
    <h1>hello</h1>
    <div v-if="error">{{ error }}</div>
    <pre v-else>{{ data }}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return { 
      data: null,
      error: null
    }
  },
  mounted() {
    fetch('https://my-pocket-spice-backend.onrender.com/api/recipes/')
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then(json => this.data = json)
      .catch(err => {
        this.error = err.message
        console.error('Fetch error:', err)
      })
  }
}
</script>
