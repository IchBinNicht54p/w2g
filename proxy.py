import asyncio
import websockets

WS_HOST = "192.168.101.104"
WS_PORT = 25567

TCP_HOST = "192.168.101.104"
TCP_PORT = 25565


async def bridge_ws_to_tcp(ws):
    print(f"Client connected via WebSocket from {ws.remote_address}")

    try:
        reader, writer = await asyncio.open_connection(TCP_HOST, TCP_PORT)
    except Exception as e:
        print(f"Failed to connect to TCP server at {TCP_HOST}:{TCP_PORT}: {e}")

        await ws.close()
        return

    async def ws_to_tcp():
        try:
            async for message in ws:
                if isinstance(message, str):
                    payload = message.encode("utf-8")

                else:
                    payload = message

                writer.write(payload)
                await writer.drain()
        except:
            pass

    async def tcp_to_ws():
        try:
            while True:
                data = await reader.read(4096)

                if not data:
                    break

                try:
                    await ws.send(data.decode("utf-8"))
                except UnicodeDecodeError:
                    await ws.send(data)

        except:
            pass

    try:
        await asyncio.gather(ws_to_tcp(), tcp_to_ws())
    finally:
        print(f"Closing connection for {ws.remote_address}")

        writer.close()
        await writer.wait_closed()


async def main():
    server = await websockets.serve(bridge_ws_to_tcp, WS_HOST, WS_PORT)

    print(
        f"WS-to-TCP Proxy running on ws://{WS_HOST}:{WS_PORT} -> "
        f"tcp://{TCP_HOST}:{TCP_PORT}"
    )

    await server.wait_closed()
