// Media Import Script for Watchlist
// Run with: node import-script.js

const CONFIG = {
    TMDB_API_KEY: 'e3cabd714830aea7a4e8ff5d7d0b7044',
    RAWG_API_KEY: '44ba0f7cd39d4d5a89e9e69cdbf967a2',
    FIREBASE: {
        apiKey: "AIzaSyDvFCUnadbVzci6GrkXc4coybXEL-UDSww",
        authDomain: "watchlist-app-ec3a0.firebaseapp.com",
        projectId: "watchlist-app-ec3a0",
        storageBucket: "watchlist-app-ec3a0.firebasestorage.app",
        messagingSenderId: "585504841013",
        appId: "1:585504841013:web:f04fefc27095c3054e407c",
        measurementId: "G-4GKX86XXPJ"
    }
};

// Media to import - organized by type
const MEDIA_TO_IMPORT = {
    movies: [
        // Clear movies
        { title: "RRR", year: 2022 },
        { title: "Picnic at Hanging Rock", year: 1975 },
        { title: "Angel's Egg", year: 1985 },
        { title: "Suspiria", year: 1977 },
        { title: "The Departed", year: 2006 },
        { title: "The Graduate", year: 1967 },
        { title: "The Greasy Strangler", year: 2016 },
        { title: "The Whale", year: 2022 },
        { title: "Requiem for a Dream", year: 2000 },
        { title: "Hellzapoppin'", year: 1941 },
        { title: "Cryptozoo", year: 2021 },
        { title: "Bebe's Kids", year: 1992 },
        { title: "I Love You Phillip Morris", year: 2009 },
        { title: "Noroi: The Curse", year: 2005 },
        { title: "Black Swan", year: 2010 },
        { title: "Hunt for the Wilderpeople", year: 2016 },
        { title: "The NeverEnding Story", year: 1984 },
        { title: "Breakin'", year: 1984 },
        { title: "No Strings Attached", year: 2011 },
        { title: "Penguin Highway", year: 2018 },
        { title: "The Usual Suspects", year: 1995 },
        { title: "Three Identical Strangers", year: 2018 },
        { title: "Aniara", year: 2018 },
        { title: "I Care a Lot", year: 2020 },
        { title: "Poor Things", year: 2023 },
        { title: "How to Talk to Girls at Parties", year: 2017 },
        { title: "Jack and the Cuckoo-Clock Heart", year: 2013 },
        { title: "The Imitation Game", year: 2014 },
        { title: "Wizards", year: 1977 },
        { title: "UHF", year: 1989 },
        { title: "Tenacious D in The Pick of Destiny", year: 2006 },
        { title: "MirrorMask", year: 2005 },
        { title: "Sneakers", year: 1992 },
        { title: "Bernie", year: 2011 },
        { title: "Something in the Dirt", year: 2022 },
        { title: "The Borderlands", year: 2013 },
        { title: "Junk Head", year: 2017 },
        { title: "Mad God", year: 2021 },
        { title: "Wendell & Wild", year: 2022 },
        { title: "Marcel the Shell with Shoes On", year: 2021 },
        { title: "The Art of Self-Defense", year: 2019 },
        { title: "Napoleon Dynamite", year: 2004 },
        // Darkdorf recommendations
        { title: "Hereditary", year: 2018 },
        { title: "Caveat", year: 2020 },
        { title: "It Follows", year: 2014 },
        { title: "Alien", year: 1979 },
        { title: "Pulse", year: 2001 }, // Kairo
        { title: "The Conjuring 2", year: 2016 },
        { title: "Paranormal Activity 3", year: 2011 },
        { title: "Annabelle: Creation", year: 2017 },
        { title: "The Blair Witch Project", year: 1999 },
        { title: "REC", year: 2007 },
    ],

    tv: [
        { title: "The Summoning", year: 2017 },
        { title: "Murder, She Wrote", year: 1984 },
        { title: "1883", year: 2021 },
        { title: "Round the Twist", year: 1989 }, // "beyond the twist" = Round the Twist
        { title: "Grand Designs", year: 1999 },
        { title: "The Peripheral", year: 2022 },
        { title: "Barry", year: 2018 },
        { title: "Fired on Mars", year: 2023 },
        { title: "Pantheon", year: 2022 },
        { title: "Series 7: The Contenders", year: 2001 }, // Actually a movie
        { title: "Baskets", year: 2016 },
        { title: "Skip and Loafer", year: 2023 },
        { title: "Miracle Workers", year: 2019 },
        { title: "Tatami Time Machine Blues", year: 2022 },
        { title: "Severance", year: 2022 },
        { title: "The Watcher", year: 2022 },
    ],

    games: [
        { title: "Paratopic" },
        { title: "Fatum Betula" },
        { title: "OMORI" },
        { title: "Phantom Abyss" },
        { title: "Pepper Grinder" },
        { title: "Windosill" },
        { title: "Chop Goblins" },
        { title: "RimWorld" },
        { title: "Earth Defense Force 6" },
        { title: "Pizza Tower" },
        { title: "Hylics" },
        { title: "The Exit 8" },
    ],

    books: [
        { title: "Roadside Picnic", author: "Arkady Strugatsky" },
        { title: "Four Thousand Weeks", author: "Oliver Burkeman" },
        { title: "Humankind", author: "Rutger Bregman" },
        { title: "The Perfection of the Paper Clip", author: "James Ward" },
        { title: "Boom Town", author: "Sam Anderson" },
        { title: "The Vanishing Hitchhiker", author: "Jan Harold Brunvand" },
        { title: "Children of Time", author: "Adrian Tchaikovsky" },
        { title: "The City & The City", author: "China Miéville" },
        { title: "Revenge", author: "Yoko Ogawa" },
    ],

    podcasts: [
        { title: "Blowback" },
        { title: "Bone Valley" }, // completed
    ]
};

