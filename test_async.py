import asyncio

async def main():
    with open("async_test.log", "w") as f:
        f.write("Asyncio start\n")
        await asyncio.sleep(1)
        f.write("Asyncio end\n")

if __name__ == "__main__":
    asyncio.run(main())
