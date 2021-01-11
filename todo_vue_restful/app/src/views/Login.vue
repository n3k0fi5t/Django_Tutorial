<template>
    <div>
        <Form ref="formLogin" :model="formData" :rules="ruleLogin">
            <FormItem prop="username">
                <Input type="text" v-model="formData.username" placeholder="Username" size="large" @on-enter="handleLogin">
                <Icon type="ios-person-outline" slot="prepend"></Icon>
                </Input>
            </FormItem>
            <FormItem prop="password">
                <Input type="password" v-model="formData.password" placeholder="Password" size="large" @on-enter="handleLogin">
                <Icon type="ios-key" slot="prepend"></Icon>
                </Input>
            </FormItem>
        </Form>
        <div class="footer">
            <Button
                type="primary"
                @click="handleLogin"
                :loading="loading"
                class="button" long>
                Login
            </Button>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import formMixin from '@/components/form.js'
import api from '@/axios-api.js'
export default {
    mixins: [formMixin],
    data () {
        return {
            loading: false,
            formData: {
                username: '',
                password: ''
            },
            ruleLogin: {
                username: [
                    {required: true, trigger: 'blur'},
                ],
                password: [
                    {required: true, trigger: 'change', min:6, max: 30}
                ]
            }
        }
    },
    computed: mapGetters(['redirect_path']),
    methods: {
        ...mapActions(['getProfile', 'changeModalStatus']),
        handleLogin () {
            this.validateForm('formLogin').then((valid) => {
                this.loading = true
                // let formData = Object.assgin({}, this.formData)
                let formData = JSON.parse(JSON.stringify(this.formData))

                api.login(formData)
                .then(res => {
                    this.loading = false
                    this.getProfile()
                    this.$success("Welcome back to OnlineMemo")
                    this.changeModalStatus({visible: false})
                    this.cleanFrom('formLogin')
                }, err => {
                    this.loading = false
                    this.$error("login failed")
                })
            })
        }
    }

}
</script>

<style scoped lang="less">
  .footer {
    overflow: auto;
    margin-top: 20px;
    margin-bottom: -15px;
    text-align: left;
    .button {
        margin: 0 0 15px 0;
        font-size: 14px;
    }
  }
</style>