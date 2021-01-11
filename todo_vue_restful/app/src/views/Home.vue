<template>
    <div>
    </div>
</template>

<script>
export default {
    name: 'Home',
    data () {
        return {
            modal1: false
        }
    },
    methods: {
        ok () {
            this.$info('点击了确定');
        },
        cancel () {
            this.$info('点击了取消');
        }
    }
}
</script>

<style scoped>

</style>