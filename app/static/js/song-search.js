document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('song-input');
    const suggestionsList = document.getElementById('suggestions');
    const selectedSongDiv = document.getElementById('selected-song');

    searchInput.addEventListener('input', function () {
        const searchTerm = searchInput.value;

        if (searchTerm.length < 2) {
            suggestionsList.innerHTML = '';
            suggestionsList.classList.add('hidden');
            return;
        }

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'search_term': searchTerm
            })
        })
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = '';
                data.forEach(item => {
                    item.similar_songs.forEach(song => {
                        const li = document.createElement('li');
                        li.textContent = song;
                        li.classList.add('cursor-pointer', 'hover:bg-gray-100', 'px-4', 'py-2');
                        li.addEventListener('click', function () {
                            selectedSongDiv.innerHTML = `Selected Song: ${item.original_song}`;
                        });
                        suggestionsList.appendChild(li);
                    });
                });
                suggestionsList.classList.remove('hidden');
            })
            .catch(error => console.error('Error:', error));
    });
});
