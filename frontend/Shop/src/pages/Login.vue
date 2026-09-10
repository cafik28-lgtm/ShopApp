<script setup> 
import { ref } from 'vue';
import { loginAdmin } from '../services/admin_api';
import { loginUser } from '../services/user_api';

const email = ref('');
const password = ref('');
const error = ref('');
async function handleLogin() { 
    error.value = '';
    try {
        let response = await loginAdmin( email.value, password.value ); 
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('admin', JSON.stringify(data));
            console.log('Admin logged in:', data);
            window.location.href = '/';
            return;
        } 
        response = await loginUser( email.value, password.value );
        if (response.ok) { 
            const data = await response.json();
            localStorage.setItem('user', JSON.stringify(data));
            console.log('User logged in:', data);
            window.location.href = '/';
            return;
        } 
        const data = await response.json();
        error.value = data.detail;
        } catch (err) {
             error.value = 'Помилка підключення до сервера';
        } 
    } 
</script>

<template>
    <div class="login-page">
        <div class="login-card">
            <h1>Login</h1>

            <form @submit.prevent="handleLogin">
                <div class="input-group">
                    <label>Email:</label>
                    <input
                        type="email"
                        v-model="email"
                        required
                    />
                </div>

                <div class="input-group">
                    <label>Password:</label>
                    <input
                        type="password"
                        v-model="password"
                        required
                    />
                </div>

                <button type="submit" class="login-button">
                    Sign in
                </button>

                <div class="links"> 
                    <router-link to="/" class="back-link">
                        Back
                    </router-link>
                    <router-link to="/user/register" class="back-link">
                        Register
                    </router-link>
                </div>
                
            </form>

            <p v-if="error" class="error">
                {{ error }}
            </p>
        </div>
    </div>
</template>

<style scoped>
.login-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f5f5f5;
}

.login-card {
    width: 400px;
    padding: 35px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.login-card h1 {
    text-align: center;
    margin-bottom: 30px;
}

.input-group {
    margin-bottom: 20px;
}

.input-group label {
    display: block;
    margin-bottom: 7px;
}

.input-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
}

.login-button {
    width: 100%;
    padding: 11px;
    margin-top: 5px;
    border: none;
    border-radius: 8px;
    background: #212529;
    color: white;
    cursor: pointer;
    font-size: 16px;
}

.login-button:hover {
    background: #343a40;
}

.links {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
}

.back-link {
    color: #212529;
    text-decoration: none;
    margin-right: 10px;
}

.error {
    margin-top: 15px;
    text-align: center;
    color: #dc3545;
}
</style>
