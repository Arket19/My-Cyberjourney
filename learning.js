async function loadJourneys() {
    try {
        const response = await fetch('learning.json');
        const journeys = await response.json();

        const writeupsContainer = document.querySelector('.lista_de_journeys');

        journeys.forEach(journey => {
            const journeyElement = document.createElement('div');
            journeyElement.className = 'w3-card journey-item';
            journeyElement.href = journey.url;
            journeyElement.innerHTML = `
                <p class="fecha">${journey.date}</p>
                <p class="texto">${journey.text}</p>
            `;
            writeupsContainer.appendChild(journeyElement);
        });

    } catch (error) {
        console.error('Error cargando los journeys:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadJourneys);
