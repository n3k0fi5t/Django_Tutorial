<template>
    <div>
        <div class="container text-dark">
            <div class="row justify-content-md-center">
                <div class="col-md-5 p-3 login justify-content-md-center">
                    <h1 class="h3 mb-3 font-weight-normal text-center">Please sign in</h1>
                    <p v-if="incorrectAuth">Incorrect username or password, please try again</p>
                    <form v-on:submit.prevent="login">
                        <div class="form-group">
                            <input type="text" name="username" id="user" v-model="username" class="form-control" placeholder="Username">
                        </div>
                        <div class="form-group">
                            <input type="password" name="password" id="pass" v-model="password" class="form-control" placeholder="Password">
                        </div>
                        <button type="submit" class="btn btn-lg btn-primary btn-block">Login</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from '../axios-api'
export default {
    name: 'login',
    data () {
        return {
            username: '',
            password: '',
            incorrectAuth: false
        }
    },
    methods: {
        login () {
            // this.$store.dispatch('userLogin', {
            //     username: this.username,
            //     password: this.password
            // })
            // .then(() => {
            //     api.createPost({
            //         Authorization: `JWT ${this.$store.state.accessToken}`,
            //         'X-Requested-With': 'XMLHttpRequest'
            //     }, {
            //         title: 'title',
            //         content: 'content'
            //     }).then(() => {

            //     })

            //     this.$router.push({ name: 'posts' })
            // })
            // .catch(err => {
            //     console.log(err)
            //     this.incorrectAuth = true
            // })
            api.userLogin({
                username: this.username,
                password: this.password
            })
            .then(resp => {
                console.log(resp)
                this.$store.dispatch('login')
                this.$router.push({ name: 'posts'})
            })
            .catch(resp => {
                console.log(resp)
            })
        }
    },
}
</script>

<style scoped>
body {
    background-color: #f4f4f4;
}
    .login {
        background-color: #fff;
        margin-top: 10%;
    }
    input {
        padding: 25px 10px;
    }
</style>