<script setup>
import { ref, onMounted } from 'vue';
import { getCategories, createCategory, deleteCategory } from '../services/category_api';

const categories = ref([]);
const name = ref('');
const description = ref('');
const error = ref('');

async function fetchCategories() {
    try {
        const response = await getCategories();
        if (response.ok) {
            categories.value = await response.json();
        }
    } catch (err) {
        error.value = 'Помилка завантаження категорій';
    }
}

async function handleCreate() {
    error.value = '';
    try {
        const response = await createCategory(name.value, description.value);
        if (response.ok) {
            name.value = '';
            description.value = '';
            await fetchCategories();
        } else {
            const data = await response.json();
            error.value = data.detail || 'Помилка створення';
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

async function handleDelete(id) {
    try {
        const response = await deleteCategory(id);
        if (response.ok) {
            await fetchCategories();
        } else {
            const data = await response.json();
            error.value = data.detail || 'Помилка видалення';
        }
    } catch (err) {
        error.value = 'Помилка підключення до сервера';
    }
}

onMounted(fetchCategories);
</script>

<template>
    <div class="admin-categories-page container mt-5">
        <h2>Category Management</h2>

        <form @submit.prevent="handleCreate" class="card p-4 mb-4 shadow-sm">
            <h4>Add New Category</h4>
            <div class="mb-3">
                <label class="form-label">Name</label>
                <input v-model="name" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
                <label class="form-label">Description</label>
                <input v-model="description" type="text" class="form-control" />
            </div>
            <button type="submit" class="btn btn-dark">Create Category</button>
        </form>

        <p v-if="error" class="text-danger">{{ error }}</p>

        <h4>Existing Categories</h4>
        <ul class="list-group">
            <li v-for="cat in categories" :key="cat.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <strong>{{ cat.name }}</strong> — <small class="text-muted">{{ cat.description || 'No description' }}</small>
                </div>
                <button @click="handleDelete(cat.id)" class="btn btn-danger btn-sm">Delete</button>
            </li>
        </ul>
    </div>
</template>