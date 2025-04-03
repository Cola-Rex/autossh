# autossh

**autossh** is a lightweight, auto-reconnect wrapper around `ssh` that keeps your SSH tunnels alive even if the connection drops. Think of it as a minimal, modern alternative to the traditional `autossh` tool, written in Python and easy to install.

---

## 🚀 One-line install

```bash
curl -fsSL https://raw.githubusercontent.com/Cola-Rex/autossh/main/install.sh | bash
```

This will download the latest prebuilt binary from the GitHub release and install it to `/usr/local/bin/autossh`.

---

## 🧪 Usage

```bash
autossh -L 5433:remote-host:5432 user@remote-host
```

This works exactly like `ssh`, but `autossh` will:

- Automatically restart the tunnel if the connection drops
- Send regular heartbeats with `ServerAliveInterval=5` and `ServerAliveCountMax=3`

Fully compatible with all standard `ssh` arguments.

---

## ❌ Uninstall

To uninstall autossh, just remove the installed binary:

```bash
sudo rm /usr/local/bin/autossh
```

---

## 🛠 Local Development

If you want to build from source:

### 1. Clone and install dependencies:

```bash
git clone https://github.com/Cola-Rex/autossh.git
cd autossh
pip install pyinstaller
```

### 2. Build a single-file binary:

```bash
./build.sh
```

The binary will be located in `dist/autossh`.

---

## 📄 License

[Apache License, Version 2.0](LICENSE)

---

Made with ☕ by [Cola-Rex](https://github.com/Cola-Rex)
