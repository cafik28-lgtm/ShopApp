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
        let response = await loginAdmin(email.value, password.value); 
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('admin', JSON.stringify({
                ...data,
                email: email.value,
                password: password.value
            }));
            console.log('Admin logged in:', data);
            window.location.href = '/';
            return;
        } 

        response = await loginUser(email.value, password.value);
        if (response.ok) { 
            const data = await response.json();
            localStorage.setItem(
                'user',
                JSON.stringify({
                    ...data,
                    password: password.value
                })
            );
            console.log('User logged in:', data);
            window.location.href = '/';
            return;
        } 

        const data = await response.json();
        error.value = data.detail || 'Помилка входу';
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
    --bg-main: #FFFFFF;
    --text-main: #1F2937;
    --text-muted: #6B7280;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --border-light: #E5E7EB;

    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--bg-main);
    font-family: 'Inter', 'Montserrat', sans-serif;
    padding: 20px;
    box-sizing: border-box;
}

.login-card {
    width: 100%;
    max-width: 420px;
    padding: 40px;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
    box-sizing: border-box;
}

.login-card h1 {
    text-align: center;
    margin: 0 0 30px;
    color: var(--text-main);
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.input-group {
    margin-bottom: 20px;
}

.input-group label {
    display: block;
    margin-bottom: 8px;
    color: var(--text-main);
    font-weight: 500;
    font-size: 14px;
}

.input-group input {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    box-sizing: border-box;
    font-size: 15px;
    background: #F9FAFB;
    color: var(--text-main);
    outline: none;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.input-group input:focus {
    border-color: var(--accent-primary);
    background: #FFFFFF;
}

.login-button {
    width: 100%;
    padding: 14px;
    margin-top: 10px;
    border: none;
    border-radius: 10px;
    background: var(--accent-primary);
    color: white;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    transition: background 0.2s ease, transform 0.1s ease;
}

.login-button:hover {
    background: var(--accent-hover);
}

.login-button:active {
    transform: scale(0.99);
}

.links {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

.back-link {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: color 0.2s ease;
}

.back-link:hover {
    color: var(--text-main);
    text-decoration: underline;
}

.error {
    margin-top: 20px;
    text-align: center;
    color: var(--accent-danger);
    background: #FEF2F2;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #FCA5A5;
    font-size: 14px;
    font-weight: 500;
}
</style>