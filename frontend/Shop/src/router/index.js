// npm install vue-router - для этого файла надо скачать
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../pages/Login.vue';
import Register from '../pages/Register.vue';
import Profile from '../pages/Profile.vue';
import AdminCategories from '../components/AdminCategories.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/login',
            component: Login
        },
        {
            path: '/user/register',
            component: Register
        },
        {
            path: '/user/profile/:userId',
            component: Profile 
        },
        {
            path: '/admin/categories',
            component: AdminCategories
        }
    ]
});

export default router;