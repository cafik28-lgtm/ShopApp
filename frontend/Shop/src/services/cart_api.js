const API_URL = "http://127.0.0.1:8000";

export async function getCart() {
    const user = JSON.parse(localStorage.getItem('user'));
    return await fetch(`${API_URL}/cart/`, {
        method: 'GET',
        headers: {
            'email': user?.email || '',
            'password': user?.password || ''
        }
    });
}

export async function addToCart(productId, amount = 1) {
    const user = JSON.parse(localStorage.getItem('user'));
    return await fetch(`${API_URL}/cart/add?product_id=${productId}&amount=${amount}`, {
        method: 'POST',
        headers: {
            'email': user?.email || '',
            'password': user?.password || ''
        }
    });
}

export async function removeFromCart(orderItemId) {
    const user = JSON.parse(localStorage.getItem('user'));
    return await fetch(`${API_URL}/cart/item/${orderItemId}`, {
        method: 'DELETE',
        headers: {
            'email': user?.email || '',
            'password': user?.password || ''
        }
    });
}

export async function checkout(address) {
    const user = JSON.parse(localStorage.getItem('user'));
    return await fetch(`${API_URL}/cart/checkout?address=${encodeURIComponent(address)}`, {
        method: 'POST',
        headers: {
            'email': user?.email || '',
            'password': user?.password || ''
        }
    });
}