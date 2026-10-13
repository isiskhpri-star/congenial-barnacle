"""
Multi-Device TCP Server

An asynchronous TCP server that accepts connections from multiple devices
simultaneously. Each device can send data which is logged, broadcast to
all other connected devices, and acknowledged back to the sender.

Usage:
    python server.py [--host HOST] [--port PORT]

Default: listens on 0.0.0.0:9000
"""

import argparse
import asyncio
import json
import logging
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("multi_device_server")


class DeviceServer:
    """Manages multiple device connections and message routing."""

    def __init__(self, host: str = "0.0.0.0", port: int = 9000):
        self.host = host
        self.port = port
        # device_id -> (reader, writer)
        self.devices: dict[str, asyncio.StreamWriter] = {}
        self._device_counter = 0
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    async def _register(self, writer: asyncio.StreamWriter) -> str:
        """Assign a unique device ID and store the writer."""
        async with self._lock:
            self._device_counter += 1
            device_id = f"device-{self._device_counter}"
            self.devices[device_id] = writer
        addr = writer.get_extra_info("peername")
        logger.info("Device connected: %s from %s  (total: %d)", device_id, addr, len(self.devices))
        return device_id

    async def _unregister(self, device_id: str) -> None:
        async with self._lock:
            writer = self.devices.pop(device_id, None)
        if writer and not writer.is_closing():
            writer.close()
            await writer.wait_closed()
        logger.info("Device disconnected: %s  (total: %d)", device_id, len(self.devices))

    # ------------------------------------------------------------------
    # Messaging
    # ------------------------------------------------------------------

    async def _send(self, writer: asyncio.StreamWriter, payload: dict) -> None:
        """Send a JSON-encoded message terminated by a newline."""
        data = json.dumps(payload) + "\n"
        writer.write(data.encode())
        await writer.drain()

    async def _broadcast(self, message: dict, exclude: str | None = None) -> None:
        """Send a message to every connected device except *exclude*."""
        async with self._lock:
            targets = {did: w for did, w in self.devices.items() if did != exclude}
        for did, writer in targets.items():
            try:
                await self._send(writer, message)
            except (ConnectionError, OSError):
                logger.warning("Failed to send to %s – will be cleaned up", did)

    # ------------------------------------------------------------------
    # Client handler
    # ------------------------------------------------------------------

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        device_id = await self._register(writer)

        # Send a welcome message with the assigned device ID
        await self._send(writer, {
            "type": "welcome",
            "device_id": device_id,
            "message": "Connected to Multi-Device Server",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # Notify other devices
        await self._broadcast(
            {"type": "device_joined", "device_id": device_id,
             "timestamp": datetime.now(timezone.utc).isoformat()},
            exclude=device_id,
        )

        try:
            while True:
                raw = await reader.readline()
                if not raw:
                    break  # client disconnected

                line = raw.decode().strip()
                if not line:
                    continue

                # Try to parse as JSON; fall back to plain text
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    payload = {"data": line}

                logger.info("[%s] data received: %s", device_id, payload)

                # Acknowledge receipt to sender
                await self._send(writer, {
                    "type": "ack",
                    "device_id": device_id,
                    "received": payload,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

                # Broadcast to other devices
                await self._broadcast(
                    {
                        "type": "data",
                        "from_device": device_id,
                        "payload": payload,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                    exclude=device_id,
                )
        except (ConnectionError, asyncio.IncompleteReadError):
            pass
        finally:
            await self._broadcast(
                {"type": "device_left", "device_id": device_id,
                 "timestamp": datetime.now(timezone.utc).isoformat()},
                exclude=device_id,
            )
            await self._unregister(device_id)

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    async def start(self) -> None:
        server = await asyncio.start_server(
            self._handle_client, self.host, self.port
        )
        addrs = ", ".join(str(s.getsockname()) for s in server.sockets)
        logger.info("Multi-Device Server listening on %s", addrs)

        async with server:
            await server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Device TCP Server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=9000, help="Bind port (default: 9000)")
    args = parser.parse_args()

    server = DeviceServer(host=args.host, port=args.port)
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("Server shut down.")


if __name__ == "__main__":
    main()
