<script setup>
import { ref } from 'vue';

const admin = ref(
    JSON.parse(localStorage.getItem('admin')) || null
);
const user = ref(
    JSON.parse(localStorage.getItem('user')) || null
);

const data = JSON.parse(localStorage.getItem('user'));
const userId = data ? data.user_id : null;

// немног передалал логаут
function handleLogout() {
    localStorage.removeItem('admin');
    localStorage.removeItem('user');
    window.location.href = '/';
}
</script>

<template>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <img src="../../public/brand.png" class="logo" />

            <div>
                <router-link v-if="!admin && !user" to="/login" class="login-link">
                    Login
                </router-link>
                <router-link v-if="user" :to="`/user/profile/${userId}`" class="login-link">
                    Profile
                </router-link>
                <router-link v-if="admin" to="/admin/categories" class="login-link">
                    Categories
                </router-link>
                <button class="logout-button" 
                        v-if="admin || user" 
                        type="button" 
                        @click="handleLogout"
                >
                    Logout
                </button>
            </div>
            
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    width: 100%;
    height: 90px;
    padding: 5px 20px;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
}

.logo {
    height: 80px;
    width: auto;
}

.login-link, .logout-button {
    color: white;
    text-decoration: none;
    font-size: 20px;
    margin-right: 15px;
}

.login-link:hover {
    color: #adb5bd;
}

.logout-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
}

.logout-button:hover {
    color: #adb5bd;
}
</style>