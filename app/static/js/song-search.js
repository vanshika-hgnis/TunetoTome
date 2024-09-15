

// function searchSongs() {
//     const searchTerm = document.getElementById('song-input').value;

//     if (!searchTerm) {
//         alert('Please enter a song title.');
//         return;
//     }

//     fetch('/api/recommend-songs', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ search_term: searchTerm }),
//     })
//         .then(response => response.json())
//         .then(data => {
//             const suggestions = document.getElementById('suggestions');
//             suggestions.innerHTML = '';
//             suggestions.classList.remove('hidden');

//             data.forEach(recommendation => {
//                 const listItem = document.createElement('li');
//                 listItem.className = 'px-4 py-2 cursor-pointer hover:bg-gray-200';
//                 listItem.textContent = `${recommendation.full_title} (Similar: ${recommendation.similar_songs.join(', ')})`;

//                 listItem.addEventListener('click', () => {
//                     document.getElementById('song-input').value = recommendation.full_title;
//                     suggestions.classList.add('hidden');
//                     displaySelectedSong(recommendation);
//                     // fetchLyrics(recommendation.title, recommendation.artist);
//                 });

//                 suggestions.appendChild(listItem);
//             });
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
// }


// function fetchLyrics(songTitle, artistName) {
//     fetch('/api/fetch-lyrics', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ song_title: songTitle, artist_name: artistName }),
//     })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`HTTP error! status: ${response.status}`);
//             }
//             return response.json();
//         })
//         .then(data => {
//             const lyricsDisplay = document.getElementById('lyrics-display');
//             if (data.lyrics) {
//                 // Replace newlines with <br> tags for proper HTML display
//                 lyricsDisplay.innerHTML = data.lyrics.replace(/\n/g, '<br>');
//             } else {
//                 lyricsDisplay.textContent = 'Lyrics not found.';
//             }
//             lyricsDisplay.classList.remove('hidden');
//         })
//         .catch(error => {
//             console.error('Error fetching lyrics:', error);
//             const lyricsDisplay = document.getElementById('lyrics-display');
//             lyricsDisplay.textContent = `Error fetching lyrics: ${error.message}`;
//             lyricsDisplay.classList.remove('hidden');
//         });
// }







// function displaySelectedSong(recommendation) {
//     const selectedSongContainer = document.getElementById('selected-song');
//     selectedSongContainer.classList.remove('hidden');

//     document.getElementById('album-cover').src = recommendation.album_cover;
//     document.getElementById('song-title').textContent = recommendation.title;
//     document.getElementById('artist-name').textContent = recommendation.artist;

//     // Set hidden form inputs for song title and artist
//     document.getElementById('hidden-song-title').value = recommendation.title;
//     document.getElementById('hidden-artist-name').value = recommendation.artist;
// }


// document.getElementById('fetch-lyrics-btn').addEventListener('click', () => {
//     const songTitle = document.getElementById('hidden-song-title').value;
//     const artistName = document.getElementById('hidden-artist-name').value;
//     fetchLyrics(songTitle, artistName);
// });


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
            suggestions.innerHTML = '';
            suggestions.classList.remove('hidden');

            data.forEach(recommendation => {
                const listItem = document.createElement('li');
                listItem.className = 'px-4 py-2 cursor-pointer hover:bg-gray-200';
                listItem.textContent = `${recommendation.full_title} (Similar: ${recommendation.similar_songs.join(', ')})`;

                listItem.addEventListener('click', () => {
                    document.getElementById('song-input').value = recommendation.full_title;
                    suggestions.classList.add('hidden');
                    displaySelectedSong(recommendation);
                });

                suggestions.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function fetchLyrics(songTitle, artistName) {
    fetch('/api/fetch-lyrics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ song_title: songTitle, artist_name: artistName }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const lyricsDisplay = document.getElementById('lyrics-display');
            if (data.lyrics) {
                // Replace newlines with <br> tags for proper HTML display
                lyricsDisplay.innerHTML = data.lyrics.replace(/\n/g, '<br>');
            } else {
                lyricsDisplay.textContent = 'Lyrics not found.';
            }
            lyricsDisplay.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error fetching lyrics:', error);
            const lyricsDisplay = document.getElementById('lyrics-display');
            lyricsDisplay.textContent = `Error fetching lyrics: ${error.message}`;
            lyricsDisplay.classList.remove('hidden');
        });
}

function displaySelectedSong(recommendation) {
    const selectedSongContainer = document.getElementById('selected-song');
    selectedSongContainer.classList.remove('hidden');

    document.getElementById('album-cover').src = recommendation.album_cover;
    document.getElementById('song-title').textContent = recommendation.title;
    document.getElementById('artist-name').textContent = recommendation.artist;

    // Set hidden form inputs for song title and artist
    document.getElementById('hidden-song-title').value = recommendation.title;
    document.getElementById('hidden-artist-name').value = recommendation.artist;
}

document.getElementById('fetch-lyrics-btn').addEventListener('click', () => {
    const songTitle = document.getElementById('hidden-song-title').value;
    const artistName = document.getElementById('hidden-artist-name').value;
    fetchLyrics(songTitle, artistName);
});
