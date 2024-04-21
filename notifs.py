import asyncio
from bleak import BleakClient


async def run(address, service_uuid, characteristic_uuid):
    async with BleakClient(address) as client:
        await client.connect()

        for service in client.services:
            print(f"Service {service.uuid}")
            for char in service.characteristics:
                print(f"    Characteristic {char.uuid}")

        def notification_handler(sender, data):
            print(f"Received data from {sender}: {data}")

        await client.start_notify(characteristic_uuid, notification_handler)

        await asyncio.sleep(30)  
        await client.stop_notify(characteristic_uuid)


service_uuid = "00000000-0000-0000-0000-000000000000"
characteristic_uuid = "00000000-6900-0000-0000-000000000000"


address = "a0:a0:aa:00:a0:aa"

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, service_uuid, characteristic_uuid))
