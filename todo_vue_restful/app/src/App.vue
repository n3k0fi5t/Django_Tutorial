<template>
  <div>
      <NavBar></NavBar>
      <div class="content-app">
        <router-view/>
      </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import NavBar from './components/Navbar.vue'
export default {
  name: 'App',
  components: {
    NavBar,
  },
  methods: {
    ...mapActions(['changeDomTitle'])
  },
  watch : {
    $route (to) {
      this.changeDomTitle()
    }
  }
}
</script>

<style lang="less">
  * {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }
  @media screen and (min-width: 1200px) {
    .content-app {
      margin-top: 80px;
      padding: 0 2%;
    }
  }
  @media screen and (min-width: 800px) {
    .content-app {
      margin-top: 60px;
      padding: 0 2%;
    }
  }
</style>
