<script setup>
import { ref, onMounted } from 'vue';
import { getFavorites, deleteFavorite } from '../services/favorites_api';
import { useRouter } from 'vue-router';

const favorites = ref([]);
const error = ref('');
const router = useRouter();

async function fetchFavs() {
    try {
        const response = await getFavorites();
        if (response.ok) {
            const data = await response.json();
            favorites.value = data.items;
        } else {
            favorites.value = [];
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function removeItem(productId) {
    try {
        const response = await deleteFavorite(productId);
        if (response.ok) {
            favorites.value = favorites.value.filter(item => item.product_id !== productId);
        }
    } catch (err) {
        console.error('Failed to remove favorite');
    }
}

onMounted(fetchFavs);
</script>

<template>
    <div class="favorites-page">
        <div class="header-fav">
            <h1>Моє обране</h1>
            <router-link to="/" class="back-btn">Назад до каталогу</router-link>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <div v-else-if="favorites.length === 0" class="empty-fav">
            <p>У вас поки немає обраних товарів.</p>
            <router-link to="/" class="details-button" style="display:inline-block; width:auto; padding:10px 20px;">Перейти до каталогу</router-link>
        </div>

        <div v-else class="products-grid">
            <div v-for="item in favorites" :key="item.product_id" class="product-card">
                <div class="product-image">
                    <img
                        v-if="item.photo"
                        :src="`http://127.0.0.1:8000/${item.photo}`"
                        alt="product"
                    />
                    <div v-else class="no-photo">No photo</div>
                    
                    <button class="favorite-btn" @click="removeItem(item.product_id)" title="Видалити">
                        ❌
                    </button>
                </div>

                <div class="product-info">
                    <h2>{{ item.name }} | {{ item.price }}$</h2>
                    <p class="description">{{ item.description || 'Немає опису' }}</p>

                    <router-link :to="`/products/${item.product_id}`" class="details-button">
                        View details
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.favorites-page {
    padding: 30px 40px;
    box-sizing: border-box;
    min-height: calc(100vh - 90px);
    background: #f5f5f5;
}

.header-fav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.header-fav h1 {
    margin: 0;
    color: #212529;
}

.back-btn {
    text-decoration: none;
    color: #212529;
    font-weight: 500;
    background: white;
    padding: 10px 18px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.empty-fav {
    text-align: center;
    padding: 50px;
    background: white;
    border-radius: 12px;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
}

.product-card {
    overflow: hidden;
    background: white;
    border: 3px solid #212529;
    border-radius: 12px;
    box-sizing: border-box;
}

.product-image {
    width: 100%;
    height: 230px;
    background: #f1f1f1;
    position: relative;
}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.favorite-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: white;
    border: none;
    border-radius: 50%;
    width: 35px;
    height: 35px;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.no-photo {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #777;
}

.product-info {
    padding: 18px;
}

.product-info h2 {
    margin: 0 0 8px;
    font-size: 21px;
    color: #212529;
}

.description {
    color: #666;
    font-size: 14px;
    margin-bottom: 15px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.details-button {
    display: block;
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 8px;
    background: #212529;
    color: white;
    font-size: 15px;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    box-sizing: border-box;
}

.details-button:hover {
    background: #343a40;
}
</style>