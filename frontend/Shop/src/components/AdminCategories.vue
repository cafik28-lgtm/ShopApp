<script setup>
import { ref, onMounted } from 'vue';
import { getCategories, createCategory, deleteCategory } from '../services/category_api';

const categories = ref([]);
const name = ref('');
const description = ref('');

// блокаем форму во время запроса, что бы не спамить запрсами
const loading = ref(false);

// Состояние для всплывающих уведомлений
const notification = ref({ message: '', type: '' });

function showNotification(message, type = 'success') {
    notification.value = { message, type };
    setTimeout(() => {
        if (notification.value.message === message) {
            notification.value = { message: '', type: '' };
        }
    }, 3000);
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

async function handleCreate() {
    if (loading.value) return;
    loading.value = true;
    
    try {
        const response = await createCategory(name.value, description.value);
        if (response.ok) {
            name.value = '';
            description.value = '';
            await fetchCategories();
            showNotification('Категорію успішно створено!', 'success');
        } else {
            const data = await response.json();
            showNotification(data.detail || 'Помилка створення', 'error');
        }
    } catch (err) {
        showNotification('Помилка підключення до сервера', 'error');
    } finally {
        loading.value = false;
    }
}

async function handleDelete(id) {
    try {
        const response = await deleteCategory(id);
        if (response.ok) {
            await fetchCategories();
            showNotification('Категорію успішно видалено!', 'success');
        } else {
            const data = await response.json();
            showNotification(data.detail || 'Помилка видалення', 'error');
        }
    } catch (err) {
        showNotification('Помилка підключення до сервера', 'error');
    }
}

onMounted(fetchCategories);
</script>

    <template>
        <div class="admin-categories-page container mt-5 position-relative">
        <transition name="fade">
            <div v-if="notification.message" 
                 :class="['alert', notification.type === 'success' ? 'alert-success' : 'alert-danger', 'custom-toast']" 
                 role="alert">
                {{ notification.message }}
            </div>
        </transition>

        <h2 class="text-center mb-4">Category Management</h2>

        <form @submit.prevent="handleCreate" class="card p-4 mb-4 shadow-sm mx-auto form-card">
            <h4 class="mb-3 text-center">Add New Category</h4>
            <div class="mb-3">
                <label class="form-label">Name</label>
                <input v-model="name" type="text" class="form-control" required :disabled="loading" />
            </div>
            <div class="mb-3">
                <label class="form-label">Description</label>
                <input v-model="description" type="text" class="form-control" :disabled="loading" />
            </div>
            <button type="submit" class="btn btn-dark w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                {{ loading ? 'Creating...' : 'Create Category' }}
            </button>
        </form>

        <!-- Список категорий по центру -->
        <div class="mx-auto list-container">
            <h4 class="mb-3">Existing Categories</h4>
            <ul class="list-group">
                <li v-for="cat in categories" :key="cat.id" class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>{{ cat.name }}</strong> — <small class="text-muted">{{ cat.description || 'No description' }}</small>
                    </div>
                    <button @click="handleDelete(cat.id)" class="btn btn-danger btn-sm">Delete</button>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>
.admin-categories-page {
    --bg-main: #FFFFFF;
    --text-main: #1F2937;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --accent-danger: #EF4444;
    --border-light: #E5E7EB;
    
    font-family: 'Inter', 'Montserrat', sans-serif;
    color: var(--text-main);
}

.form-card, .list-container {
    max-width: 600px;
}

.card {
    background-color: #FFFFFF;
    border: 1px solid var(--border-light) !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03) !important;
}

.btn-dark {
    background-color: var(--accent-primary) !important;
    border-color: var(--accent-primary) !important;
    border-radius: 10px;
    padding: 12px;
    font-weight: 600;
    transition: background-color 0.2s ease;
}

.btn-dark:hover:not(:disabled) {
    background-color: var(--accent-hover) !important;
    border-color: var(--accent-hover) !important;
}

.form-control {
    border-radius: 10px;
    border: 1px solid var(--border-light);
    padding: 10px 14px;
}

.form-control:focus {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

.list-group-item {
    border: 1px solid var(--border-light) !important;
    margin-bottom: 8px;
    border-radius: 10px !important;
    padding: 14px 18px;
}

.btn-danger {
    background-color: #EF4444;
    border: none;
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: 600;
}

.btn-danger:hover {
    background-color: #DC2626;
}

.custom-toast {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1050;
    min-width: 250px;
    text-align: center;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
    opacity: 0;
}
</style>