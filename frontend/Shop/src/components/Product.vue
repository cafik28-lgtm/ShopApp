<script setup>
import { ref, onMounted } from 'vue';
import { getProduct, deleteProduct } from '../services/product_api';
import { useRoute, useRouter } from 'vue-router';
import { getUser } from '../services/user_api';
import { getCategorie } from '../services/category_api';
import { getProductFeedbacks, createFeedback, deleteFeedback } from '../services/feedback_api';

const route = useRoute();
const router = useRouter();

const product = ref(null);
const error = ref('');
const seller = ref(null);
const category = ref(null);
const feedbacks = ref([]);

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

onMounted(() => {
    fetchProduct();
    fetchFeedbacks();
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

                    <h1>{{ product.name }} | {{ product.cost }}$</h1>

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
                        >
                            Buy
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
    min-height: calc(100vh - 90px);
    padding: 40px;
    background: #f5f5f5;
    box-sizing: border-box;
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

.product-rating {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 15px;
    font-size: 16px;
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
    margin-bottom: 15px;
}

.description {
    margin-bottom: 20px;
    font-size: 17px;
    line-height: 1.5;
    color: #555;
}

.amount {
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

.bottom-div{
    display: flex;
    flex-direction: column;
    margin-top: 40px;
}

.choice-div{
    display: flex;
}

/* Стили для блока отзывов */
.feedbacks-section {
    background: white;
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
}

.feedbacks-section h2 {
    margin-top: 0;
    margin-bottom: 20px;
    color: #212529;
}

.feedbacks-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 30px;
}

.feedback-item {
    padding: 15px;
    background: #fafafa;
    border: 1px solid #eee;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.feedback-header {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #666;
}

.feedback-text {
    margin: 0;
    color: #333;
}

.delete-feedback-btn {
    align-self: flex-start;
    padding: 5px 10px;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
}

.no-feedbacks {
    color: #777;
    margin-bottom: 20px;
}

.feedback-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    border-top: 1px solid #eee;
    padding-top: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.form-select, .form-textarea {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 15px;
    background: #fafafa;
}

.form-textarea {
    resize: vertical;
    min-height: 80px;
}

.submit-feedback-btn {
    padding: 10px 20px;
    background: #212529;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    align-self: flex-start;
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