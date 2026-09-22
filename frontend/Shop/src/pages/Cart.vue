<script setup>
import { ref, onMounted } from 'vue';
import { getCart, removeFromCart, checkout } from '../services/cart_api';
import { useRouter } from 'vue-router';

const cart = ref(null);
const error = ref('');
const address = ref('');
const router = useRouter();

async function fetchCart() {
    try {
        const res = await getCart();
        if (res.ok) {
            cart.value = await res.json();
        } else {
            cart.value = null;
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function removeItem(id) {
    try {
        const res = await removeFromCart(id);
        if (res.ok) {
            fetchCart();
        }
    } catch (err) {
        console.error('Failed to remove item');
    }
}

async function handleCheckout() {
    if (!address.value) {
        alert('Будь ласка, введіть адресу доставки');
        return;
    }
    try {
        const res = await checkout(address.value);
        if (res.ok) {
            alert('Замовлення успішно оформлено!');
            router.push('/');
        } else {
            const data = await res.json();
            alert(data.detail || 'Помилка оформлення');
        }
    } catch (err) {
        alert('Помилка з\'єднання');
    }
}

onMounted(fetchCart);
</script>

<template>
    <div class="cart-page">
        <div class="header-cart">
            <h1>Кошик</h1>
            <router-link to="/" class="back-btn">Назад до каталогу</router-link>
        </div>

        <div v-if="!cart || cart.items.length === 0" class="empty-cart">
            <p>Ваш кошик порожній</p>
            <router-link to="/" class="details-button">До каталогу</router-link>
        </div>

        <div v-else class="cart-content">
            <div class="items-list">
                <div v-for="item in cart.items" :key="item.order_item_id" class="cart-item">
                    <img v-if="item.photo" :src="`http://127.0.0.1:8000/${item.photo}`" alt="" class="item-img" />
                    <div v-else class="item-img no-photo">No photo</div>

                    <div class="item-info">
                        <h3>{{ item.name }}</h3>
                        <p>Ціна: {{ item.price }}$</p>
                        <p>Кількість: {{ item.amount }}</p>
                        <p class="cost">Всього: <b>{{ item.cost }}$</b></p>
                    </div>

                    <button class="delete-btn" @click="removeItem(item.order_item_id)" title="Видалити">🗑️</button>
                </div>
            </div>

            <div class="cart-summary">
                <h2>Разом: {{ cart.total_cost }}$</h2>
                <div class="input-group">
                    <label>Адреса доставки:</label>
                    <input type="text" v-model="address" placeholder="Місто, відділення НП..." class="form-input" />
                </div>
                <button class="checkout-btn" @click="handleCheckout">Оформити замовлення</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.cart-page {
    --bg-main: #FFFFFF;
    --text-main: #1F2937;
    --text-muted: #6B7280;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --border-light: #E5E7EB;

    padding: 40px;
    background: var(--bg-main);
    min-height: calc(100vh - 90px);
    box-sizing: border-box;
    font-family: 'Inter', 'Montserrat', sans-serif;
}

.header-cart {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
}

.header-cart h1 {
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

.empty-cart {
    text-align: center;
    background: #FFFFFF;
    padding: 60px 20px;
    border: 1px solid var(--border-light);
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
}

.empty-cart p {
    color: var(--text-muted);
    font-size: 16px;
    margin-bottom: 20px;
}

.details-button {
    display: inline-block;
    padding: 12px 24px;
    border-radius: 10px;
    background: var(--text-main);
    color: white;
    font-weight: 600;
    text-decoration: none;
    margin-top: 5px;
    transition: background 0.2s ease;
}

.details-button:hover {
    background: var(--accent-primary);
}

.cart-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 30px;
    align-items: start;
}

.items-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.cart-item {
    display: flex;
    align-items: center;
    background: #FFFFFF;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid var(--border-light);
    gap: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    transition: box-shadow 0.2s ease;
}

.cart-item:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
}

.item-img {
    width: 90px;
    height: 90px;
    object-fit: cover;
    border-radius: 10px;
    background: #F9FAFB;
    flex-shrink: 0;
}

.no-photo {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 13px;
}

.item-info {
    flex: 1;
}

.item-info h3 {
    margin: 0 0 6px;
    color: var(--text-main);
    font-size: 18px;
    font-weight: 600;
}

.item-info p {
    margin: 4px 0;
    color: var(--text-muted);
    font-size: 14px;
}

.cost {
    margin-top: 8px !important;
    font-size: 15px;
    color: var(--text-main);
}

.delete-btn {
    background: #FEF2F2;
    border: 1px solid #FCA5A5;
    border-radius: 10px;
    width: 40px;
    height: 40px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

.delete-btn:hover {
    background: #FEE2E2;
    transform: scale(1.05);
}

.cart-summary {
    background: #FFFFFF;
    padding: 30px;
    border-radius: 16px;
    border: 1px solid var(--border-light);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
    height: fit-content;
    position: sticky;
    top: 30px;
}

.cart-summary h2 {
    margin-top: 0;
    margin-bottom: 25px;
    color: var(--text-main);
    font-size: 22px;
    font-weight: 700;
}

.input-group {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.input-group label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-main);
}

.form-input {
    padding: 12px 16px;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    font-size: 15px;
    background: #F9FAFB;
    color: var(--text-main);
    outline: none;
    transition: border-color 0.2s ease;
}

.form-input:focus {
    border-color: var(--accent-primary);
    background: #FFFFFF;
}

.checkout-btn {
    width: 100%;
    padding: 14px;
    background: var(--accent-primary);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.1s ease;
}

.checkout-btn:hover {
    background: var(--accent-hover);
}

.checkout-btn:active {
    transform: scale(0.99);
}

@media (max-width: 900px) {
    .cart-content {
        grid-template-columns: 1fr;
    }

    .cart-page {
        padding: 20px;
    }

    .header-cart {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
}
</style>