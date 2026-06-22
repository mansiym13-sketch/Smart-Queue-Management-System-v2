import pandas as pd


STATUS_OPTIONS = [
    "WAITING",
    "CALLED",
    "SERVING",
    "COMPLETED"
]

QUEUE_STATUS_OPTIONS = [
    "ACTIVE",
    "INACTIVE"
]


def priority_label(priority_level):
    labels = {
        3: "High",
        2: "Medium",
        1: "Low"
    }

    return labels.get(priority_level, "Low")


def priority_value(priority_label_text):
    values = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    return values.get(priority_label_text, 1)


def queue_label(queue):
    if queue.get("id") is None:
        return queue.get("name", "All Queues")

    return f"{queue.get('name', 'Queue')} (ID {queue.get('id')})"


def token_label(token):
    return f"{token.get('token_number')} (ID {token.get('id')})"


def build_token_dataframe(tokens, queues=None, users=None):
    queue_map = {
        queue.get("id"): queue
        for queue in queues or []
    }

    user_map = {
        user.get("id"): user
        for user in users or []
    }

    rows = []

    for token in tokens or []:
        queue = queue_map.get(token.get("queue_id"), {})
        user = user_map.get(token.get("user_id"), {})

        rows.append(
            {
                "ID": token.get("id"),
                "Token": token.get("token_number"),
                "Customer": user.get("username") or user.get("email") or token.get("user_id"),
                "Queue": queue.get("name") or token.get("queue_id"),
                "Priority": priority_label(token.get("priority_level")),
                "Status": token.get("status")
            }
        )

    return pd.DataFrame(rows)


def queue_summary_dataframe(tokens, queues):
    rows = []

    for queue in queues or []:
        queue_tokens = [
            token
            for token in tokens or []
            if token.get("queue_id") == queue.get("id")
        ]

        rows.append(
            {
                "Queue": queue.get("name"),
                "Waiting": sum(1 for token in queue_tokens if token.get("status") == "WAITING"),
                "Called": sum(1 for token in queue_tokens if token.get("status") == "CALLED"),
                "Serving": sum(1 for token in queue_tokens if token.get("status") == "SERVING"),
                "Completed": sum(1 for token in queue_tokens if token.get("status") == "COMPLETED"),
                "Total": len(queue_tokens)
            }
        )

    return pd.DataFrame(rows)


def show_api_error(st, result, fallback="Request failed"):
    if isinstance(result, dict) and result.get("error"):
        st.error(result.get("error") or fallback)
        return True

    return False