// Utility functions
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function searchTMDB(query, mediaType, year = null) {
    try {
        const searchUrl = `https://api.themoviedb.org/3/search/${mediaType}?api_key=${CONFIG.TMDB_API_KEY}&query=${encodeURIComponent(query)}${year ? `&year=${year}` : ''}`;
        const response = await fetch(searchUrl);
        const data = await response.json();

        if (data.results && data.results.length > 0) {
            const item = data.results[0];

            // Get detailed info for genres and watch providers
            const detailUrl = `https://api.themoviedb.org/3/${mediaType}/${item.id}?api_key=${CONFIG.TMDB_API_KEY}`;
            const detailResponse = await fetch(detailUrl);
            const detailData = await detailResponse.json();

            return {
                type: mediaType,
                apiId: item.id,
                title: item.title || item.name,
                year: (item.release_date || item.first_air_date || '').substring(0, 4),
                poster: item.poster_path ? `https://image.tmdb.org/t/p/w500${item.poster_path}` : null,
                overview: item.overview,
                genres: (detailData.genres || []).map(g => g.name),
                tmdbUrl: `https://www.themoviedb.org/${mediaType}/${item.id}`,
                watched: false,
                addedDate: new Date().toISOString()
            };
        }
        return null;
    } catch (error) {
        console.error(`Error searching TMDB for "${query}":`, error.message);
        return null;
    }
}

async function searchGame(query) {
    try {
        const response = await fetch(
            `https://api.rawg.io/api/games?key=${CONFIG.RAWG_API_KEY}&search=${encodeURIComponent(query)}&page_size=1`
        );
        const data = await response.json();

        if (data.results && data.results.length > 0) {
            const item = data.results[0];
            return {
                type: 'game',
                apiId: item.id,
                title: item.name,
                year: item.released ? item.released.substring(0, 4) : null,
                poster: item.background_image,
                overview: `Platforms: ${(item.platforms || []).map(p => p.platform.name).slice(0, 3).join(', ')}`,
                rating: item.rating,
                url: `https://rawg.io/games/${item.slug}`,
                genres: (item.genres || []).map(g => g.name),
                watched: false,
                addedDate: new Date().toISOString()
            };
        }
        return null;
    } catch (error) {
        console.error(`Error searching game "${query}":`, error.message);
        return null;
    }
}

async function searchBook(title, author = null) {
    try {
        const query = author ? `${title} ${author}` : title;
        const response = await fetch(
            `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(query)}&maxResults=1`
        );
        const data = await response.json();

        if (data.items && data.items.length > 0) {
            const item = data.items[0].volumeInfo;
            return {
                type: 'book',
                apiId: data.items[0].id,
                title: item.title,
                author: (item.authors || []).join(', '),
                year: item.publishedDate ? item.publishedDate.substring(0, 4) : null,
                poster: item.imageLinks?.thumbnail || null,
                overview: item.description || '',
                genres: item.categories || [],
                url: item.infoLink,
                watched: false,
                addedDate: new Date().toISOString()
            };
        }
        return null;
    } catch (error) {
        console.error(`Error searching book "${title}":`, error.message);
        return null;
    }
}

async function searchPodcast(query) {
    try {
        const response = await fetch(
            `https://itunes.apple.com/search?term=${encodeURIComponent(query)}&media=podcast&limit=1`
        );
        const data = await response.json();

        if (data.results && data.results.length > 0) {
            const item = data.results[0];
            return {
                type: 'podcast',
                apiId: item.collectionId,
                title: item.collectionName,
                artist: item.artistName,
                year: item.releaseDate ? new Date(item.releaseDate).getFullYear().toString() : null,
                poster: item.artworkUrl600 || item.artworkUrl100,
                overview: item.description || '',
                genres: item.genres || [],
                url: item.collectionViewUrl,
                watched: false,
                addedDate: new Date().toISOString()
            };
        }
        return null;
    } catch (error) {
        console.error(`Error searching podcast "${query}":`, error.message);
        return null;
    }
}

