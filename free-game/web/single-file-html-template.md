# Single-File HTML Tool Template

A complete template for creating self-contained HTML tools with Tailwind CSS.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen py-8">
    <div class="max-w-4xl mx-auto px-4">
        <div class="mb-6">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Tool Name</h1>
            <p class="text-gray-600">Brief description of what this tool does.</p>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
            <!-- Tool content here -->
            <label for="input" class="block text-sm font-medium text-gray-700 mb-2">
                Input
            </label>
            <input
                type="text"
                id="input"
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter something..."
            >

            <button
                onclick="process()"
                class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
            >
                Process
            </button>

            <div id="output" class="mt-4"></div>
        </div>
    </div>

    <script>
        // Load saved state on page load
        window.addEventListener('DOMContentLoaded', () => {
            const saved = localStorage.getItem('tool-state');
            if (saved) {
                document.getElementById('input').value = saved;
            }
        });

        // Save state on input change
        document.getElementById('input').addEventListener('input', (e) => {
            localStorage.setItem('tool-state', e.target.value);
        });

        // Main processing function
        function process() {
            const input = document.getElementById('input').value;
            const output = document.getElementById('output');

            // Do something with the input
            output.textContent = `Processed: ${input}`;
        }

        // Copy to clipboard helper
        async function copyToClipboard(text) {
            try {
                await navigator.clipboard.writeText(text);
                alert('Copied to clipboard!');
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        }
    </script>
</body>
</html>
```

## Key Features

- **Tailwind CSS via CDN** - No build step required
- **localStorage** - Persists state across page reloads
- **Responsive** - Works on mobile and desktop
- **Copy-to-clipboard** - Easy text copying functionality
- **Self-contained** - Everything in one file

## Customization Tips

1. Replace `Tool Name` with your actual tool name
2. Add more Tailwind utility classes for styling
3. Use `localStorage.getItem()` and `setItem()` for persistence
4. Add error handling with try-catch blocks
5. Include success/error message divs for user feedback
