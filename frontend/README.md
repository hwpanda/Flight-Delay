# React frontend

This Vite + React + TypeScript application owns the browser experience. Flask
continues to own prediction and data APIs.

## Development

In one terminal, run Flask on port 5000:

```bash
./venv/bin/python app.py
```

In another, run Vite. It proxies `/api` requests to Flask:

```bash
cd frontend
npm install
npm run dev
```

## Production build

```bash
cd frontend
npm run build
```

The production bundle is written to `static/react/`, which Flask serves at `/`.
