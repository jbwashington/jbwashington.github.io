# Copy to Clipboard in JavaScript

Modern way to copy text to clipboard using the Clipboard API.

```javascript
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        console.log('Copied to clipboard!');
        return true;
    } catch (err) {
        console.error('Failed to copy:', err);
        return false;
    }
}

// Usage
copyToClipboard('Hello, World!');
```

## With fallback for older browsers

```javascript
function copyToClipboard(text) {
    // Modern API
    if (navigator.clipboard) {
        return navigator.clipboard.writeText(text);
    }

    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();

    try {
        document.execCommand('copy');
        return Promise.resolve();
    } catch (err) {
        return Promise.reject(err);
    } finally {
        document.body.removeChild(textarea);
    }
}
```

## Browser Support

The Clipboard API requires HTTPS (or localhost) and needs user permission. The `writeText()` method works in all modern browsers.
