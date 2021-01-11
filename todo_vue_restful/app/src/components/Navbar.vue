<template>
  <div id="header">
    <Menu mode="horizontal" theme="light" @on-select="handleRoute" :active-name="activeMenu">
      <div class="logo"><span>Online Memo</span></div>
      <Menu-item name="/">
        <Icon type="ios-home"></Icon>
        Home
      </Menu-item>
      <Menu-item name="/todo-list">
        <Icon type="ios-paper"></Icon>
        Todo-list
      </Menu-item>
      <template v-if="!isAuthenticated">
        <div class="btn-menu">
          <Button type="default"
                  shape="circle"
                  @click="handleBtnClick('login')">Login
          </Button>
          <Button type="default"
                  shape="circle"
                  @click="handleBtnClick('register')"
                  style="margin-left: 10px;">Register
          </Button>
        </div>
      </template>
      <template v-else>
        <Dropdown class="drop-menu" @on-click="handleRoute" placement="bottom" trigger="click">
          <Button type="text" class="drop-menu-title">{{ user.username }}
            <Icon type="ios-arrow-down"></Icon>
          </Button>
          <Dropdown-menu slot="list">
            <Dropdown-item divided name="/logout">logout</Dropdown-item>
          </Dropdown-menu>
        </Dropdown>
      </template>
    </Menu>
    <Modal v-model="modalVisible" width="400">
      <div slot="header" style="font-size: 18px; font-weight: 600">Welcome to {{website.title}}</div>
      <component :is="modalStatus.mode"></component>
      <div slot="footer" style="display: none;"></div>
    </Modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import login from '@/views/Login.vue'
import register from '@/views/Register.vue'
export default {
    name: 'Navbar',
    components: {
      login,
      register
    },
    mounted () {
      // make sure we could always get csrf token
      this.getProfile()
    },
    computed: {
        ...mapGetters(['modalStatus', 'isAuthenticated', 'website', 'user']),
        activeMenu () {
          // correspond to navigation bar active item
          return '/' + this.$route.path.split('/')[1]
        },
        modalVisible: {
          set (value) {
            this.changeModalStatus({
              visible: value
            })
          },
          get () {
            return this.modalStatus.visible
          }
        }
    },
    methods: {
      ...mapActions(['changeModalStatus', 'getProfile']),
      handleBtnClick (mode) {
        this.changeModalStatus({
          visible: true,
          mode: mode
        })
      },
      handleRoute (route) {
        console.log(route)
        if (route && this.$route.path !== route) {
          this.$router.push(route)
        }
      }
    }
}
</script>

<style lang="less" scoped>
  #header {
    min-width: 300px;
    position: fixed;
    top: 0;
    left: 0;
    height: 60px;
    width: 100%;
    z-index: 1000;
    background-color: #fff;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
    .logo {
      margin-left: 2%;
      margin-right: 2%;
      font-size: 20px;
      float: left;
      line-height: 60px;
    }
    .drop-menu {
      float: right;
      margin-right: 30px;
      position: absolute;
      right: 10px;
      &-title {
        font-size: 18px;
      }
    }
    .btn-menu {
      font-size: 16px;
      float: right;
      margin-right: 10px;
    }
  }
</style>