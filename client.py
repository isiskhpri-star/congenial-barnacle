"""
Multi-Device TCP Client

Connects to the Multi-Device Server, sends data, and listens for
messages from the server (including broadcasts from other devices).

Usage:
    python client.py [--host HOST] [--port PORT]

Once connected you can type messages in the terminal. They are sent
as newline-delimited JSON (or plain text) to the server.

Special commands:
    /json KEY VALUE   – send a JSON object {"KEY": "VALUE"}
    /quit             – disconnect
"""

import argparse
import asyncio
import json
import sys


async def read_server(reader: asyncio.StreamReader) -> None:
    """Continuously read and display messages from the server."""
    try:
        while True:
            raw = await reader.readline()
            if not raw:
                print("\n[client] Server closed the connection.")
                break
            msg = raw.decode().strip()
            try:
                parsed = json.loads(msg)
                print(f"\n<<< {json.dumps(parsed, indent=2)}")
            except json.JSONDecodeError:
                print(f"\n<<< {msg}")
            # Re-show the prompt
            print(">>> ", end="", flush=True)
    except asyncio.CancelledError:
        pass


async def run_client(host: str, port: int) -> None:
    reader, writer = await asyncio.open_connection(host, port)
    print(f"[client] Connected to {host}:{port}")

    # Start background task to print incoming messages
    recv_task = asyncio.create_task(read_server(reader))

    loop = asyncio.get_event_loop()
    try:
        while True:
            print(">>> ", end="", flush=True)
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            if line == "/quit":
                break

            # /json shortcut: /json temperature 22.5  ->  {"temperature": "22.5"}
            if line.startswith("/json "):
                parts = line.split(maxsplit=2)
                if len(parts) == 3:
                    payload = json.dumps({parts[1]: parts[2]})
                else:
                    print("[client] Usage: /json KEY VALUE")
                    continue
            else:
                # Send as a JSON object with a "data" key
                payload = json.dumps({"data": line})

            writer.write((payload + "\n").encode())
            await writer.drain()
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        recv_task.cancel()
        writer.close()
        await writer.wait_closed()
        print("[client] Disconnected.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Device TCP Client")
    parser.add_argument("--host", default="127.0.0.1", help="Server address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="Server port (default: 9000)")
    args = parser.parse_args()

    try:
        asyncio.run(run_client(args.host, args.port))
    except KeyboardInterrupt:
        print("\n[client] Interrupted.")


if __name__ == "__main__":
    main()
