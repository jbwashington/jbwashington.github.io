# localStorage Helper Functions

Utilities for working with localStorage that handle JSON serialization and errors.

```javascript
// Save data to localStorage
function saveToStorage(key, value) {
    try {
        const serialized = JSON.stringify(value);
        localStorage.setItem(key, serialized);
        return true;
    } catch (err) {
        console.error('Failed to save to localStorage:', err);
        return false;
    }
}

// Load data from localStorage
function loadFromStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (err) {
        console.error('Failed to load from localStorage:', err);
        return defaultValue;
    }
}

// Remove item from localStorage
function removeFromStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (err) {
        console.error('Failed to remove from localStorage:', err);
        return false;
    }
}

// Clear all localStorage
function clearStorage() {
    try {
        localStorage.clear();
        return true;
    } catch (err) {
        console.error('Failed to clear localStorage:', err);
        return false;
    }
}

// Check if localStorage is available
function isStorageAvailable() {
    try {
        const test = '__storage_test__';
        localStorage.setItem(test, test);
        localStorage.removeItem(test);
        return true;
    } catch (err) {
        return false;
    }
}
```

## Usage Example

```javascript
// Save user preferences
saveToStorage('theme', { mode: 'dark', fontSize: 16 });

// Load user preferences
const theme = loadFromStorage('theme', { mode: 'light', fontSize: 14 });

// Update history
const history = loadFromStorage('history', []);
history.push({ action: 'login', timestamp: Date.now() });
saveToStorage('history', history.slice(-10)); // Keep only last 10
```

## Storage Limits

- localStorage typically has a 5-10MB limit per origin
- Storing large amounts of data can throw a QuotaExceededError
- Always wrap operations in try-catch blocks
