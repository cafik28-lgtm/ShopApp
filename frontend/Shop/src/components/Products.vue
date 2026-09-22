<script setup>
import { onMounted, ref } from 'vue';
import { getProducts } from '../services/product_api';
import { useRouter } from 'vue-router';
import { getCategories } from '../services/category_api';
import { getFavorites, addFavorites, deleteFavorite } from '../services/favorites_api';
import { addToCart } from '../services/cart_api';

import likedImg from '../assets/favorites/liked.png';
import notLikedImg from '../assets/favorites/notliked.png';

const allProducts = ref([]);
const products = ref([]);
const categories = ref([]);
const selected = ref('');
const error = ref('');

const favoriteIds = ref(new Set());

const router = useRouter();

const user = JSON.parse(localStorage.getItem('user'));


async function fetchProductsAndFavorites() {
    try {
        const resProducts = await getProducts();

        if (resProducts.ok) {
            const data = await resProducts.json();

            allProducts.value = data;
            products.value = data;
        } else {
            const data = await resProducts.json();
            error.value = data.detail || 'Помилка отримання товарів';
        }

        if (user) {
            const resFavs = await getFavorites();

            if (resFavs.ok) {
                const data = await resFavs.json();

                favoriteIds.value = new Set(
                    data.items.map(item => item.product_id)
                );
            }
        }
    } catch (err) {
        console.error(err);
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

                // Створюємо новий Set, щоб Vue точно побачив зміни
                favoriteIds.value = new Set(favoriteIds.value);
            }
        } else {
            const response = await addFavorites(productId);

            if (response.ok) {
                favoriteIds.value.add(productId);

                // Створюємо новий Set, щоб Vue точно побачив зміни
                favoriteIds.value = new Set(favoriteIds.value);
            }
        }
    } catch (err) {
        console.error('Error toggling favorite', err);
    }
}


async function handleAddToCart(productId) {
    if (!user) {
        router.push('/login');
        return;
    }

    try {
        const response = await addToCart(productId, 1);

        if (response.ok) {
            alert('Товар додано до кошика!');
        } else {
            const data = await response.json();

            alert(data.detail || 'Помилка додавання');
        }
    } catch (err) {
        console.error('Error adding to cart', err);
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
        console.error('Помилка завантаження категорій', err);
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
        error.value = 'Помилка фільтрації товарів';
    }
}


onMounted(fetchProductsAndFavorites);
onMounted(fetchCategories);
</script>


<template>
    <div class="products-page">

        <div class="header-product">
            <h1>Products</h1>

            <button
                class="details-button"
                v-if="user"
                type="button"
                @click="addProduct"
            >
                Add product
            </button>
        </div>


        <div class="category-filter">
            <select
                v-model="selected"
                @change="filterProductsByCategory"
            >
                <option value="">All categories</option>

                <option
                    v-for="c in categories"
                    :key="c.id"
                    :value="c.id"
                >
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


                    <button
                        class="favorite-btn"
                        @click.stop="toggleFavorite(p.id)"
                        :title="
                            favoriteIds.has(p.id)
                                ? 'Видалити з обраного'
                                : 'Додати в обране'
                        "
                    >
                        <img
                            :src="
                                favoriteIds.has(p.id)
                                    ? likedImg
                                    : notLikedImg
                            "
                            class="fav-icon"
                            alt="favorite"
                        />
                    </button>

                </div>


                <div class="product-info">

                    <h2>
                        {{ p.name }} | {{ p.cost }}$
                    </h2>


                    <div
                        class="product-rating"
                        v-if="p.reviews_count > 0"
                    >
                        <span class="stars">
                            ⭐ {{ p.average_rating }}
                        </span>

                        <span class="reviews-count">
                            ({{ p.reviews_count }})
                        </span>
                    </div>


                    <div
                        class="product-rating no-reviews"
                        v-else
                    >
                        <span>
                            No reviews
                        </span>
                    </div>


                    <router-link
                        :to="`/products/${p.id}`"
                        class="details-button"
                    >
                        View details
                    </router-link>


                    <button
                        v-if="user"
                        class="details-button add-cart-btn"
                        @click.stop="handleAddToCart(p.id)"
                    >
                        🛒 В кошик
                    </button>

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

.header-product {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.header-product h1 {
    margin: 0;
    color: #212529;
}

.category-filter {
    margin-bottom: 30px;
}

.category-filter select {
    padding: 10px 14px;
    border: 2px solid #212529;
    border-radius: 8px;
    background: white;
    font-size: 15px;
    cursor: pointer;
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
    position: relative;
}

.product-image > img {
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

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 0;
    cursor: pointer;

    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

    transition: transform 0.1s;
    overflow: hidden;
}

.favorite-btn:hover {
    transform: scale(1.08);
}

.favorite-btn .fav-icon {
    width: 16px;
    height: 16px;
    object-fit: contain;
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


.add-cart-btn {
    margin-top: 10px;
    background: #28a745;
}

.add-cart-btn:hover {
    background: #218838;
}


.error {
    color: #dc3545;
}


.header-product .details-button {
    width: auto;
    padding: 10px 20px;
    font-size: 16px;
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

    .products-page {
        padding: 20px;
    }

    .header-product {
        gap: 15px;
        flex-direction: column;
        align-items: stretch;
    }
}

</style>
