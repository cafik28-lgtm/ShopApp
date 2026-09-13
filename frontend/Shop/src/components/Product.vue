<script setup>
import { ref, onMounted } from 'vue';
import { getProduct } from '../services/product_api';
import { useRoute } from 'vue-router';
import { getUser } from '../services/user_api';

const route = useRoute();

const product = ref(null);
const error = ref('');
const seller = ref(null);

async function fetchProduct() {
    try {
        const productId = route.params.productId;

        const response = await getProduct(productId);

        if (response.ok) {
            product.value = await response.json();

            const sellerResponse = await getUser(product.value.seller_id);

            if(sellerResponse.ok){
                seller.value = await sellerResponse.json();
            } else {
                const data = await response.json();
                error.value = data.detail || 'Error with get seller';
            }
        } else {
            const data = await response.json();
            error.value = data.detail || 'Помилка отримання товару';
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

onMounted(fetchProduct);
</script>

<template>
    <div class="product-page">

        <div v-if="error" class="error">
            {{ error }}
        </div>

        <div v-else-if="product" class="product-card">

            <div class="product-image">
                <img
                    v-if="product.photo"
                    :src="`http://127.0.0.1:8000/${product.photo}`"
                    alt="product"
                />

                <div v-else class="no-photo">
                    No photo
                </div>
            </div>

            <div class="product-info">

                <h1>{{ product.name }}</h1>

                <p class="price">
                    {{ product.cost }} ₴
                </p>

                <p class="description">
                    {{ product.description || 'No description' }}
                </p>

                <p v-if="product.in_stock" class="amount">
                    Available: {{ product.amount }}
                </p>

                 <p v-else class="amount">
                    Available: 0
                </p>

                <button
                    class="buy-button"
                    :class="product.in_stock ? 'available' : 'unavailable'"
                    :disabled="!product.in_stock"
                >
                    Buy
                </button>

                <router-link :to="`/user/profile/${seller.id}`"
                        class="seller-link">
                    {{ seller.first_name }}{{ seller.last_name }}
                </router-link>

                

            </div>

        </div>

    </div>
</template>

<style scoped>
.product-page {
    min-height: calc(100vh - 90px);
    padding: 40px;
    background: #f5f5f5;
    box-sizing: border-box;
}

.product-card {
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 50px;
    padding: 40px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    box-sizing: border-box;
}

.product-image {
    height: 450px;
    background: #eee;
    border-radius: 15px;
    overflow: hidden;
}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
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
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.product-info h1 {
    margin: 0 0 15px;
    font-size: 36px;
    color: #212529;
}

.price {
    margin: 0 0 20px;
    font-size: 28px;
    font-weight: 600;
}

.description {
    margin-bottom: 20px;
    font-size: 17px;
    line-height: 1.5;
    color: #555;
}

.amount,
.stock {
    margin: 5px 0;
    font-size: 16px;
}

.buy-button {
    margin-top: 25px;
    padding: 13px 25px;
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 17px;
    cursor: pointer;
}

.buy-button.available {
    background: #212529;
}

.buy-button.unavailable {
    background: #dc3545;
    cursor: not-allowed;
}

.error {
    color: #dc3545;
    text-align: center;
}
.seller-link {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 16px;
    border-radius: 8px;
    background: #f1f1f1;
    color: #212529;
    text-decoration: none;
    font-size: 16px;
    font-weight: 500;
    transition: 0.2s;
}

.seller-link:hover {
    transform: translateY(-2px);
}

@media (max-width: 700px) {
    .product-card {
        grid-template-columns: 1fr;
        padding: 25px;
    }

    .product-image {
        height: 300px;
    }
}
</style>