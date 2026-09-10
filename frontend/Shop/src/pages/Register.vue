<script setup>
import { ref } from 'vue';
import { createUser } from '../services/user_api';
import { useRouter } from 'vue-router';

const router = useRouter();

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const phone = ref('');
const country = ref('');
const city = ref('');

const error = ref('');

async function handleRegister() {
    error.value = '';
    try {
        const response = await createUser(
            firstName.value,
            lastName.value,
            email.value,
            password.value,
            phone.value,
            country.value,
            city.value
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
    <div class="register-page">
        <div class="register-card">
            <h1>Register</h1>

            <form @submit.prevent="handleRegister">

                <div class="input-row">
                    <div class="input-group">
                        <label>First name:</label>
                        <input
                            type="text"
                            v-model="firstName"
                            required
                        />
                    </div>

                    <div class="input-group">
                        <label>Last name:</label>
                        <input
                            type="text"
                            v-model="lastName"
                            required
                        />
                    </div>
                </div>

                <div class="input-row">
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
                </div>

                <div class="input-row">
                    <div class="input-group">
                        <label>Phone:</label>
                        <input
                            type="tel"
                            v-model="phone"
                        />
                    </div>

                    <div class="input-group">
                        <label>Country:</label>
                        <input
                            type="text"
                            v-model="country"
                        />
                    </div>
                </div>

                <div class="input-group">
                    <label>City:</label>
                    <input
                        type="text"
                        v-model="city"
                    />
                </div>

                <button type="submit" class="register-button">
                    Register
                </button>

                <router-link to="/login" class="back-link">
                    Back to login
                </router-link>
            </form>

            <p v-if="error" class="error">
                {{ error }}
            </p>
        </div>
    </div>
</template>

<style scoped>
.register-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f5f5f5;
}

.register-card {
    width: 600px;
    padding: 35px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.register-card h1 {
    text-align: center;
    margin-bottom: 30px;
}

.input-row {
    display: flex;
    gap: 20px;
}

.input-group {
    flex: 1;
    margin-bottom: 18px;
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

.register-button {
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

.register-button:hover {
    background: #343a40;
}

.back-link {
    display: block;
    text-align: center;
    margin-top: 15px;
    color: #212529;
    text-decoration: none;
}

.back-link:hover {
    text-decoration: underline;
}

.error {
    margin-top: 15px;
    text-align: center;
    color: #dc3545;
}
</style>