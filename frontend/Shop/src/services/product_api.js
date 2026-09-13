const API_URL = 'http://127.0.0.1:8000';

export async function getProducts() {
    return await fetch(`${API_URL}/products/`);
}

export async function getProduct(productId) {
    const response = await fetch(
        `${API_URL}/products/${productId}`
    );
    
    return response;
}