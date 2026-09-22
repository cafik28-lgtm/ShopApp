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
    --bg-main: #FFFFFF;
    --text-main: #1F2937;
    --text-muted: #6B7280;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --border-light: #E5E7EB;

    padding: 40px;
    box-sizing: border-box;
    min-height: calc(100vh - 90px);
    background: var(--bg-main);
    font-family: 'Inter', 'Montserrat', sans-serif;
}

.header-fav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
}

.header-fav h1 {
    margin: 0;
    color: var(--text-main);
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.back-btn {
    text-decoration: none;
    color: var(--text-main);
    font-weight: 600;
    font-size: 15px;
    background: #F9FAFB;
    padding: 10px 18px;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    transition: all 0.2s ease;
}

.back-btn:hover {
    background: var(--border-light);
    transform: translateY(-1px);
}

.empty-fav {
    text-align: center;
    padding: 60px 20px;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
}

.empty-fav p {
    color: var(--text-muted);
    font-size: 16px;
    margin-bottom: 20px;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 30px;
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
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.06);
    border-color: transparent;
}

.product-image {
    width: 100%;
    height: 260px;
    background: #F9FAFB;
    position: relative;
    border-radius: 15px 15px 0 0;
    overflow: hidden;
}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.4s ease;
}

.product-card:hover .product-image img {
    transform: scale(1.04);
}

.favorite-btn {
    position: absolute;
    top: 15px;
    right: 15px;
    background: white;
    border: 1px solid var(--border-light);
    border-radius: 50%;
    width: 38px;
    height: 38px;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: all 0.2s ease;
    z-index: 2;
}

.favorite-btn:hover {
    transform: scale(1.1);
    background: #FEF2F2;
    border-color: #FCA5A5;
}

.no-photo {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 14px;
}

.product-info {
    padding: 20px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.product-info h2 {
    margin: 0 0 6px;
    font-size: 18px;
    color: var(--text-main);
    font-weight: 600;
    line-height: 1.3;
}

.description {
    color: var(--text-muted);
    font-size: 13px;
    margin-bottom: 20px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.4;
}

.details-button {
    display: block;
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 10px;
    background: var(--text-main);
    color: white;
    font-size: 15px;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    box-sizing: border-box;
    transition: background 0.2s ease;
    margin-top: auto;
}

.details-button:hover {
    background: var(--accent-primary);
}

.error {
    color: var(--accent-danger);
    background: #FEF2F2;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #FCA5A5;
    margin-bottom: 20px;
}

@media (max-width: 600px) {
    .favorites-page {
        padding: 20px;
    }
    
    .header-fav {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
}
</style>