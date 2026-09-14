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

export async function createProduct(
    userId, 
    name,
    description,
    cost,
    amount,
    inStock,
    categoryId
) {
    const user = JSON.parse(localStorage.getItem('user'));

    const response = await fetch(
        `${API_URL}/products/seller=${userId}/create`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                email: user.email,
                password: user.password
            },
            body: JSON.stringify({
                name: name,
                description: description,
                cost: cost,
                amount: amount,
                in_stock: inStock,
                photo: null,
                created_at: new Date().toISOString(),
                category_id: categoryId
           })
        }
    );
    return response;
}

export async function uploadProductMedia(productId, file) {
    const user = JSON.parse(localStorage.getItem('user'));

    const formData = new FormData();
    formData.append('media', file);

    const response = await fetch(
        `${API_URL}/products/${productId}/media`,
        {
            method: 'PUT',
            headers: {
                email: user.email,
                password: user.password
            },
            body: formData
        }
    );

    return response;
}


export async function updateProduct(productId, data) {
    const user = JSON.parse(localStorage.getItem('user'));

    const response = await fetch(
        `${API_URL}/products/${productId}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                email: user.email,
                password: user.password
            },
            body: JSON.stringify(data)
        }
    );

    return response;
}

export async function deleteProduct(productId) {
    const admin = JSON.parse(localStorage.getItem('admin'));
    const user = JSON.parse(localStorage.getItem('user'));
    
    const headers = {};
    if (admin) {
        headers['email'] = admin.email;
        headers['password'] = admin.password;
    } else if (user) {
        headers['email'] = user.email;
        headers['password'] = user.password;
    }

    const response = await fetch(
        `${API_URL}/products/${productId}`,
        {
            method: 'DELETE',
            headers: headers
        }
    );

    return response;
}