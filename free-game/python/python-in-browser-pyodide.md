# Running Python in the Browser with Pyodide

Pyodide brings Python and the scientific stack to the browser via WebAssembly.

## Basic Setup

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
</head>
<body>
    <textarea id="code" rows="10" cols="50">
print("Hello from Python!")
import sys
print(f"Python version: {sys.version}")
    </textarea>
    <button onclick="runPython()">Run</button>
    <pre id="output"></pre>

    <script>
        let pyodide;

        async function loadPyodide() {
            pyodide = await loadPyodide();
            console.log('Pyodide loaded');
        }

        async function runPython() {
            if (!pyodide) {
                await loadPyodide();
            }

            const code = document.getElementById('code').value;
            const output = document.getElementById('output');

            try {
                // Redirect stdout to capture print statements
                pyodide.runPython(`
                    import sys
                    from io import StringIO
                    sys.stdout = StringIO()
                `);

                // Run the user's code
                pyodide.runPython(code);

                // Get the output
                const result = pyodide.runPython('sys.stdout.getvalue()');
                output.textContent = result;
            } catch (err) {
                output.textContent = `Error: ${err}`;
            }
        }

        // Load Pyodide when page loads
        loadPyodide();
    </script>
</body>
</html>
```

## Using Python Packages

```javascript
async function setupPyodide() {
    pyodide = await loadPyodide();

    // Load packages
    await pyodide.loadPackage(['numpy', 'pandas']);

    console.log('Pyodide and packages loaded');
}

// Use NumPy
const result = pyodide.runPython(`
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5])
    arr.mean()
`);
console.log('Mean:', result);
```

## Accessing JavaScript from Python

```javascript
// Make JavaScript functions available to Python
pyodide.globals.set('jsAlert', (msg) => alert(msg));

pyodide.runPython(`
    # Call JavaScript function from Python
    jsAlert("Hello from Python!")
`);
```

## Available Packages

Pyodide includes many scientific packages:
- numpy, pandas, scipy, matplotlib
- scikit-learn, networkx
- And many more from PyPI

Check the [Pyodide package list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) for what's available.

## Performance Notes

- First load can take a few seconds (downloading WASM)
- Execution speed is close to native Python
- Some packages may not be fully compatible
- Browser-based, so no filesystem access by default
