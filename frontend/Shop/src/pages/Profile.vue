<script setup>
import { onMounted, ref } from 'vue';
import { getUser, uploadAvatar, updateUser, deleteUser } from '../services/user_api';
import { useRoute, useRouter } from 'vue-router';
import { getProducts } from '../services/product_api';
import { getFavorites } from '../services/favorites_api';

const route = useRoute();
const router = useRouter();
const products = ref([]);

const email = ref('');
const first_name = ref('');
const last_name = ref('');
const phone = ref('');
const avatar = ref('');
const avatarFile = ref(null);
const city = ref('');
const country = ref('');
const isOwnProfile = ref(false);

const favoriteProducts = ref([]);

const admin = JSON.parse(localStorage.getItem('admin'));
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

            first_name.value = data.first_name;
            last_name.value = data.last_name;
            email.value = data.email;
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

async function fetchSellerProducts() {
    try {
        const response = await getProducts();

        if (response.ok) {
            const data = await response.json();

            products.value = data.filter(
                product => 
                product.seller_id == route.params.userId
            );
        } else {
            const data = await response.json();
            error.value = data.detail || 'Failed to load products';
        }
    } catch (err) {
        error.value = 'Connection error';
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

async function handleUpdate() {
    error.value = '';
    try {
        const userId = route.params.userId;
        const response = await updateUser(userId, {
            first_name: first_name.value,
            last_name: last_name.value,
            phone: phone.value,
            country: country.value,
            city: city.value
        });

        if (response.ok) {
            const data = await response.json();

            first_name.value = data.first_name;
            last_name.value = data.last_name;
            phone.value = data.phone;
            country.value = data.country;
            city.value = data.city;
        }
        else {
            const data = await response.json();
            error.value = data.detail || 'Помилка оновлення профілю';
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function handleDeleteUserByAdmin() {
    if (!confirm('Ви впевнені, що хочете видалити цього користувача?')) return;
    error.value = '';
    try {
        const userId = route.params.userId;
        const response = await deleteUser(userId);
        
        if (response.ok) {
            router.push('/');
        } else {
            const data = await response.json().catch(() => ({}));
            error.value = data.detail || 'Помилка видалення користувача';
        }
    } catch (err) {
        router.push('/');
    }
}

async function getFavoritesProducts() {
    if (!isOwnProfile.value) return;

    try {
        const response = await getFavorites();

        if (response.ok) {
            const data = await response.json();
            favoriteProducts.value = data.items;
        } else {
            const data = await response.json();
            error.value = data.detail || 'Error getting favorite products';
        }
    } catch (err) {
        error.value = 'Server connection error';
    }
}

onMounted(getProfile);
onMounted(fetchSellerProducts);
onMounted(getFavoritesProducts);
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

                            <span class="value">
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

                    <div>
                        <button
                            v-if="isOwnProfile"
                            class="save-button"
                            type="submit"
                            style="margin-right: 15px;"
                        >
                            Save changes
                        </button>

                        <button
                            v-if="admin"
                            class="save-button"
                            type="button"
                            style="background: #dc3545;"
                            @click="handleDeleteUserByAdmin"
                        >
                            Delete User (Admin)
                        </button>
                    </div>
                   

                    <p v-if="error" class="error">
                        {{ error }}
                    </p>
                </div>
            </form>
            <div class="seller-products">
                <h2>Seller products</h2>

                <div v-if="products.length" class="products-grid">
                    <div
                        v-for="p in products"
                        :key="p.id"
                        class="product-card"
                        :class="p.in_stock ? 'in-stock' : 'out-of-stock'"
                    >
                        <div class="product-image">
                            <img
                                v-if="p.photo"
                                :src="`http://127.0.0.1:8000/${p.photo}`"
                                alt="product"
                            />
                            <div v-else class="no-photo">
                                No photo
                            </div>
                        </div>

                        <div class="product-info">
                            <h3>{{ p.name }}</h3>

                            <p class="product-price">
                                {{ p.cost }}$
                            </p>

                            <router-link
                                :to="`/products/${p.id}`"
                                class="details-button"
                            >
                                View details
                            </router-link>
                        </div>
                    </div>
                </div>

                <p v-else class="no-products">
                    This user has no products.
                </p>
            </div>
            <div v-if="isOwnProfile" class="seller-products">
                <h2>Favorites</h2>

                <div v-if="favoriteProducts.length" class="products-grid">
                    <div
                        v-for="p in favoriteProducts"
                        :key="p.product_id"
                        class="product-card"
                    >
                        <div class="product-image">
                            <img
                                v-if="p.photo"
                                :src="`http://127.0.0.1:8000/${p.photo}`"
                                alt="product"
                            />
                            <div v-else class="no-photo">
                                No photo
                            </div>
                        </div>

                        <div class="product-info">
                            <h3>{{ p.name }}</h3>

                            <p class="product-price">
                                {{ p.price }}$
                            </p>

                            <router-link
                                :to="`/products/${p.product_id}`"
                                class="details-button"
                            >
                                View details
                            </router-link>
                        </div>
                    </div>
                </div>

                <p v-else class="no-products">
                    You have no favorite products.
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.profile-page {
    --bg-main: #FFFFFF;
    --text-main: #1F2937;
    --text-muted: #6B7280;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --border-light: #E5E7EB;

    min-height: calc(100vh - 90px);
    padding: 40px;
    background: var(--bg-main);
    box-sizing: border-box;
    font-family: 'Inter', 'Montserrat', sans-serif;
}

.profile-card {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 40px;
    padding: 40px;
    box-sizing: border-box;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
}

.profile-left {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.avatar-wrapper {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    overflow: hidden;
    background: #F9FAFB;
    border: 1px solid var(--border-light);
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

.avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F9FAFB;
    color: var(--text-muted);
    font-size: 15px;
}

.upload-button {
    margin-top: 20px;
    padding: 10px 20px;
    border-radius: 10px;
    background: #F9FAFB;
    border: 1px solid var(--border-light);
    color: var(--text-main);
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.2s ease;
    text-align: center;
}

.upload-button:hover {
    background: var(--border-light);
    transform: translateY(-1px);
}

.upload-button input {
    display: none;
}

.profile-right {
    display: flex;
    flex-direction: column;
}

.profile-right h1 {
    margin: 0 0 25px;
    font-size: 28px;
    color: var(--text-main);
    font-weight: 700;
    letter-spacing: -0.5px;
}

.profile-label {
    margin: 0 0 8px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: var(--text-muted);
}

.profile-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 25px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.label {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-muted);
}

.value,
.info-item input {
    width: 100%;
    min-height: 44px;
    padding: 10px 16px;
    box-sizing: border-box;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    font-size: 15px;
    color: var(--text-main);
    background: #F9FAFB;
    outline: none;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.value {
    display: flex;
    align-items: center;
}

.info-item input:focus {
    border-color: var(--accent-primary);
    background: #FFFFFF;
}

.save-button {
    padding: 12px 24px;
    border: none;
    border-radius: 10px;
    background: var(--accent-primary);
    color: white;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.1s ease;
}

.save-button:hover {
    background: var(--accent-hover);
}

.save-button:active {
    transform: scale(0.99);
}

.error {
    margin-top: 15px;
    color: var(--accent-danger);
    background: #FEF2F2;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #FCA5A5;
    font-size: 14px;
    font-weight: 500;
}

.seller-products {
    grid-column: 1 / -1;
    margin-top: 40px;
    width: 100%;
    border-top: 1px solid var(--border-light);
    padding-top: 30px;
}

.seller-products h2 {
    margin: 0 0 20px;
    color: var(--text-main);
    font-size: 22px;
    font-weight: 700;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.product-card {
    overflow: hidden;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-radius: 16px;
    box-sizing: border-box;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
}

.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    border-color: transparent;
}

.product-card.in-stock {
    border-color: var(--border-light);
}

.product-card.out-of-stock {
    border-color: #FCA5A5;
    background: #FEF2F2;
}

.product-image {
    width: 100%;
    height: 180px;
    background: #F9FAFB;
    position: relative;
    overflow: hidden;
}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
    transform: scale(1.03);
}

.no-photo {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--text-muted);
    font-size: 14px;
}

.product-info {
    padding: 16px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.product-info h3 {
    margin: 0 0 6px;
    font-size: 17px;
    color: var(--text-main);
    font-weight: 600;
}

.product-price {
    margin-bottom: 15px;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-main);
}

.details-button {
    display: block;
    width: 100%;
    padding: 10px;
    border-radius: 10px;
    background: var(--text-main);
    color: white;
    text-align: center;
    text-decoration: none;
    box-sizing: border-box;
    font-size: 14px;
    font-weight: 600;
    margin-top: auto;
    transition: background 0.2s ease;
}

.details-button:hover {
    background: var(--accent-primary);
}

.no-products {
    color: var(--text-muted);
    font-style: italic;
    margin: 0;
}

@media (max-width: 900px) {
    .products-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .products-grid {
        grid-template-columns: 1fr;
    }
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

    .profile-left {
        margin-bottom: 20px;
    }
}
</style>