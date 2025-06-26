document.getElementById('generateBtn').addEventListener('click', () => {
    const size = parseInt(document.getElementById('sizeInput').value);
    
    fetch('/generate-mult-table/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // для Django CSRF защиты
            // вычитал, что в Django CSRF-защита необходима для обеспечения безопасности веб-приложений и 
            // защиты их пользователей от атак типа Cross-Site Request Forgery (CSRF).
        },
        body: JSON.stringify({ size: size })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка сети');
        }
        return response.text(); // сервер возвращает HTML
    })
    .then(html => {
        document.getElementById('tableContainer').innerHTML = html;
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('tableContainer').innerHTML = '<p>Ошибка при получении данных.</p>';
    });
});


// Данный кусок взят со Stack overflow
// Функция для получения CSRF токена из cookie
// Функция для получения CSRF-токена из cookie нужна, 
// чтобы автоматически и безопасно включать его в заголовки AJAX-запросов, 
// обеспечивая защиту от CSRF-атак при асинхронной отправке данных с помощью JavaScript.
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i=0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}