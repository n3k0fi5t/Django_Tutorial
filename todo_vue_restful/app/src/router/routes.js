import { 
    Home,
    Logout,
    TodoList
} from '../views'

export default [
    {
        path: '/',
        name: 'home',
        component: Home,
        meta: {
            title: ''
        }
    },
    {
        path: '/todo-list',
        name: 'todo-list',
        component: TodoList,
        meta: {
            title: 'Todo-list',
            requiresAuth: true
        }
    },
    {
        path: '/logout',
        name: 'logout',
        component: Logout
    }
]