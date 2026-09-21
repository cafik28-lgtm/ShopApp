const API_URL = 'http://127.0.0.1:8000';

export async function getFavorites() {
    const user = JSON.parse(localStorage.getItem('user'));

    const response = await fetch(
        `${API_URL}/favorites/`,
        {
            method: 'GET',
            headers: {
                email: user.email,
                password: user.password 
            }
        }
    );

    return response;
}

export async function addFavorites(productId){
    const user = JSON.parse(localStorage.getItem('user'));
    const response = await fetch(`${API_URL}/favorites/?product_id=${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'email': user.email,
            'password': user.password,
        }
    });
    return response;
} 

export async function deleteFavorite(productId) {
    const user = JSON.parse(localStorage.getItem('user'));

    const response = await fetch(
        `${API_URL}/favorites/favorite/${productId}/delete`,
        {
            method: 'DELETE',
            headers: {
                email: user.email,
                password: user.password
            }
        }
    );

    return response;
}
