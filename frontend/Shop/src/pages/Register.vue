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
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 90px);
    background: #f5f5f5;
}

.auth-card {
    background: white;
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    width: 100%;
    max-width: 400px;
    box-sizing: border-box;
}

.auth-card h2 {
    margin-top: 0;
    margin-bottom: 25px;
    text-align: center;
    font-size: 32px;
    color: #212529;
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
    font-size: 15px;
    color: #333;
}

.form-input {
    padding: 12px 14px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 15px;
    background: #fafafa;
    outline: none;
    transition: border-color 0.2s;
}

.form-input:focus {
    border-color: #212529;
}

.auth-button {
    margin-top: 10px;
    padding: 12px;
    background: #212529;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.2s;
}

.auth-button:hover {
    background: #343a40;
}

.auth-links {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.link {
    color: #212529;
    text-decoration: none;
    font-size: 14px;
}

.link:hover {
    text-decoration: underline;
}

.error {
    color: #dc3545;
    margin-bottom: 15px;
    text-align: center;
    font-size: 14px;
}
</style>