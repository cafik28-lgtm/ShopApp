<script setup>
import { onMounted, ref } from 'vue';
import { getUser, uploadAvatar } from '../services/user_api';
import { useRoute } from 'vue-router';

const route = useRoute();

const email = ref('');
const first_name = ref('');
const last_name = ref('');
const phone = ref('');
const avatar = ref('');
const avatarFile = ref(null);
const city = ref('');
const country = ref('');
const isOwnProfile = ref(false);

const error = ref('');

async function getProfile() {
    try {
        const userId = route.params.userId;
        const currentUser = JSON.parse(localStorage.getItem('user'));

        isOwnProfile.value =
            currentUser && currentUser.user_id == userId;

        const response = await getUser(userId);

        if (response.ok) {
            const data = await response.json();

            email.value = data.email;
            first_name.value = data.first_name;
            last_name.value = data.last_name;
            phone.value = data.phone;
            avatar.value = data.avatar;
            city.value = data.city;
            country.value = data.country;
        } else {
            const data = await response.json();
            error.value = data.detail;
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function handleAvatarUpload(event) {
    const file = event.target.files[0];

    if (!file) {
        return;
    }

    avatarFile.value = file;

    try {
        const userId = route.params.userId;

        const response = await uploadAvatar(userId, file);

        if (response.ok) {
            const data = await response.json();

            avatar.value = data.avatar;
        } else {
            const data = await response.json();
            error.value = data.detail;
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

onMounted(getProfile);

</script>


<template>
    <div class="profile-page">
        <div class="profile-card">

            <div class="profile-left">
                <div class="avatar-wrapper">
                    <img
                        v-if="avatar"
                        :src="`http://127.0.0.1:8000/${avatar}`"
                        alt="avatar"
                        class="avatar"
                    />
                
                    <div v-else class="avatar avatar-placeholder">
                        No avatar
                    </div>
                </div>

                <label v-if="isOwnProfile" class="upload-button">
                    Change photo
                    <input
                        type="file"
                        accept="image/*"
                        @change="handleAvatarUpload"
                    />
                </label>
            </div>
            <form @submit.prevent="handleUpdate">
                <div class="profile-right">
                    <p class="profile-label">PROFILE</p>

                    <h1>
                        {{ first_name || 'User' }}
                        {{ last_name || '' }}
                    </h1>

                    <div class="profile-info">

                        <div class="info-item">
                            <span class="label">First name</span>

                            <input
                                v-if="isOwnProfile"
                                v-model="first_name"
                            />

                            <span v-else class="value">
                                {{ first_name || 'None' }}
                            </span>
                        </div>

                        <div class="info-item">
                            <span class="label">Last name</span>

                            <input
                                v-if="isOwnProfile"
                                v-model="last_name"
                            />

                            <span v-else class="value">
                                {{ last_name || 'None' }}
                            </span>
                        </div>

                        <div class="info-item">
                            <span class="label">Email</span>

                            <input
                                v-if="isOwnProfile"
                                v-model="email"
                                type="email"
                            />

                            <span v-else class="value">
                                {{ email || 'None' }}
                            </span>
                        </div>

                        <div class="info-item">
                            <span class="label">Phone</span>

                            <input
                                v-if="isOwnProfile"
                                v-model="phone"
                                type="tel"
                            />

                            <span v-else class="value">
                                {{ phone || 'None' }}
                            </span>
                        </div>

                        <div class="info-item">
                            <span class="label">Country</span>

                            <input
                                v-if="isOwnProfile"
                                v-model="country"
                            />

                            <span v-else class="value">
                                {{ country || 'None' }}
                            </span>
                        </div>

                        <div class="info-item">
                            <span class="label">City</span>

                            <input
                                v-if="isOwnProfile"
                                v-model="city"
                            />

                            <span v-else class="value">
                                {{ city || 'None' }}
                            </span>
                        </div>

                    </div>

                    <button
                        v-if="isOwnProfile"
                        class="save-button"
                        type="submit"
                    >
                        Save changes
                    </button>

                    <p v-if="error" class="error">
                        {{ error }}
                    </p>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.profile-page {
    min-height: calc(100vh - 90px);
    padding: 25px 40px;
    background: #f5f5f5;
    box-sizing: border-box;
}

.profile-card {
    width: 100%;
    max-width: 1100px;
    min-height: calc(100vh - 140px);
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 3fr;
    gap: 45px;
    padding: 40px;
    box-sizing: border-box;

    background: white;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
}

.profile-left {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 10px;
}

.avatar-wrapper {
    width: 220px;
    height: 220px;
}

.avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 20px;
}

.avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e6e6e6;
    color: #777;
}

.upload-button {
    margin-top: 15px;
    padding: 9px 18px;
    border-radius: 8px;
    background: #212529;
    color: white;
    cursor: pointer;
    font-size: 14px;
}

.upload-button input {
    display: none;
}

.profile-right h1 {
    margin: 0 0 30px;
    font-size: 34px;
}

.profile-label {
    margin: 0 0 5px;
    font-size: 12px;
    letter-spacing: 2px;
    color: #888;
}

.profile-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px 25px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.label {
    font-size: 13px;
    color: #777;
}

.value,
.info-item input {
    width: 100%;
    min-height: 42px;
    padding: 10px 12px;
    box-sizing: border-box;

    border: 1px solid #ddd;
    border-radius: 8px;

    font-size: 16px;
    color: #222;
    background: #fafafa;
}

.info-item input {
    outline: none;
}

.info-item input:focus {
    border-color: #212529;
    background: white;
}

.save-button {
    margin-top: 30px;
    padding: 11px 24px;
    border: none;
    border-radius: 8px;
    background: #212529;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

.error {
    margin-top: 20px;
    color: #dc3545;
}

@media (max-width: 800px) {
    .profile-page {
        padding: 20px;
    }

    .profile-card {
        grid-template-columns: 1fr;
        padding: 25px;
    }

    .profile-info {
        grid-template-columns: 1fr;
    }
}
</style>