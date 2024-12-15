async function loadWriteups() {
    try {
        const response = await fetch('writeups.json');
        const writeups = await response.json();

        const tagColors = [
            "w3-red", "w3-deep-purple", "w3-indigo", "w3-blue",
            "w3-light-blue", "w3-cyan", "w3-aqua", "w3-teal", "w3-green", "w3-light-green",
            "w3-lime", "w3-sand", "w3-khaki", "w3-yellow", "w3-amber", "w3-orange",
            "w3-deep-orange", "w3-blue-gray", "w3-brown", "w3-light-gray", "w3-gray",
            "w3-dark-gray", "w3-pale-red", "w3-pale-yellow", "w3-pale-green", "w3-pale-blue"
        ];

        const tagMap = {};
        let colorIndex = 0;

        function getTagColor(tag) {
            if (!tagMap[tag]) {
                tagMap[tag] = tagColors[colorIndex % tagColors.length];
                colorIndex++;
            }
            return tagMap[tag];
        }

        const writeupsContainer = document.querySelector('.lista_de_writeups');
        const tagsContainer = document.querySelector('.barra_de_etiquetas > div');
        const allTags = new Set();

        writeups.forEach(writeup => {
            const writeupElement = document.createElement('a');
            writeupElement.className = 'w3-card writeup-item';
            writeupElement.href = writeup.url;

            const sortedTags = writeup.tags.sort();
            const tagHTML = sortedTags
                .map(tag => {
                    allTags.add(tag);
                    return `<span class="${getTagColor(tag)}">${tag}</span>`;
                })
                .join(' ');

            writeupElement.innerHTML = `
                <h4>${writeup.title}</h4>
                <p>${tagHTML}</p>
                <p class="fecha">${writeup.date}</p>
            `;

            writeupsContainer.appendChild(writeupElement);
        });

        Array.from(allTags).sort().forEach(tag => {
            const tagButton = document.createElement('button');
            tagButton.className = 'w3-bar-item w3-button botones';
            tagButton.textContent = tag;
            tagButton.setAttribute('onclick', `filterWriteups('${tag}')`);
            tagsContainer.appendChild(tagButton);
        });

    } catch (error) {
        console.error('Error cargando los writeups:', error);
    }
}

function filterWriteups(tag) {
    const writeups = document.querySelectorAll('.writeup-item');
    const buttons = document.querySelectorAll('.botones');

    // Array para almacenar las etiquetas activadas
    let selectedTags = [];

    // Si se selecciona "All", desmarcar todos los botones y mostrar todos los writeups
    if (tag === 'All') {
        // Si "All" es seleccionado, desmarcar todos los demás botones
        buttons.forEach(button => button.classList.remove('active'));
        const allButton = Array.from(buttons).find(button => button.textContent === 'All');
        if (allButton) {
            allButton.classList.add('active');
        }

        // Mostrar todos los writeups
        writeups.forEach(writeup => {
            writeup.style.display = 'flex';
        });
        return;
    }

    // Buscar el botón correspondiente a la etiqueta seleccionada y alternar su estado
    const clickedButton = Array.from(buttons).find(button => button.textContent === tag);
    if (clickedButton) {
        clickedButton.classList.toggle('active');
    }

    // Guardar las etiquetas seleccionadas
    selectedTags = Array.from(buttons)
        .filter(button => button.classList.contains('active') && button.textContent !== 'All')
        .map(button => button.textContent);

    // Si no hay etiquetas seleccionadas, activar "All" y mostrar todos los writeups
    if (selectedTags.length === 0) {
        const allButton = Array.from(buttons).find(button => button.textContent === 'All');
        if (allButton) {
            allButton.classList.add('active');
        }

        writeups.forEach(writeup => {
            writeup.style.display = 'flex';
        });
        return;
    }

    // Desmarcar "All" si hay otras etiquetas activadas
    const allButton = Array.from(buttons).find(button => button.textContent === 'All');
    if (allButton) {
        allButton.classList.remove('active');
    }

    // Filtrar los writeups según las etiquetas activas
    writeups.forEach(writeup => {
        const tagSpans = writeup.querySelectorAll('span');
        const tags = Array.from(tagSpans).map(span => span.textContent);

        // Verificar si el writeup tiene todas las etiquetas seleccionadas
        const matchesAllTags = selectedTags.every(tag => tags.includes(tag));

        if (matchesAllTags) {
            writeup.style.display = 'flex';
        } else {
            writeup.style.display = 'none';
        }
    });
}






document.addEventListener('DOMContentLoaded', loadWriteups);
