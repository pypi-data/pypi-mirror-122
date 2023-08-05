from lib.aws_utils import get_event_bridge_client


def _get_client():
    return get_event_bridge_client()


def publish_event(source, event_bus_name, event_bus_arn, event_type, event_context):
    client = _get_client()
    return client.put_events(
        Entries=[
            {
                "Source": source,
                "EventBusName": event_bus_name,
                "Resources": [
                    event_bus_arn
                ],
                "DetailType": event_type,
                "Detail": event_context,
            }

        ]
    )
