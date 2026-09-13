<script setup>
import { onMounted, ref } from 'vue';
import { getProducts } from '../services/product_api';

const products = ref([]);
const error = ref('');

async function fetchProducts() {
    try {
        const response = await getProducts();

        if (response.ok) {
            products.value = await response.json();
        } else {
            const data = await response.json();
            error.value = data.detail || 'Помилка отримання товарів';
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

onMounted(fetchProducts);
</script>

<template>
    <div class="products-page">

        <h1>Products</h1>

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
                    <h2>{{ p.name }}</h2>

                    <p class="product-price">
                        {{ p.cost }} $
                    </p>

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
    margin: 0 0 10px;
    font-size: 21px;
    color: #212529;
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