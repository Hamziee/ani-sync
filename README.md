# ani-sync README

Welcome to **ani-sync**, the syncing tool I made to keep my anime watch progress consistent across devices. Honestly, this was a personal project that got slightly out of hand. Expect some rough edges, it’s not perfect, and I won’t pretend it is. 99% was ChatGPT's work. If it works for you, great! If not, well… it works on my machine

---

## Features

- **Sync Your Progress**: Keep track of what you’ve watched with ani-cli across your PC, phone or other devices (samsung smart fridge maybe?).
- **Cloud Storage**: Syncs progress to a remote server by default (`ani-sync.hamzie.site:25507`).
- **Arguments Compatibility**: Run `ani-sync` with the same arguments as `ani-cli` and more.
- **Open Source**: Both the client and server are open-source because trust matters.

---

## How It Works

ani-sync acts as a wrapper around ani-cli, handling syncing automatically before and after your anime sessions. By default, it uses `ani-sync.hamzie.site` to store and authenticate your data. The server saves your progress as plain text files, yes, I could *technically* read them, but I don’t care about your anime habits. You’ll just have to trust me the same way you trust big corporations. But I’ve got better things to do then look what episode you are at on Naruto. 

If you’re privacy-focused (for anime? really?), you can host your own server. Check out the server code here: [Hamziee/ani-sync-server](https://github.com/Hamziee/ani-sync-server). (don't expect anything good)


---

## Setup & Installation

### [easy method] PyPi:
```bash
pip install ani-sync
```

### [method 2] Clone and install:
```bash
git clone https://github.com/Hamziee/ani-sync.git
cd ani-sync
pip install .
```

### Requirements:
- **ani-cli** installed and in your PATH
- Python 3.x
- Git Bash (Windows users) (you should have this already if u installed ani-cli correctly, if not, then, okay, how are you using it???)

---

## Usage

**Basic Sync Flow:**

1. If you’ve been using ani-cli already, first upload your progress:
   ```bash
   ani-sync --- --upload
   ```
2. After that, just run:
   ```bash
   ani-sync
   ```
   It’ll handle syncing automatically.

**Commands:**

- **Register an account:**
  ```bash
  ani-sync --- --register
  ```
- **Log in:**
  ```bash
  ani-sync --- --login
  ```
- **Upload progress:** [!] This is done automatically after you finished watching and clicked quit in ani-cli
  ```bash
  ani-sync --- --upload
  ```
- **Download progress:** [!] This is done automatically when you start it
  ```bash
  ani-sync --- --download
  ```

**Passing Arguments:**

- Pass ani-cli arguments directly:
  ```bash
  ani-sync -c --dub
  ```
- Pass ani-sync arguments with `---`:
  ```bash
  ani-sync --- --upload
  ```

---

## FAQ

### Q: Is this stable?
A: Define stable

### Q: Can I trust this?
A: You trust big corporations with your data, don’t you? This is no different—just smaller scale and open source and anime which is not really personal data.

### Q: What if I don’t trust anyone?
A: Sure, grab the server code here: [Hamziee/ani-sync-server](https://github.com/Hamziee/ani-sync-server) and host it yourself, you got something to hide huh?

## Credits

- Me (Hamza) for duct-taping this together.
- ChatGPT working hard for 4 hours and getting working code after being yelled at (i said thank you at the very end)