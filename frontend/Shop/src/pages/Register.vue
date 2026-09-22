<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { createUser } from '../services/user_api';

const email = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

async function handleRegister() {
    error.value = '';
    try {
        const response = await createUser(
            email.value,
            password.value,
        );
        if (response.ok) {
            const data = await response.json();
            console.log('User registered:', data);
            router.push('/login');
            return;
        } else {
            const data = await response.json();
            error.value = data.detail;
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <h2>Register</h2>

            <p v-if="error" class="error">{{ error }}</p>

            <form @submit.prevent="handleRegister" class="auth-form">
                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" v-model="email" required class="form-input" />
                </div>

                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" v-model="password" required class="form-input" />
                </div>

                <button type="submit" class="auth-button">Register</button>
            </form>

            <div class="auth-links">
                <router-link to="/login" class="link">Back to login</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
.auth-container {
    --bg-main: #FFFFFF;
    --text-main: #1F2937;
    --text-muted: #6B7280;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --border-light: #E5E7EB;

    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 90px);
    background: var(--bg-main);
    font-family: 'Inter', 'Montserrat', sans-serif;
    padding: 20px;
    box-sizing: border-box;
}

.auth-card {
    background: #FFFFFF;
    padding: 40px;
    border: 1px solid var(--border-light);
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
    width: 100%;
    max-width: 420px;
    box-sizing: border-box;
}

.auth-card h2 {
    margin-top: 0;
    margin-bottom: 30px;
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    color: var(--text-main);
    letter-spacing: -0.5px;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-main);
}

.form-input {
    padding: 12px 16px;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    font-size: 15px;
    background: #F9FAFB;
    color: var(--text-main);
    outline: none;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.form-input:focus {
    border-color: var(--accent-primary);
    background: #FFFFFF;
}

.auth-button {
    margin-top: 10px;
    padding: 14px;
    background: var(--accent-primary);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.1s ease;
}

.auth-button:hover {
    background: var(--accent-hover);
}

.auth-button:active {
    transform: scale(0.99);
}

.auth-links {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.link {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: color 0.2s ease;
}

.link:hover {
    color: var(--text-main);
    text-decoration: underline;
}

.error {
    color: var(--accent-danger);
    background: #FEF2F2;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #FCA5A5;
    margin-bottom: 20px;
    text-align: center;
    font-size: 14px;
    font-weight: 500;
}
</style>