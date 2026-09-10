const API_URL = "http://127.0.0.1:8000";

export async function loginAdmin(email, password) {
    const response = await fetch(
        `${API_URL}/admin/login`, {
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