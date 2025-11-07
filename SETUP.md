# Watchlist App Setup Instructions

Your watchlist app is ready! Just follow these simple steps to get it running.

## Step 1: Get a GitHub Personal Access Token

This allows the app to save your watchlist to this repository.

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: `Watchlist App`
4. Set expiration: "No expiration" (recommended for personal use)
5. Check the box for: **`repo`** (this gives full control of private repositories)
6. Scroll down and click "Generate token"
7. **COPY THE TOKEN** - you won't see it again! (looks like `ghp_xxxxxxxxxxxxxxxxxxxx`)

## Step 2: Get API Keys for Media Search

### TMDB API Key (Optional but Recommended)
This gives you rich movie/TV data and "where to watch" links. There's a demo key in the code, but getting your own is better.

1. Go to: https://www.themoviedb.org/signup
2. Create a free account
3. Go to: https://www.themoviedb.org/settings/api
4. Request an API key (choose "Developer")
5. Fill out the form (just say it's for personal use)
6. Copy your API Key (v3 auth)

### RAWG API Key (Required for Game Search)
This enables searching for video games with full metadata.

1. Go to: https://rawg.io/apidocs
2. Click "Get an API Key"
3. Create a free account
4. Copy your API Key (free tier: 20,000 requests/month)

### Book & Podcast APIs (No Keys Required!)
- **Books**: Uses Google Books API - works without an API key
- **Podcasts**: Uses iTunes API - works without an API key

## Step 3: Configure the App

1. Open the `watchlist/index.html` file in a text editor
2. Find the `CONFIG` section near the top of the `<script>` tag (around line 515)
3. Replace `YOUR_GITHUB_TOKEN_HERE` with your token from Step 1
4. Replace `YOUR_RAWG_API_KEY_HERE` with your RAWG key from Step 2
5. (Optional) Replace the `TMDB_API_KEY` with your own key from Step 2
6. Save the file

The config section should look like this:
```javascript
const CONFIG = {
    PASSWORD: 'give me movie show',
    GITHUB_TOKEN: 'ghp_your_actual_token_here',  // ← Paste your GitHub token here
    GITHUB_OWNER: 'cranberry-sam',
    GITHUB_REPO: 'cranberry-sam.github.io',
    GITHUB_BRANCH: 'claude/shared-media-watchlist-app-011CUuMXViUKygXXmh13CmZ5',
    TMDB_API_KEY: 'your_tmdb_key_here',  // ← Optional: paste your TMDB key
    RAWG_API_KEY: 'your_rawg_key_here'   // ← Required for game search
};
```

## Step 4: Enable GitHub Pages

1. Go to your repository settings on GitHub
2. Click "Pages" in the left sidebar
3. Under "Source", select your branch: `claude/shared-media-watchlist-app-011CUuMXViUKygXXmh13CmZ5`
4. Click "Save"
5. Wait a minute or two for it to deploy
6. Your app will be live at: `https://cranberry-sam.github.io/watchlist/`

## Step 5: Use the App!

1. Visit your GitHub Pages URL: `https://cranberry-sam.github.io/watchlist/`
2. Enter the password: `give me movie show`
3. Start adding movies, TV shows, books, games, podcasts, and more!

## How to Use

### Adding Items:
- **Movies & TV Shows**: Search with rich metadata from TMDB, including "where to watch" links
- **Games**: Search the RAWG database for video games with platforms and ratings
- **Books**: Search Google Books for any book with author info and descriptions
- **Podcasts**: Search iTunes for podcasts with artist info
- **Other media**: Use "Other (Manual)" for anything else (albums, documentaries, articles, etc.)

### Managing Items:
- **Mark as watched**: Click the "Mark Watched" button
- **Add review**: After marking as watched, you can add your thoughts
- **Remove**: Click the "Remove" button to delete an item
- **Filter**: Use the tabs to filter by status or media type

### Sharing with Your Wife:
- Just share the URL and the password
- You both can add, update, and review items
- All changes are automatically synced through GitHub
- Every action creates a commit, so you have a full history

## Troubleshooting

**"Failed to save changes"**: Check that your GitHub token is correct and has `repo` permissions

**"Search failed"**:
- For games: Check that your RAWG API key is correct
- For movies/TV: Your TMDB API key might be invalid or you've hit the rate limit (very rare)
- Books and podcasts should work without API keys

**Can't see GitHub Pages**: Make sure the repo is set to use GitHub Pages and the correct branch is selected

**Password not working**: Make sure it's exactly: `give me movie show` (lowercase, with spaces)

**Game search not working**: Make sure you've added your RAWG API key - this is required for game search

## Security Notes

- Since your repo is **private**, the embedded token is safe
- Only people with the password can use the app
- You can revoke and regenerate your GitHub token anytime
- Each change is tracked as a git commit for easy rollback if needed

---

Enjoy your watchlist! 🎬🍿
