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
    min-height: calc(100vh - 90px);
    padding: 30px;
    background: #f5f5f5;
    box-sizing: border-box;
}

.product-form {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    padding: 35px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    box-sizing: border-box;
}

.product-form h1 {
    margin: 0 0 30px;
    text-align: center;
    color: #212529;
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
    margin-bottom: 7px;
    color: #555;
}

.input-group input,
.input-group textarea,
.input-group select {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
    font-size: 15px;
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
    gap: 8px;
    margin-bottom: 20px;
}

.checkbox-group input {
    width: 17px;
    height: 17px;
    cursor: pointer;
}

.checkbox-group label {
    cursor: pointer;
}

.create-button {
    width: 100%;
    padding: 11px;
    border: none;
    border-radius: 8px;
    background: #212529;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

.create-button:hover {
    background: #343a40;
}

.error {
    margin-bottom: 15px;
    text-align: center;
    color: #dc3545;
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