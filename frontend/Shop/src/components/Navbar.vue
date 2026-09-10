<script setup>
import { ref } from 'vue';

const admin = ref(
    JSON.parse(localStorage.getItem('admin')) || null
);
const user = ref(
    JSON.parse(localStorage.getItem('user')) || null
);

console.log(`${admin}, ${user}`);

async function logOut() {
    localStorage.removeItem('user');
    localStorage.removeItem('admin');

    window.location.reload();
}

</script>

<template>
    <nav class="navbar navbar-dark bg-dark mb-4">
        <div class="container">
            <img src="../../public/brand.png" class="logo" />

            <router-link v-if="!admin && !user" to="/login" class="login-link">
                Login
            </router-link>
            <button class="logout-button" 
                    v-if="admin || user" 
                    type="submit" 
                    @click="logOut"
            >
                LogOut
            </button>
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    width: 100%;
    padding: 5px 20px;
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
}
.logout-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
}
</style>