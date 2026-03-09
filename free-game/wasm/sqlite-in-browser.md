# SQLite in the Browser with sql.js

Run SQLite databases entirely in the browser using WebAssembly.

## Basic Setup

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-wasm.js"></script>
</head>
<body>
    <button onclick="createDatabase()">Create DB</button>
    <button onclick="queryDatabase()">Query DB</button>
    <pre id="output"></pre>

    <script>
        let db;

        async function createDatabase() {
            // Initialize SQL.js
            const SQL = await initSqlJs({
                locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
            });

            // Create a new database
            db = new SQL.Database();

            // Create a table
            db.run(`
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE
                )
            `);

            // Insert some data
            db.run(`
                INSERT INTO users (name, email) VALUES
                ('Alice', 'alice@example.com'),
                ('Bob', 'bob@example.com'),
                ('Charlie', 'charlie@example.com')
            `);

            document.getElementById('output').textContent = 'Database created!';
        }

        function queryDatabase() {
            if (!db) {
                alert('Create database first!');
                return;
            }

            // Execute a query
            const results = db.exec('SELECT * FROM users');

            // Display results
            const output = document.getElementById('output');
            if (results.length > 0) {
                const columns = results[0].columns;
                const values = results[0].values;

                let text = columns.join('\t') + '\n';
                text += values.map(row => row.join('\t')).join('\n');

                output.textContent = text;
            }
        }

        // Save database to localStorage
        function saveDatabase() {
            const data = db.export();
            const buffer = new Uint8Array(data);
            localStorage.setItem('sqliteDb', JSON.stringify(Array.from(buffer)));
        }

        // Load database from localStorage
        async function loadDatabase() {
            const SQL = await initSqlJs({
                locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
            });

            const saved = localStorage.getItem('sqliteDb');
            if (saved) {
                const data = new Uint8Array(JSON.parse(saved));
                db = new SQL.Database(data);
            }
        }
    </script>
</body>
</html>
```

## Prepared Statements

```javascript
// Safer way to insert data with parameters
const stmt = db.prepare('INSERT INTO users (name, email) VALUES (?, ?)');
stmt.run(['David', 'david@example.com']);
stmt.free();
```

## Export Database

```javascript
// Export database as a file
function downloadDatabase() {
    const data = db.export();
    const blob = new Blob([data], { type: 'application/x-sqlite3' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'database.sqlite';
    a.click();

    URL.revokeObjectURL(url);
}
```

## Import Database from File

```javascript
async function loadDatabaseFromFile(file) {
    const SQL = await initSqlJs({
        locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
    });

    const arrayBuffer = await file.arrayBuffer();
    db = new SQL.Database(new Uint8Array(arrayBuffer));
}

// Usage with file input
document.getElementById('fileInput').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        await loadDatabaseFromFile(file);
        console.log('Database loaded!');
    }
});
```

## Use Cases

- Client-side data analysis
- Offline-first applications
- Data exploration tools
- CSV to SQLite converter
- Temporary query playground

## Performance

- Entire database runs in memory
- Fast queries on small to medium datasets
- Can handle databases up to ~100MB efficiently
- Persistence via localStorage or file download