// Import functions
async function importMedia() {
    console.log('🚀 Starting media import...\n');

    const results = {
        success: [],
        failed: [],
        skipped: []
    };

    let totalItems = 0;
    for (const mediaType in MEDIA_TO_IMPORT) {
        totalItems += MEDIA_TO_IMPORT[mediaType].length;
    }

    let processedCount = 0;

    // Import Movies
    console.log('🎬 Importing Movies...');
    for (const movie of MEDIA_TO_IMPORT.movies) {
        processedCount++;
        console.log(`[${processedCount}/${totalItems}] Searching: ${movie.title} (${movie.year || 'no year'})`);

        const result = await searchTMDB(movie.title, 'movie', movie.year);
        if (result) {
            results.success.push({ original: movie.title, imported: result });
            console.log(`  ✅ Found: ${result.title} (${result.year})`);
        } else {
            results.failed.push({ title: movie.title, type: 'movie', reason: 'Not found in TMDB' });
            console.log(`  ❌ Not found`);
        }

        await sleep(300); // Rate limit
    }

    // Import TV Shows
    console.log('\n📺 Importing TV Shows...');
    for (const show of MEDIA_TO_IMPORT.tv) {
        processedCount++;
        console.log(`[${processedCount}/${totalItems}] Searching: ${show.title} (${show.year || 'no year'})`);

        const result = await searchTMDB(show.title, 'tv', show.year);
        if (result) {
            results.success.push({ original: show.title, imported: result });
            console.log(`  ✅ Found: ${result.title} (${result.year})`);
        } else {
            results.failed.push({ title: show.title, type: 'tv', reason: 'Not found in TMDB' });
            console.log(`  ❌ Not found`);
        }

        await sleep(300);
    }

    // Import Games
    console.log('\n🎮 Importing Games...');
    for (const game of MEDIA_TO_IMPORT.games) {
        processedCount++;
        console.log(`[${processedCount}/${totalItems}] Searching: ${game.title}`);

        const result = await searchGame(game.title);
        if (result) {
            results.success.push({ original: game.title, imported: result });
            console.log(`  ✅ Found: ${result.title}`);
        } else {
            results.failed.push({ title: game.title, type: 'game', reason: 'Not found in RAWG' });
            console.log(`  ❌ Not found`);
        }

        await sleep(300);
    }

    // Import Books
    console.log('\n📚 Importing Books...');
    for (const book of MEDIA_TO_IMPORT.books) {
        processedCount++;
        console.log(`[${processedCount}/${totalItems}] Searching: ${book.title} by ${book.author || 'unknown'}`);

        const result = await searchBook(book.title, book.author);
        if (result) {
            results.success.push({ original: book.title, imported: result });
            console.log(`  ✅ Found: ${result.title}`);
        } else {
            results.failed.push({ title: book.title, type: 'book', reason: 'Not found in Google Books' });
            console.log(`  ❌ Not found`);
        }

        await sleep(300);
    }

    // Import Podcasts
    console.log('\n🎙️ Importing Podcasts...');
    for (const podcast of MEDIA_TO_IMPORT.podcasts) {
        processedCount++;
        console.log(`[${processedCount}/${totalItems}] Searching: ${podcast.title}`);

        const result = await searchPodcast(podcast.title);
        if (result) {
            results.success.push({ original: podcast.title, imported: result });
            console.log(`  ✅ Found: ${result.title}`);
        } else {
            results.failed.push({ title: podcast.title, type: 'podcast', reason: 'Not found in iTunes' });
            console.log(`  ❌ Not found`);
        }

        await sleep(300);
    }

    return results;
}

// Main execution
async function main() {
    console.log('╔════════════════════════════════════════════════════╗');
    console.log('║        WATCHLIST MEDIA IMPORT SCRIPT               ║');
    console.log('╚════════════════════════════════════════════════════╝\n');

    const results = await importMedia();

    console.log('\n');
    console.log('╔════════════════════════════════════════════════════╗');
    console.log('║                  IMPORT SUMMARY                    ║');
    console.log('╚════════════════════════════════════════════════════╝');
    console.log(`✅ Successfully found: ${results.success.length} items`);
    console.log(`❌ Failed to find: ${results.failed.length} items`);

    if (results.failed.length > 0) {
        console.log('\n❌ Failed items:');
        results.failed.forEach(item => {
            console.log(`  - ${item.title} (${item.type}): ${item.reason}`);
        });
    }

    // Save results to JSON file for review
    const fs = require('fs');
    fs.writeFileSync('import-results.json', JSON.stringify(results, null, 2));
    console.log('\n💾 Full results saved to: import-results.json');

    console.log('\n🔥 Ready to push to Firebase!');
    console.log('📝 Review import-results.json to verify the data');
    console.log('🚀 Run with --upload flag to actually push to Firebase');
}

// Check if running with --upload flag
const shouldUpload = process.argv.includes('--upload');

if (shouldUpload) {
    console.log('Upload functionality not yet implemented - please review results first!');
} else {
    main().catch(console.error);
}
