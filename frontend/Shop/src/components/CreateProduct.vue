<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { createProduct } from '../services/product_api';
import { getCategories } from '../services/category_api';

const router = useRouter();

const user = JSON.parse(localStorage.getItem('user'));
const name = ref('');
const description = ref('');
const cost = ref('');
const amount = ref('');
const inStock = ref(true);
const categoryId = ref('');

const error = ref('');
const categories = ref([]);

async function handleCreate() {
    try{
        const response = await createProduct(
            user.user_id,
            name.value,
            description.value,
            cost.value,
            amount.value,
            inStock.value,
            categoryId.value
        )
        if(response.ok){
            const data = await response.json();
            router.push(`/products/${data.id}/media`)
        }
    } catch (err) {
        error.value = err
    }
}

async function fetchCategories() {
    try {
        const response = await getCategories();
        if (response.ok) {
            categories.value = await response.json();
        }
    } catch (err) {
        showNotification('Помилка завантаження категорій', 'error');
    }
}


onMounted(fetchCategories);
</script>

<template>
    <div class="create-product-page">
        <div class="product-form">
            <h1>Create product</h1>

            <form @submit.prevent="handleCreate">

                <div class="input-group">
                    <label>Name:</label>
                    <input
                        type="text"
                        v-model="name"
                        required
                    />
                </div>

                <div class="input-group">
                    <label>Description:</label>
                    <textarea
                        v-model="description"
                    ></textarea>
                </div>

                <div class="input-row">
                    <div class="input-group">
                        <label>Price:</label>
                        <input
                            type="number"
                            v-model="cost"
                            min="0"
                            required
                        />
                    </div>

                    <div class="input-group">
                        <label>Amount:</label>
                        <input
                            type="number"
                            v-model="amount"
                            min="0"
                            required
                        />
                    </div>
                </div>

                <div class="checkbox-group">
                    <input
                        id="inStock"
                        type="checkbox"
                        v-model="inStock"
                    />

                    <label for="inStock">
                        In stock
                    </label>
                </div>

                <div class="input-group">
                    <label>Category:</label>

                    <select
                        v-model="categoryId"
                        required
                    >
                        <option value="" disabled>
                            Select category
                        </option>

                        <option
                            v-for="category in categories"
                            :key="category.id"
                            :value="category.id"
                        >
                            {{ category.name }} — {{ category.description }}
                        </option>
                    </select>
                </div>

                <p v-if="error" class="error">
                    {{ error }}
                </p>

                <button
                    type="submit"
                    class="create-button"
                >
                    Next
                </button>

            </form>
        </div>
    </div>
</template>

<style scoped>
.create-product-page {
    --bg-main: #FFFFFF;
    --text-main: #1F2937;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --border-light: #E5E7EB;

    min-height: calc(100vh - 90px);
    padding: 40px;
    background: var(--bg-main);
    box-sizing: border-box;
    font-family: 'Inter', 'Montserrat', sans-serif;
}

.product-form {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    padding: 40px;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
    box-sizing: border-box;
}

.product-form h1 {
    margin: 0 0 30px;
    text-align: center;
    color: var(--text-main);
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.input-row {
    display: flex;
    gap: 20px;
}

.input-group {
    flex: 1;
    margin-bottom: 20px;
}

.input-group label {
    display: block;
    margin-bottom: 8px;
    color: var(--text-main);
    font-weight: 500;
    font-size: 14px;
}

.input-group input,
.input-group textarea,
.input-group select {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    box-sizing: border-box;
    font-size: 15px;
    color: var(--text-main);
    background-color: #F9FAFB;
    transition: border-color 0.2s, box-shadow 0.2s;
    outline: none;
}

.input-group input:focus,
.input-group textarea:focus,
.input-group select:focus {
    border-color: var(--accent-primary);
    background-color: #FFFFFF;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.12);
}

.input-group textarea {
    min-height: 120px;
    resize: vertical;
}

.input-group select {
    cursor: pointer;
}

.checkbox-group {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 25px;
}

.checkbox-group input {
    width: 18px;
    height: 18px;
    cursor: pointer;
    accent-color: var(--accent-primary);
}

.checkbox-group label {
    cursor: pointer;
    color: var(--text-main);
    font-size: 15px;
    user-select: none;
}

.create-button {
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 10px;
    background: var(--accent-primary);
    color: white;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.1s ease;
}

.create-button:hover {
    background: var(--accent-hover);
}

.create-button:active {
    transform: scale(0.99);
}

.error {
    margin-bottom: 15px;
    text-align: center;
    color: var(--accent-danger);
    font-size: 14px;
    font-weight: 500;
}

@media (max-width: 650px) {
    .input-row {
        flex-direction: column;
        gap: 0;
    }

    .create-product-page {
        padding: 20px;
    }

    .product-form {
        padding: 25px;
    }
}
</style>