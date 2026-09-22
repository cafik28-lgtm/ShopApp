<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getProduct, uploadProductMedia } from '../services/product_api';

const route = useRoute();
const router = useRouter();

const product = ref(null);
const mediaFile = ref(null);
const error = ref('');
const success = ref('');

async function handleProductUpload(event) {
    const file = event.target.files[0];

    if (!file) {
        return;
    }

    mediaFile.value = file;
    error.value = '';
    success.value = '';

    try {
        const productId = route.params.productId;

        const response = await uploadProductMedia(productId, file);

        if (response.ok) {
            const data = await response.json();

            console.log('Product media uploaded:', data);

            success.value = 'Product photo uploaded successfully';

            router.push(`/products/${productId}`);
        } else {
            const data = await response.json();
            error.value = data.detail || 'Failed to upload product photo';
        }
    } catch (err) {
        console.log(err);
        error.value = err.message;
    }
}

async function fetchProduct() {
    try {
        const productId = route.params.productId;

        const response = await getProduct(productId);

        if (response.ok) {
            product.value = await response.json();
        } else {
            const data = await response.json();
            error.value = data.detail || 'Failed to get product';
        }
    } catch (err) {
        error.value = 'Connection error';
    }
}

function goNext() {
    const productId = route.params.productId;
    router.push(`/products/${productId}`);
}

onMounted(fetchProduct);
</script>
<template>
    <div class="product-media-page">
        <div class="media-card">
            <h1>Add product photo</h1>

            <input
                class="file-input"
                type="file"
                accept="image/*"
                @change="handleProductUpload"
            />

            <p v-if="error" class="error">
                {{ error }}
            </p>

            <p v-if="success" class="success">
                {{ success }}
            </p>

            <button
                v-if="product && product.photo"
                class="upload-button"
                type="button"
                @click="goNext"
            >
                Save changes
            </button>
        </div>
    </div>
</template>

<style scoped>
.product-media-page {
    min-height: calc(100vh - 90px);
    padding: 40px;
    background: #f5f5f5;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
}

.media-card {
    width: 100%;
    max-width: 600px;
    padding: 40px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    text-align: center;
    box-sizing: border-box;
}

.media-card h1 {
    margin: 0 0 30px;
    color: #212529;
}

.file-input {
    width: 100%;
    padding: 12px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
    cursor: pointer;
}

.upload-button {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 8px;
    background: #212529;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

.upload-button:hover {
    background: #343a40;
}

.success {
    margin-top: 20px;
    color: #198754;
}

.error {
    margin-top: 20px;
    color: #dc3545;
}
</style>