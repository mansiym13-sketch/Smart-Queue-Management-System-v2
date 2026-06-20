from api import create_queue, get_queues

print(
    create_queue(
        "Hospital Queue",
        "OPD Consultation"
    )
)

print(get_queues())