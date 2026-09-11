const API_URL = 'http://127.0.0.1:8000';

export async function getCategories() {
    return await fetch(`${API_URL}/categories/`);
}

export async function createCategory(name, description) {
    const admin = JSON.parse(localStorage.getItem('admin'));
    return await fetch(`${API_URL}/categories/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'email': admin?.email || '',
            'password': admin?.password || ''
        },
        body: JSON.stringify({ name, description })
    });
}

export async function deleteCategory(id) {
    const admin = JSON.parse(localStorage.getItem('admin'));
    return await fetch(`${API_URL}/categories/${id}`, {
        method: 'DELETE',
        headers: {
            'email': admin?.email || '',
            'password': admin?.password || ''
        }
    });
}
