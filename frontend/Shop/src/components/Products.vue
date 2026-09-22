<script setup>
import { onMounted, ref } from 'vue';
import { getProducts } from '../services/product_api';
import { getCategories } from '../services/category_api';
import { getFavorites, addFavorites, deleteFavorite } from '../services/favorites_api';
import { useRouter } from 'vue-router';

// Картинки для избранного
import likedImg from '../assets/favorites/liked.png';
import notLikedImg from '../assets/favorites/notliked.png';

const allProducts = ref([]);
const products = ref([]);
const categories = ref([]);
const selected = ref('');
const favoriteIds = ref(new Set());
const error = ref('');

const router = useRouter();
const user = JSON.parse(localStorage.getItem('user'));

async function fetchProductsAndFavorites() {
    try {
        const response = await getProducts();

        if (response.ok) {
            allProducts.value = await response.json();
            products.value = allProducts.value;
        } else {
            const data = await response.json();
            error.value = data.detail || 'Помилка отримання товарів';
        }

        if (user) {
            const resFavs = await getFavorites();
            if (resFavs.ok) {
                const data = await resFavs.json();
                favoriteIds.value = new Set(data.items.map(item => item.product_id));
            }
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function fetchCategories() {
    try {
        const response = await getCategories();
        if (response.ok) {
            categories.value = await response.json();
        }
    } catch (err) {
        console.error('Помилка завантаження категорій', 'error');
    }
}

async function filterProductsByCategory() {
    if (selected.value === '') {
        products.value = allProducts.value;
        return;
    }

    try {
        products.value = [];
        for (const p of allProducts.value) {
            if (p.category_id === Number(selected.value)) {
                products.value.push(p);
            }
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function toggleFavorite(productId) {
    if (!user) {
        router.push('/login');
        return;
    }

    try {
        if (favoriteIds.value.has(productId)) {
            const response = await deleteFavorite(productId);
            if (response.ok) {
                favoriteIds.value.delete(productId);
            }
        } else {
            const response = await addFavorites(productId);
            if (response.ok) {
                favoriteIds.value.add(productId);
            }
        }
    } catch (err) {
        console.error('Error toggling favorite', err);
    }
}

async function addProduct() {
    router.push(`/products/seller=${user.user_id}/create`);
}

onMounted(fetchProductsAndFavorites);
onMounted(fetchCategories);
</script>

<template>
    <div class="products-page">
        <div class="header-product">
            <h1>Products</h1>
            
            <div class="header-actions">
                <router-link v-if="user" to="/favorites" class="fav-page-link">⭐ Моє обране</router-link>
                <router-link v-if="user" to="/cart" class="fav-page-link">🛒 Кошик</router-link>
                
                <select class="category-select" v-model="selected" @change="filterProductsByCategory">
                    <option value="">All categories</option>
                    <option v-for="c in categories" :key="c.id" :value="c.id">
                        {{ c.name }}
                    </option>
                </select>

                <button class="details-button add-product-btn" 
                        v-if="user" 
                        type="button" 
                        @click="addProduct"
                >
                    Add product
                </button>  
            </div>
        </div>

        <p v-if="error" class="error">
            {{ error }}
        </p>

        <div v-else class="products-grid">
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

                    <button 
                        class="favorite-btn" 
                        @click.stop="toggleFavorite(p.id)"
                        :title="favoriteIds.has(p.id) ? 'Видалити з обраного' : 'Додати в обране'"
                    >
                        <img 
                            :src="favoriteIds.has(p.id) ? likedImg : notLikedImg" 
                            class="fav-icon" 
                            alt="favorite" 
                        />
                    </button>
                </div>

                <div class="product-info">
                    <h2>{{ p.name }} |  {{ p.cost }}$</h2>

                    <div class="product-rating" v-if="p.reviews_count > 0">
                        <span class="stars">⭐ {{ p.average_rating }}</span>
                        <span class="reviews-count">({{ p.reviews_count }})</span>
                    </div>
                    <div class="product-rating no-reviews" v-else>
                        <span>No reviews</span>
                    </div>

                    <router-link :to="`/products/${p.id}`" class="details-button">
                        View details
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Глобальные переменные для страницы */
.products-page {
    --bg-main: #FFFFFF;
    --bg-card: #FFFFFF;
    --bg-image: #F9FAFB;
    --text-main: #1F2937;
    --text-muted: #6B7280;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --accent-warning: #F59E0B;
    --border-light: #E5E7EB;

    padding: 40px;
    box-sizing: border-box;
    background-color: var(--bg-main);
    min-height: 100vh;
    font-family: 'Inter', 'Montserrat', sans-serif;
}

.header-product {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
    flex-wrap: wrap;
    gap: 20px;
}

.products-page h1 {
    margin: 0;
    color: var(--text-main);
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 15px;
}

.category-select {
    padding: 10px 16px;
    border-radius: 10px;
    border: 1px solid var(--border-light);
    font-size: 15px;
    color: var(--text-main);
    background-color: var(--bg-card);
    cursor: pointer;
    outline: none;
    transition: border-color 0.2s;
}

.category-select:focus {
    border-color: var(--accent-primary);
}

.fav-page-link {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-main);
    text-decoration: none;
    padding: 10px 18px;
    background: var(--bg-image);
    border: 1px solid var(--border-light);
    border-radius: 10px;
    transition: all 0.2s ease;
}

.fav-page-link:hover {
    background: var(--border-light);
    transform: translateY(-1px);
}

.header-product .add-product-btn {
    width: auto;
    padding: 10px 20px;
    font-size: 15px;
    margin: 0;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 30px;
}

.product-card {
    background: var(--bg-card);
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

.product-card.out-of-stock {
    opacity: 0.7;
    filter: grayscale(40%);
}

.product-image {
    width: 100%;
    height: 260px;
    background: var(--bg-image);
    position: relative;
    border-radius: 15px 15px 0 0;
    overflow: hidden;
}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.product-card:hover .product-image img {
    transform: scale(1.04);
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

.favorite-btn {
    position: absolute;
    top: 15px;
    right: 15px;
    background: white;
    border: 1px solid var(--border-light);
    border-radius: 50%;
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: all 0.2s ease;
    z-index: 2;
}

.favorite-btn:hover {
    transform: scale(1.1);
    border-color: var(--text-muted);
}

.favorite-btn img.fav-icon {
    width: 18px;
    height: 18px;
    object-fit: contain;
}

.out-of-stock-badge {
    position: absolute;
    bottom: 15px;
    left: 15px;
    background: var(--accent-danger);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    z-index: 2;
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

.price {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 12px;
}

.product-rating {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 20px;
    font-size: 14px;
}

.stars {
    font-weight: 600;
    color: var(--accent-warning);
}

.reviews-count, .no-reviews {
    color: var(--text-muted);
    font-size: 13px;
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
}

@media (max-width: 600px) {
    .products-page {
        padding: 20px;
    }
    
    .header-actions {
        width: 100%;
        flex-wrap: wrap;
    }
    
    .category-select, .details-button.add-product-btn {
        flex-grow: 1;
    }
}
</style>