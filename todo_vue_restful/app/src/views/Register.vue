<template>
    <div>
        <!-- add 'ref="ref_value"' to locate the element by this.$refs[ref_value] -->
        <Form ref="formRegister" :rules="ruleRegister" :model="formData">
        <FormItem prop="username">
            <Input type="text" v-model="formData.username" placeholder="username" size="large" @on-enter="handleRegister">
            <Icon type="ios-person-outline" slot="prepend"></Icon>
            </Input>
        </FormItem>
        <FormItem prop="email">
            <Input v-model="formData.email" placeholder="email Address" size="large" @on-enter="handleRegister">
            <Icon type="ios-mail" slot="prepend"></Icon>
            </Input>
        </FormItem>
        <FormItem prop="password">
            <Input type="password" v-model="formData.password" placeholder="password" size="large" @on-enter="handleRegister">
            <Icon type="ios-key" slot="prepend"></Icon>
            </Input>
        </FormItem>
        <FormItem prop="passwordAgain">
            <Input type="password" v-model="formData.passwordAgain" placeholder="password Again" size="large" @on-enter="handleRegister">
            <Icon type="ios-key" slot="prepend"></Icon>
            </Input>
        </FormItem>
        </Form>
        <div class="footer">
            <Button
                type="primary"
                @click="handleRegister"
                :loading="loading"
                class="button" long>
                Register
            </Button>
            <Button
                type="default"
                @click="switch_modal('login')"
                class="button" long>
                Already registed? Login now!
            </Button>
        </div>
    </div>
</template>

<script>
import {mapActions} from 'vuex'
import formMixin from '@/components/form.js'
import api from '@/axios-api.js'
export default {
    mixins: [formMixin],
    data () {
        const CheckUsername = (rule, value, callback) => {
            api.checkUsernameOrEmail(value, undefined).then(res => {
                if (res.data.data.username === true) {
                    callback(new Error("username already exist"))
                } else {
                    callback()
                }
            })
        }
        const CheckEmail = (rule, value, callback) => {
            api.checkUsernameOrEmail(undefined, value).then(res => {
                if (res.data.data.email === true) {
                    callback(new Error("email already exist"))
                } else {
                    callback()
                }
            })
        }
        const CheckAgainPassword = (rule, value, callback) => {
            if (value !== this.formData.password) {
                callback(new Error("password does not match"))
            }
            callback()
        }
        const CheckPassword = (rule, value, callback) => {
            if (value !== '') {
                this.$refs.formRegister.validateField('passwordAgain')
            }
            callback()
        }
        return {
            loading: false,
            formData: {
                username: '',
                password: '',
                passwordAgain: '',
                email: ''
            },
            ruleRegister: {
                username: [
                    {required: true, trigger: 'blur'},
                    {validator: CheckUsername, trigger: 'blur'}
                ],
                email: [
                    {required: true, trigger: 'blur', type: 'email'},
                    {validator: CheckEmail, trigger: 'blur'}
                ],
                password: [
                    {required: true, trigger: 'blur', min: 6, max: 20},
                    {validator: CheckPassword, trigger: 'blur'}
                ],
                passwordAgain: [
                    {required: true, trigger: 'change', validator: CheckAgainPassword}
                ]
            }
        }
    },
    methods: {
        ...mapActions(['getProfile', 'changeModalStatus']),
        switch_modal (mode) {
            this.changeModalStatus({mode:mode})
        },
        handleRegister () {
            this.validateForm('formRegister').then((valid) => {
                this.loading = true
                // let formData = Object.assgin({}, this.formData)
                let formData = JSON.parse(JSON.stringify(this.formData))
                delete formData['passwordAgain']

                api.register(formData)
                .then(res => {
                    this.loading = false
                    this.$success("register sucessfully")
                    this.changeModalStatus({visible: false})
                    this.cleanFrom('formRegister')
                }, err => {
                    this.loading = false
                    this.$error("register failed")
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