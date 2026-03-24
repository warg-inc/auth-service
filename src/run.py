import asyncio
from setup.app_factory import AppFactory


async def main():
    grpc_server = AppFactory.create_grpc_server()

    await grpc_server.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())