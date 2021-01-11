import Vue from 'vue'
export default {
    methods: {
        validateForm (formName) {
            return new Promise((resolve, reject) => {
                this.$refs[formName].validate(valid => {
                    if (!valid) {
                        Vue.prototype.$error('please validate the error fields')
                        reject()
                    } else {
                        resolve()
                    }
                })
            })
        },
        cleanFrom (formName) {
            this.$refs[formName].resetFields();
        }
    }
}