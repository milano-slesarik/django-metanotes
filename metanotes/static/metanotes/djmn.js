document.addEventListener('DOMContentLoaded', () => {
    loadNotes();
    setInitialPosition();
    setupToggleClickListener();
});

function setupToggleClickListener() {
    const toggleBtn = document.getElementById('djmn-toggle');
    toggleBtn.addEventListener('click', function (event) {
        if (this.isDragging) {
            this.isDragging = false;
            return;
        }

        var overlay = document.querySelector('#djmn .djmn-notes-panel');
        var toggle = document.getElementById('djmn-toggle');
        overlay.style.top = toggle.style.top;
        overlay.style.display = 'block';
        toggle.style.display = 'none';
    });
}

document.querySelector('#djmn .djmn-notes-panel').addEventListener('click', function (event) {
    if (event.target === this) {
        var overlay = document.querySelector('#djmn .djmn-notes-panel');
        var toggle = document.getElementById('djmn-toggle');
        overlay.style.display = 'none';
        toggle.style.display = 'block';
    }
});

function loadNotes() {
    fetch('/metanotes/get/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(notes => {
        const list = document.getElementById('djmn-list');
        list.innerHTML = '';
        notes.reverse().forEach(note => {
            const div = document.createElement('div');
            div.className = 'djmn-note';

            // Format the timestamp to display date and hours:minutes
            const timestamp = new Date(note.timestamp);
            const formattedTimestamp = `${timestamp.toLocaleDateString()} ${timestamp.getHours()}:${timestamp.getMinutes()}`;

            div.innerHTML = `
                <p>${note.content}</p>
                <span class="author">${note.author}</span>
                <span class="timestamp">${formattedTimestamp}</span>
                <button class="djmn-remove-button" onclick="removeNote('${note.uuid}')">x</button>
            `;
            list.appendChild(div);
        });

        const toggleBtn = document.getElementById('djmn-toggle');
        if (notes.length > 0) {
            toggleBtn.classList.add('pulsing');
            toggleBtn.textContent = notes.length;
        } else {
            toggleBtn.classList.remove('pulsing');
            toggleBtn.textContent = '+';
        }

        // Ensure the toggle button remains clickable
        setupToggleClickListener();
    });
}

function addNote() {
    const content = document.getElementById('djmn-content').value;
    if (!content) {
        return;
    }
    fetch('/metanotes/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({content: content})
    })
    .then(response => response.json())
    .then(() => {
        document.getElementById('djmn-content').value = '';
        loadNotes();
    });
}

function removeNote(noteId) {
    fetch('/metanotes/remove/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: noteId})
    })
    .then(response => response.json())
    .then(() => {
        loadNotes();
    });
}

// Drag-and-drop functionality along Y-axis only
dragElement(document.getElementById('djmn-toggle'));

function dragElement(elmnt) {
    var pos2 = 0, pos4 = 0, isDragging = false;
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
        isDragging = false;
        elmnt.isDragging = false;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        pos2 = pos4 - e.clientY;
        pos4 = e.clientY;
        elmnt.style.top = (elmnt.offsetTop - pos2) + 'px';
        localStorage.setItem('djmnTop', elmnt.style.top);
        isDragging = true;
        elmnt.isDragging = true;
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
        if (isDragging) {
            elmnt.click = function (event) {
                event.preventDefault();
                isDragging = false;
                elmnt.click = null;
            }
        }
        isDragging = false;
    }
}

function setInitialPosition() {
    const storedPosition = localStorage.getItem('djmnTop');
    if (storedPosition) {
        document.getElementById('djmn-toggle').style.top = storedPosition;
    }
}
