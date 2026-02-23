# Multi-Device TCP Server

An asynchronous TCP server (Python 3.12+, no external dependencies) that lets multiple devices connect simultaneously and exchange data in real time.

## Features

- **Concurrent connections** – each device is handled in its own async task
- **Automatic device IDs** – every connection is assigned a unique `device-N` identifier
- **JSON messaging** – all messages are newline-delimited JSON
- **Broadcast** – data sent by one device is relayed to every other connected device
- **Acknowledgements** – the server confirms receipt of every message back to the sender
- **Join / leave notifications** – all devices are notified when a peer connects or disconnects

## Quick Start

### 1. Start the server

```bash
python server.py                # listens on 0.0.0.0:9000
python server.py --port 8888    # custom port
```

### 2. Connect one or more clients

Open separate terminals and run:

```bash
python client.py                        # connects to 127.0.0.1:9000
python client.py --host 192.168.1.10    # connect to a remote server
```

### 3. Send data

Type a message and press Enter. The server will:

1. Acknowledge the message back to you.
2. Broadcast it to every other connected device.

#### Special client commands

| Command | Description |
|---------|-------------|
| `/json KEY VALUE` | Send `{"KEY": "VALUE"}` as structured data |
| `/quit` | Disconnect gracefully |

## Protocol

All messages are **newline-delimited JSON** (`\n`-terminated).

### Server → Client message types

| `type` | When | Extra fields |
|--------|------|--------------|
| `welcome` | On connect | `device_id`, `message` |
| `ack` | After receiving data | `device_id`, `received` |
| `data` | Broadcast from another device | `from_device`, `payload` |
| `device_joined` | A new device connected | `device_id` |
| `device_left` | A device disconnected | `device_id` |

### Client → Server

Send any valid JSON object (or plain text) terminated by `\n`.

## Requirements

- Python 3.12 or later (uses only the standard library)
