<script setup>
import { ref, onMounted } from 'vue';
import { getProduct, deleteProduct } from '../services/product_api';
import { useRoute, useRouter } from 'vue-router';
import { getUser } from '../services/user_api';
import { getCategorie } from '../services/category_api';
import { getProductFeedbacks, createFeedback, deleteFeedback } from '../services/feedback_api';
import { getFavorites, addFavorites, deleteFavorite } from '../services/favorites_api';
import { addToCart } from '../services/cart_api';

import notLiked from '../assets/favorites/notliked.png';
import liked from '../assets/favorites/liked.png';

const route = useRoute();
const router = useRouter();

const product = ref(null);
const error = ref('');
const seller = ref(null);
const category = ref(null);
const feedbacks = ref([]);
const isFavorite = ref(false);

const newRating = ref(5);
const newFeedbackText = ref('');

const currentUser = JSON.parse(localStorage.getItem('user'));
const currentUserId = currentUser ? currentUser.user_id : null;
const admin = JSON.parse(localStorage.getItem('admin'));

const productId = route.params.productId;

async function fetchProduct() {
    try {
        const response = await getProduct(productId);

        if (response.ok) {
            product.value = await response.json();

            const sellerResponse = await getUser(product.value.seller_id);

            if(sellerResponse.ok){
                seller.value = await sellerResponse.json();
            } else {
                const data = await response.json();
                error.value = data.detail || 'Error with get seller';
                return;
            }

            const categoryResponse = await getCategorie(product.value.category_id);

            if (categoryResponse.ok) {
                category.value = await categoryResponse.json();
            } else {
                const data = await categoryResponse.json();
                error.value = data.detail || 'Error with get category';
            }
        } else {
            const data = await response.json();
            error.value = data.detail || 'Помилка отримання товару';
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function fetchFeedbacks() {
    try {
        const response = await getProductFeedbacks(productId);
        if (response.ok) {
            feedbacks.value = await response.json();
        }
    } catch (err) {
        console.error('Failed to load feedbacks');
    }
}

async function updateProduct() {
    router.push(`/products/${productId}/edit`);
}

async function handleDeleteProduct() {
    try {
        const response = await deleteProduct(productId);
        if (response.ok) {
            router.push('/');
        } else {
            const data = await response.json();
            error.value = data.detail || 'Помилка видалення товару';
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function handleCreateFeedback() {
    if (!newFeedbackText.value.trim()) return;
    try {
        const response = await createFeedback(
            Number(productId),
            Number(newRating.value),
            newFeedbackText.value
        );
        if (response.ok) {
            newFeedbackText.value = '';
            newRating.value = 5;
            fetchFeedbacks();
        } else {
            const data = await response.json();
            error.value = data.detail || 'Failed to post feedback';
        }
    } catch (err) {
        error.value = 'Connection error';
    }
}

async function handleDeleteFeedback(feedbackId) {
    try {
        const response = await deleteFeedback(feedbackId);
        if (response.ok) {
            fetchFeedbacks();
        } else {
            const data = await response.json();
            error.value = data.detail || 'Failed to delete feedback';
        }
    } catch (err) {
        error.value = 'Connection error';
    }
}

async function checkFavorite() {
    if(!currentUser) return;

    try{
        const response = await getFavorites();

        if(response.ok) {
            const data = await response.json();

            for(const favorite of data.items){
                if(favorite.product_id === Number(productId)) {
                    isFavorite.value = true;
                    break;
                }
            }
        }
    } catch(err){
        console.error('Failed to check favorite');
    }
}

async function clickFavorite() {
    if(!currentUser) return;

    try{
        if(isFavorite.value){
            const response = await deleteFavorite(productId);

            if(response.ok){
                isFavorite.value = false;
            } 
        }
        else {
            const response = await addFavorites(productId);
            
            if(response.ok){
                isFavorite.value = true;
            }
        }
    } catch(err){
        console.error('Favorite error');
    }
}

async function handleAddToCart() {
    if (!currentUser) {
        router.push('/login');
        return;
    }
    
    if (!product.value || !product.value.in_stock) {
        alert('Цього товару немає в наявності.');
        return;
    }

    try {
        const response = await addToCart(Number(productId), 1);
        if (response.ok) {
            alert('Товар додано до кошика!');
        } else {
            const data = await response.json();
            alert(data.detail || 'Помилка додавання до кошика');
        }
    } catch (err) {
        console.error('Error adding to cart', err);
        alert('Помилка з\'єднання');
    }
}

onMounted(() => {
    fetchProduct();
    fetchFeedbacks();
    checkFavorite();
});
</script>

<template>
    <div class="product-page">

        <div v-if="error" class="error">
            {{ error }}
        </div>

        <div v-else-if="product" class="product-container">
            <div class="product-card">

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
                    <div class="title-row">

                        <h1>{{ product.name }} | {{ product.cost }}$</h1>

                        <button class="favorite-button"
                        v-if="currentUser"
                        @click="clickFavorite">
                            <img
                                v-if="isFavorite"
                                :src="liked"
                                alt="Liked"
                            />
                            <img 
                                v-else="isFavorite"
                                :src="notLiked"
                                alt="Not liked"
                            />
                        </button>
                    </div>

                    <!-- Блок со средним рейтингом -->
                    <div class="product-rating" v-if="product.reviews_count > 0">
                        <span class="stars">⭐ {{ product.average_rating }}</span>
                        <span class="reviews-count">({{ product.reviews_count }} reviews)</span>
                    </div>
                    <div class="product-rating no-reviews" v-else>
                        <span>No reviews yet</span>
                    </div>

                    <p class="description">
                        {{ product.description || 'No description' }}
                    </p>

                    <p v-if="product.in_stock" class="amount">
                        Available: {{ product.amount }}
                    </p>

                     <p v-else class="amount">
                        Available: 0
                    </p>

                    <div v-if="category" class="category">
                        <span class="category-name">
                            Category: {{ category.name }}
                        </span>

                        <span class="category-description">
                            - {{ category.description || 'No description' }}
                        </span>
                    </div>
                    <div class="bottom-div">
                        <!-- Покупатель -->
                        <button v-if="product.seller_id !== currentUserId && !admin"
                        class="buy-button"
                        :class="product.in_stock ? 'available' : 'unavailable'"
                        :disabled="!product.in_stock"
                        @click="handleAddToCart"
                        >
                            {{ product.in_stock ? '🛒 Додати в кошик' : 'Немає в наявності' }}
                        </button>

                        <!-- Владелец или Админ -->
                        <div class="choice-div" v-if="product.seller_id === currentUserId || admin">
                            <button
                                v-if="product.seller_id === currentUserId"
                                class="buy-button available"
                                style="margin-right: 10px;"
                                @click="updateProduct"
                            >
                                Update
                            </button>
                            <button
                                class="buy-button available"
                                style="background: #dc3545;"
                                @click="handleDeleteProduct"
                            >
                                Delete Product
                            </button>
                        </div>

                        <router-link v-if="seller" :to="`/user/profile/${seller.id}`"
                                class="seller-link">
                            {{ seller.first_name || seller.last_name ? seller.first_name + ' ' + seller.last_name + ' | ' : '' }} {{ seller.email }}
                        </router-link>
                    </div>
                </div>

            </div>

            <!-- Блок отзывов и фидбеков -->
            <div class="feedbacks-section">
                <h2>Reviews & Feedbacks</h2>

                <div v-if="feedbacks.length" class="feedbacks-list">
                    <div v-for="f in feedbacks" :key="f.id" class="feedback-item">
                        <div class="feedback-header">
                            <span class="rating">⭐ {{ f.rating }} / 5</span>
                            <span class="date">{{ new Date(f.created_at).toLocaleDateString() }}</span>
                        </div>
                        <p class="feedback-text">{{ f.feedback }}</p>
                        
                        <button 
                            v-if="currentUserId === f.customer_id" 
                            class="delete-feedback-btn"
                            @click="handleDeleteFeedback(f.id)"
                        >
                            Delete
                        </button>
                    </div>
                </div>
                <p v-else class="no-feedbacks">No reviews yet. Be the first!</p>

                <!-- Форма добавления отзыва -->
                <form v-if="currentUser" @submit.prevent="handleCreateFeedback" class="feedback-form">
                    <h3>Leave a review</h3>
                    <div class="form-group">
                        <label>Rating:</label>
                        <select v-model="newRating" class="form-select">
                            <option value="5">5 - Excellent</option>
                            <option value="4">4 - Good</option>
                            <option value="3">3 - Average</option>
                            <option value="2">2 - Poor</option>
                            <option value="1">1 - Terrible</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <textarea 
                            v-model="newFeedbackText" 
                            placeholder="Write your review here..." 
                            required
                            class="form-textarea"
                        ></textarea>
                    </div>
                    <button type="submit" class="submit-feedback-btn">Submit Review</button>
                </form>
            </div>
        </div>

    </div>
</template>

<style scoped>
.product-page {
    --bg-main: #FFFFFF;
    --text-main: #1F2937;
    --text-muted: #6B7280;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --accent-warning: #F59E0B;
    --border-light: #E5E7EB;

    min-height: calc(100vh - 90px);
    padding: 40px;
    background: var(--bg-main);
    box-sizing: border-box;
    font-family: 'Inter', 'Montserrat', sans-serif;
}

.product-container {
    max-width: 1000px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.product-card {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 50px;
    padding: 40px;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
    box-sizing: border-box;
}

.product-image {
    height: 450px;
    background: #F9FAFB;
    border-radius: 15px;
    overflow: hidden;
    position: relative;
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
    color: var(--text-muted);
    font-size: 14px;
}

.product-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.product-info h1 {
    margin: 0 0 15px;
    font-size: 32px;
    color: var(--text-main);
    font-weight: 700;
    letter-spacing: -0.5px;
}

.product-rating {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 15px;
    font-size: 15px;
}

.stars {
    font-weight: 600;
    color: var(--accent-warning);
}

.reviews-count {
    color: var(--text-muted);
}

.no-reviews {
    color: var(--text-muted);
    font-style: italic;
    margin-bottom: 15px;
}

.description {
    margin-bottom: 20px;
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-muted);
}

.amount {
    margin: 5px 0;
    font-size: 15px;
    color: var(--text-main);
    font-weight: 500;
}

.category {
    margin-top: 10px;
    font-size: 15px;
    color: var(--text-muted);
}

.category-name {
    font-weight: 600;
    color: var(--text-main);
}

.buy-button {
    margin-top: 25px;
    padding: 14px 25px;
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
}

.buy-button.available {
    background: var(--accent-primary);
}

.buy-button.available:hover {
    background: var(--accent-hover);
}

.buy-button.unavailable {
    background: var(--accent-danger);
    cursor: not-allowed;
}

.error {
    color: var(--accent-danger);
    background: #FEF2F2;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #FCA5A5;
    text-align: center;
    max-width: 1000px;
    margin: 0 auto 20px auto;
}

.seller-link {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 16px;
    border-radius: 10px;
    background: #F9FAFB;
    border: 1px solid var(--border-light);
    color: var(--text-main);
    text-decoration: none;
    font-size: 15px;
    font-weight: 500;
    transition: all 0.2s;
}

.seller-link:hover {
    background: var(--border-light);
    transform: translateY(-1px);
}

.bottom-div {
    display: flex;
    flex-direction: column;
    margin-top: 25px;
}

.choice-div {
    display: flex;
}

.feedbacks-section {
    background: #FFFFFF;
    padding: 40px;
    border: 1px solid var(--border-light);
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
}

.feedbacks-section h2 {
    margin-top: 0;
    margin-bottom: 25px;
    color: var(--text-main);
    font-size: 24px;
    font-weight: 700;
}

.feedbacks-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 30px;
}

.feedback-item {
    padding: 20px;
    background: #F9FAFB;
    border: 1px solid var(--border-light);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.feedback-header {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: var(--text-muted);
}

.rating {
    font-weight: 600;
    color: var(--accent-warning);
}

.feedback-text {
    margin: 0;
    color: var(--text-main);
    font-size: 15px;
}

.delete-feedback-btn {
    align-self: flex-start;
    padding: 6px 12px;
    background: var(--accent-danger);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
}

.delete-feedback-btn:hover {
    background: #DC2626;
}

.no-feedbacks {
    color: var(--text-muted);
    margin-bottom: 25px;
    font-style: italic;
}

.feedback-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    border-top: 1px solid var(--border-light);
    padding-top: 30px;
}

.feedback-form h3 {
    margin: 0 0 5px 0;
    color: var(--text-main);
    font-size: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-main);
}

.form-select, .form-textarea {
    padding: 12px 16px;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    font-size: 15px;
    background: #F9FAFB;
    color: var(--text-main);
    outline: none;
    transition: border-color 0.2s;
}

.form-select:focus, .form-textarea:focus {
    border-color: var(--accent-primary);
    background: #FFFFFF;
}

.form-textarea {
    resize: vertical;
    min-height: 100px;
}

.submit-feedback-btn {
    padding: 12px 24px;
    background: var(--text-main);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    align-self: flex-start;
    transition: background 0.2s;
}

.submit-feedback-btn:hover {
    background: var(--accent-primary);
}

.title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.favorite-button {
    border: 1px solid var(--border-light);
    background: #FFFFFF;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s;
}

.favorite-button:hover {
    transform: scale(1.08);
}

.favorite-button img {
    width: 20px;
    height: 20px;
    object-fit: contain;
}

@media (max-width: 700px) {
    .product-card {
        grid-template-columns: 1fr;
        padding: 25px;
    }

    .product-image {
        height: 300px;
    }

    .product-page {
        padding: 20px;
    }

    .feedbacks-section {
        padding: 25px;
    }
}
</style>