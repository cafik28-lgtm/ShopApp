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
    padding: 30px 40px;
    background: #f5f5f5;
    min-height: calc(100vh - 90px);
    box-sizing: border-box;
}

.header-cart {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.header-cart h1 {
    margin: 0;
    color: #212529;
}

.back-btn {
    text-decoration: none;
    color: #212529;
    background: white;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: 500;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.empty-cart {
    text-align: center;
    background: white;
    padding: 40px;
    border-radius: 12px;
}

.details-button {
    display: inline-block;
    padding: 10px 20px;
    border-radius: 8px;
    background: #212529;
    color: white;
    text-decoration: none;
    margin-top: 15px;
}

.cart-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 30px;
}

.items-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.cart-item {
    display: flex;
    align-items: center;
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 2px solid #212529;
    gap: 20px;
}

.item-img {
    width: 90px;
    height: 90px;
    object-fit: cover;
    border-radius: 8px;
    background: #eee;
}

.no-photo {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #777;
    font-size: 12px;
}

.item-info {
    flex: 1;
}

.item-info h3 {
    margin: 0 0 8px;
    color: #212529;
}

.item-info p {
    margin: 4px 0;
    color: #555;
    font-size: 15px;
}

.cost {
    margin-top: 8px;
    font-size: 16px;
    color: #212529;
}

.delete-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    transition: transform 0.1s;
}

.delete-btn:hover {
    transform: scale(1.1);
}

.cart-summary {
    background: white;
    padding: 25px;
    border-radius: 12px;
    border: 2px solid #212529;
    height: fit-content;
}

.cart-summary h2 {
    margin-top: 0;
    margin-bottom: 20px;
    color: #212529;
}

.input-group {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-input {
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 15px;
}

.checkout-btn {
    width: 100%;
    padding: 14px;
    background: #212529;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.2s;
}

.checkout-btn:hover {
    background: #343a40;
}

@media (max-width: 900px) {
    .cart-content {
        grid-template-columns: 1fr;
    }
}
</style>