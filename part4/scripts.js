const API_BASE_URL = 'http://127.0.0.1:5000';

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

function populatePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    const options = ['10', '50', '100', 'All'];
    
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        priceFilter.appendChild(optionElement);
    });
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) {
            loginLink.style.display = 'block';
        }
    } else {
        if (loginLink) {
            loginLink.style.display = 'none';
        }
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/api/v1/places`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price);
        
        placeCard.innerHTML = `
            <div class="place-info">
                <h3>${place.title}</h3>
                <p>${place.description}</p>
                <p>Price: $${place.price}</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        `;
        
        placesList.appendChild(placeCard);
    });
}

function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const price = parseInt(card.getAttribute('data-price'));
        
        if (maxPrice === 'All') {
            card.style.display = 'block';
        } else {
            if (price <= parseInt(maxPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    const errorMessage = errorData.error || 'Login failed';
                    alert('Login failed: ' + errorMessage);
                }
            } catch (error) {
                alert('Login failed: ' + error.message);
            }
        });
    }

    const priceFilter = document.getElementById('price-filter');
    
    if (priceFilter) {
        populatePriceFilter();
        checkAuthentication();
        
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlacesByPrice(selectedPrice);
        });
    }
});