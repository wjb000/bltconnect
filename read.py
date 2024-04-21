import asyncio
from bleak import BleakClient

async def notification_handler(sender, data):
    print(f"Notification from {sender}: {data.hex()}")

async def run(address):
    async with BleakClient(address) as client:
        print(f"Connected to {address}")

        services = client.services
        for service in services:
            print(f"Service {service.uuid}: {service.description}")
            for char in service.characteristics:
                print(f"  Characteristic {char.uuid}: Properties: {char.properties}")
                

                if "notify" in char.properties:
                    await client.start_notify(char.uuid, notification_handler)
                    print(f"Subscribed to {char.uuid}. Waiting for data...")
                    await asyncio.sleep(30) 
                    await client.stop_notify(char.uuid)
                    print(f"Unsubscribed from {char.uuid}.")

                if "read" in char.properties:
                    value = await client.read_gatt_char(char.uuid)
                    print(f"Read from {char.uuid}: {value}")

address = "a0:a0:aa:00:a0:aa"
loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
