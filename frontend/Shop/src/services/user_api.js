const API_URL = "http://127.0.0.1:8000";

export async function loginUser(email, password) {
    const response = await fetch(
        `${API_URL}/users/login`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }
    );

    return response;
}

export async function createUser(
    email, 
    password, ) {
        const response = await fetch(
        `${API_URL}/users/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                hashed_password: password,
                email: email,
            })
        }
    );

    return response;
}

export async function getUser(userId) {
    const response = await fetch(
        `${API_URL}/users/${userId}`
    );

    return response;
}

export async function uploadAvatar(userId, file) {
    const user = JSON.parse(localStorage.getItem('user'));

    const formData = new FormData();
    formData.append('avatar', file);

    const response = await fetch(
        `${API_URL}/users/${userId}/avatar`,
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