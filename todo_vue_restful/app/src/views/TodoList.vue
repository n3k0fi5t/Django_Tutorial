<template>
    <div>
        <Row type="flex" :gutter="18">
            <Col :span="18">
                <Panel shadow>
                    <div slot="title">My Todo list</div>
                    <div v-if="total > 0">
                        <div v-for="(item, idx) in todolist" :key="item.id">
                            <Card v-if="edit.visible && edit.idx === idx" class="item-top">
                                <Form ref="formEdit" :model="formData" :rules="ruleEdit">
                                    <FormItem prop="title">
                                        <Input type="text" v-model="formData.username">
                                        <Icon type="ios-person-outline" slot="prepend"></Icon>
                                        {{item.title}}
                                        </Input>
                                    </FormItem>
                                    <FormItem prop="context">
                                        <Input type="text" v-model="formData.context" size="large">
                                        <Icon type="ios-key" slot="prepend"></Icon>
                                        </Input>
                                    </FormItem>
                                </Form>
                            </Card>
                            <Card v-else class="item-top">
                                    <div slot="title" class="item-title">{{item.title}}</div>
                                    <div slot="extra">{{item.is_finished}} {{item.id}}</div>
                                    <div class="item-body">
                                        <Col span="2">
                                            <Button v-if="!item.is_finished" shape="circle" icon="ios-circle-outline" @click="handleFinish(idx)"></Button>
                                            <Icon v-else type="ios-checkmark-circle" size="36"></Icon>
                                        </Col>
                                        <Col span="20">
                                            <span>{{item.content}}</span>
                                        </Col>
                                        <Col span="2">
                                            <Button type="primary" shape="circle" class="edit-btn" @click="handleEdit(idx)">
                                                Edit
                                            </Button>
                                        </Col>
                                    </div>
                                </span>
                            </Card>
                        </div>
                    </div>
                    <div v-else>
                        <Card style="text-align: center;">
                            No data
                        </Card>
                    </div>
                </Panel>
                <Pagination :total="total"
                            :page-size="limit"
                            @on-change="pushRouter"
                            :current.sync="query.page"></Pagination>
            </Col>
            <Col :span="6">
                <Panel shadow>
                    <div slot="title">Quick add</div>
                </Panel>
            </Col>
        </Row>
    </div>
</template>

<script>
import api from '@/axios-api.js'
import Panel from '@/components/Panel.vue'
import Navbar from '../components/Navbar.vue'
import Pagination from '../components/Pagination.vue'
import formMixin from '@/components/form.js'
export default {
    data () {
        return {
            limit: 3,
            total: 0,
            todolist: [],
            todo: [],
            query: {
                page: 1
            },
            edit: {
                visible: false,
                idx: 0
            },
            formData: {
                title: '',
                context: '',
                is_finished: false
            },
            ruleEdit: {
                title: [
                    {required: true, trigger: 'blur', max: 50},
                ],
                context: [
                    {required: false, trigger: 'blur'}
                ],
                is_finished: [
                    {required: true, type: 'boolean'}
                ]
            }
        }
    },
    mixins: [formMixin],
    components: {
        Panel,
        Pagination
    },
    mounted () {
        this.init()
    },
    methods: {
        init () {
            let query = this.$route.query
            this.query.page = parseInt(query.page) || 1
            if (this.query.page < 1) {
                this.query.page = 1
            }
            this.getTodoList(this.query)
        },
        getTodoList ({page = 1}) {
            api.getTodoList((page-1)*this.limit, this.limit)
            .then(res => {
                this.todolist = res.data.data.results
                this.total = res.data.data.total
                this.todolist.forEach(function(item) {
                    console.log(item)
                })
            }, err => {
                console.log(err)
            })
        },
        pushRouter () {
            this.$router.push({
                name: 'todo-list',
                query: this.query
            })
        },
        handleFinish (idx) {
            let item = this.todolist[idx] || {}
            api.updateItem({item_id: item.id}, {is_finished: true}).then(res => {
                this.todolist[idx] = res.data.data
                this.init()
            }, err => {
                console.log(err)
            })
        },
        handleEdit (idx) {
            this.edit.idx = idx
            this.edit.visible = true
        }
    },
    watch: {
        $route (newVal, oldVal) {
            if (newVal !== oldVal) {
                this.init()
            }
        }
    }

}
</script>

<style scoped>
    .item-top {
        margin-top: 1%;
    }
    .item-title {
        font-size: 18px;
        font-weight: bold;
    }
    .item-body {
        margin-bottom: 1px;
        font-size: 16px;
        overflow: auto;
    }
    .edit-btn {
        margin-left: 2%;
        margin-right: 2%;
        float: right;
    }
    .page {
        margin: 20px;
        float: right;
    }
    .checkmark {
        margin-left: 1%;
        margin-right: 1%;
        float: left;
    }

</style>>