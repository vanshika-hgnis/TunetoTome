function searchSongs() {
    const searchTerm = document.getElementById('song-input').value;

    if (!searchTerm) {
        alert('Please enter a song title.');
        return;
    }

    fetch('/api/recommend-songs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ search_term: searchTerm }),
    })
        .then(response => response.json())
        .then(data => {
            const suggestions = document.getElementById('suggestions');
            const selectedSongContainer = document.getElementById('selected-song');
            suggestions.innerHTML = '';  // Clear existing suggestions
            suggestions.classList.remove('hidden');  // Unhide the suggestions box

            // Loop over recommendations and add them to the suggestions list
            data.forEach(recommendation => {
                const listItem = document.createElement('li');
                listItem.className = 'px-4 py-2 cursor-pointer hover:bg-gray-200';  // Styling for list items
                listItem.textContent = `${recommendation.original_song} (Similar: ${recommendation.similar_songs.join(', ')})`;

                // Add an event listener for click events on each suggestion
                listItem.addEventListener('click', () => {
                    document.getElementById('song-input').value = recommendation.original_song;
                    suggestions.classList.add('hidden');  // Hide suggestions when a song is selected

                    // Display the selected song details
                    const selectedSongHtml = `
                    <div class="mt-8 mb-4 p-8 bg-white border border-black rounded-lg shadow-slate-200 shadow-sm flex flex-col items-center space-y-4 w-200">
                    <div class="mt-2 selected-song-details flex items-center space-x-4">
                    <!-- Album Cover -->
                    <div class="album-cover">
                    <img src="${recommendation.album_cover}" alt="Album Cover" class="w-32 h-32 object-cover rounded-lg">
                    </div>
                    <!-- Song Details -->
                    <div class="song-info">
                    <h2 class="text-2xl font-bold text-black">${recommendation.original_song}</h2>
                    <p class="text-sm text-black mt-1">${recommendation.artist_name}</p>
                    </div>
                    </div>
                    <p class="text-sm text-black mt-2">Similar Songs: ${recommendation.similar_songs.join(', ')}</p>
                    </div>
                    `;
                    selectedSongContainer.innerHTML = selectedSongHtml;  // Update the #selected-song container
                });

                suggestions.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
