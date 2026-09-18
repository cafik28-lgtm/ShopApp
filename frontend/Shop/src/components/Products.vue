<script setup>
import { onMounted, ref } from 'vue';
import { getProducts } from '../services/product_api';
import { useRouter } from 'vue-router';
import { getCategories } from '../services/category_api';

const allProducts = ref([]);
const products = ref([]);
const categories = ref([]);
const selected = ref('');

const error = ref('');

const router = useRouter();

const user = JSON.parse(localStorage.getItem('user'));

async function fetchProducts() {
    try {
        const response = await getProducts();

        if (response.ok) {
            allProducts.value = await response.json();
            products.value = allProducts.value;
        } else {
            const data = await response.json();
            error.value = data.detail || 'Помилка отримання товарів';
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function addProduct() {
    router.push(`/products/seller=${user.user_id}/create`);
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
    if(selected.value === '') {
        products.value = allProducts.value;
        return;
    }

    try {
        products.value = [];
        for(const p of allProducts.value) {
            if(p.category_id === Number(selected.value)) {
                products.value.push(p);
            }
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}


onMounted(fetchProducts);
onMounted(fetchCategories);
</script>

<template>
    <div class="products-page">
        <div class="header-product">
            <div class="">
                <h1>Products</h1>
                <button class="details-button" 
                        v-if="user" 
                        type="button" 
                        @click="addProduct"
                >
                    Add product
                </button>  
            </div>
            <select v-model="selected" @change="filterProductsByCategory">
                <option value="">All categories</option>
                <option v-for="c in categories" :key="c.id" :value="c.id">
                    {{ c.name }}
                </option>
            </select>

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
.products-page {
    padding: 30px 40px;
    box-sizing: border-box;
}

.products-page h1 {
    margin-bottom: 30px;
    color: #212529;
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
    transition: transform 0.2s, box-shadow 0.2s;
}

.product-card.in-stock {
    border-color: #212529;
}

.product-card.out-of-stock {
    border-color: #dc3545;
}

.product-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
}

.product-image {
    width: 100%;
    height: 230px;
    background: #f1f1f1;
}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
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

/* Стили для блока рейтинга в карточке */
.product-rating {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 12px;
    font-size: 14px;
}

.stars {
    font-weight: 600;
    color: #212529;
}

.reviews-count {
    color: #777;
}

.no-reviews {
    color: #999;
    font-style: italic;
    font-size: 13px;
    margin-bottom: 12px;
}

.product-price {
    margin: 0 0 18px;
    font-size: 20px;
    font-weight: 600;
    color: #212529;
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

.error {
    color: #dc3545;
}

.header-product .details-button {
    width: 15vw;
    font-size: 32px;
    margin-bottom: 18px;
    margin-left: 15px;
}

.header-product {
    display: flex;
    align-items: center;
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

    .products-page {
        padding: 20px;
    }
}
</style>