// ===== КОНФИГУРАЦИЯ =====
// Меняй здесь URL своего API
const API_URL = 'http://localhost/api';
// ========================

// Проверка авторизации при загрузке страницы
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const currentPage = window.location.pathname;
    
    // Страницы, доступные без авторизации
    const publicPages = ['/auth.html', '/index.html', '/'];
    
    if (!token && !publicPages.includes(currentPage)) {
        window.location.href = 'auth.html';
        return false;
    }
    
    if (token && currentPage === '/auth.html') {
        window.location.href = 'index.html';
        return false;
    }
    
    return true;
}

// Выход из системы
function logout() {
    const refresh_token = localStorage.getItem('refresh_token');
    
    if (refresh_token) {
        fetch(`${API_URL}/auth/logout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh_token })
        }).catch(console.error);
    }
    
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = 'auth.html';
}

// Получить заголовки с токеном
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Обновление токена
async function refreshToken() {
    const refresh_token = localStorage.getItem('refresh_token');
    
    if (!refresh_token) {
        throw new Error('No refresh token');
    }
    
    const response = await fetch(`${API_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_token })
    });
    
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token);
        }
        return data.access_token;
    } else {
        throw new Error('Refresh failed');
    }
}

// Универсальный fetch с автоматическим обновлением токена
async function fetchWithAuth(url, options = {}) {
    let accessToken = localStorage.getItem('access_token');
    
    const makeRequest = (token) => fetch(`${API_URL}${url}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers
        }
    });
    
    let response = await makeRequest(accessToken);
    
    // Если токен просрочен - пробуем обновить
    if (response.status === 401) {
        try {
            const newToken = await refreshToken();
            response = await makeRequest(newToken);
        } catch (error) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = 'auth.html';
            throw error;
        }
    }
    
    return response;
}

// Показать уведомление
function showNotification(message, type = 'success') {
    // Удаляем старые уведомления
    const oldNotifications = document.querySelectorAll('.notification');
    oldNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}