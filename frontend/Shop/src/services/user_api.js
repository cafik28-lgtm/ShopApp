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
    firstName, 
    lastName,
    email, 
    password, 
    phone, 
    country, 
    city) {
        const response = await fetch(
        `${API_URL}/users/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                hashed_password: password,
                email: email,
                phone: phone,
                country: country,
                city: city
            })
        }
    );

    return response;
}