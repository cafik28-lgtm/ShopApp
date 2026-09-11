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

console.log(`${admin}, ${user}`);

async function logOut() {
    localStorage.removeItem('user');
    localStorage.removeItem('admin');

    window.location.reload();
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
                <button class="logout-button" 
                        v-if="admin || user" 
                        type="submit" 
                        @click="logOut"
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
    margin-right: 10px;
}
.logout-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
}
</style>