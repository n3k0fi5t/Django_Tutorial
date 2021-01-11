<template>
    <div>
    </div>
</template>

<script>
import api from '@/axios-api.js'

export default {
    mounted () {
        api.logout().then(res => {
            this.$store.dispatch('clearProfile')
            this.$router.replace({
                path: '/'
            })
        })
    }
}
</script>

<style scoped>
</style>