const API_URL = "http://127.0.0.1:8000";

export async function getProductFeedbacks(productId) {
    const response = await fetch(`${API_URL}/feedbacks/product/${productId}`);
    return response;
}

export async function createFeedback(productId, rating, feedbackText) {
    const user = JSON.parse(localStorage.getItem('user'));
    const response = await fetch(`${API_URL}/feedbacks/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'email': user?.email || '',
            'password': user?.password || ''
        },
        body: JSON.stringify({
            product_id: productId,
            rating: rating,
            feedback: feedbackText
        })
    });
    return response;
}

export async function deleteFeedback(feedbackId) {
    const user = JSON.parse(localStorage.getItem('user'));
    const response = await fetch(`${API_URL}/feedbacks/${feedbackId}`, {
        method: 'DELETE',
        headers: {
            'email': user?.email || '',
            'password': user?.password || ''
        }
    });
    return response;
}