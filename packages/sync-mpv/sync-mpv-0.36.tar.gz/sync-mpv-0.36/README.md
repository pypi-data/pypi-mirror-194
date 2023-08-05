## sync-mpv

Host a server and watch any youtube-dl compatible video in synchronization with connecting clients
utilizing the mpv player.

AES-encrypted server <-> client transport.  

### Installation

If **"~/.local/bin/"** is not inside your PATH, install mpv-sync with sudo privileges.
> sudo pip install sync-mpv

### Dependencies
- mpv
- pycryptodome  
- python-mpv-jsonipc

### Usage  
#### Server
For your server to receive and send messages you'll have to open TCP port *51984*.  

On first start of **"sync-mpv-server"**, you'll be asked to decide for a 16-digit long password.  
The clients will have to enter the same password when prompted.

Password will be written to **"~/.config/sync-mpv/serverpassword.conf"** 

#### Client

On first start of **"sync-mpv-client"**, you'll be asked to specify  your username and the IP and password of the server.  
A config file will be created in **"~/.config/sync-mpv/mpv-sync.conf"**

Press Space to toggle play/pause.





