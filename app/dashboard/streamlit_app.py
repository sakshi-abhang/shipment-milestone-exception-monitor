import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Shipment Monitor",
    page_icon="🚢",
    layout="wide"
)


st.title("Shipment Milestone & Exception Monitor")

st.write(
    "Monitor shipments, milestone events, delays, "
    "and operational exceptions."
)


try:
    shipments_response = requests.get(
        f"{API_BASE_URL}/shipments",
        timeout=5
    )

    exceptions_response = requests.get(
        f"{API_BASE_URL}/exceptions",
        timeout=5
    )

    shipments_response.raise_for_status()
    exceptions_response.raise_for_status()

    shipments = shipments_response.json()
    exceptions = exceptions_response.json()

except requests.RequestException as error:
    st.error(
        f"Unable to connect to the Shipment API: {error}"
    )

    st.stop()


total_shipments = len(shipments)

open_exceptions = [
    item
    for item in exceptions
    if not item["resolved"]
]

high_exceptions = [
    item
    for item in open_exceptions
    if item["severity"] in ["HIGH", "CRITICAL"]
]


column1, column2, column3 = st.columns(3)


with column1:
    st.metric(
        "Total Shipments",
        total_shipments
    )


with column2:
    st.metric(
        "Open Exceptions",
        len(open_exceptions)
    )


with column3:
    st.metric(
        "High/Critical",
        len(high_exceptions)
    )


st.subheader("Shipments")

st.subheader("Shipment Details")


shipment_ids = [
    shipment["shipment_id"]
    for shipment in shipments
]


selected_shipment_id = st.selectbox(
    "Select Shipment",
    shipment_ids
)

selected_shipment = next(
    shipment
    for shipment in shipments
    if shipment["shipment_id"] == selected_shipment_id
)
st.subheader("Filters")

detail_column1, detail_column2, detail_column3 = st.columns(3)


with detail_column1:
    st.write("**Origin**")
    st.write(selected_shipment["origin"])


with detail_column2:
    st.write("**Destination**")
    st.write(selected_shipment["destination"])


with detail_column3:
    st.write("**Status**")
    st.write(selected_shipment["status"])
    
st.write("**Container Number**")

st.write(
    selected_shipment["container_number"]
)


st.write("**Booking Number**")

st.write(
    selected_shipment["booking_number"]
)

st.subheader("Milestone Timeline")


try:
    events_response = requests.get(
        f"{API_BASE_URL}/shipments/"
        f"{selected_shipment_id}/events",
        timeout=5
    )

    events_response.raise_for_status()

    shipment_events = events_response.json()

except requests.RequestException as error:
    shipment_events = []

    st.error(
        f"Unable to load shipment events: {error}"
    )
    
if shipment_events:

    for event in shipment_events:

        st.write(
            f"### {event['event_type']}"
        )

        st.write(
            f"Location: {event['location']}"
        )

        st.write(
            f"Time: {event['event_time']}"
        )

        if event["description"]:
            st.write(
                event["description"]
            )

        st.divider()

else:
    st.info(
        "No milestone events available for this shipment."
    )
    
statuses = sorted(
    set(
        shipment["status"]
        for shipment in shipments
    )
)

origins = sorted(
    set(
        shipment["origin"]
        for shipment in shipments
    )
)

destinations = sorted(
    set(
        shipment["destination"]
        for shipment in shipments
    )
)


filter_column1, filter_column2, filter_column3 = st.columns(3)


with filter_column1:
    selected_status = st.selectbox(
        "Status",
        ["All"] + statuses
    )


with filter_column2:
    selected_origin = st.selectbox(
        "Origin",
        ["All"] + origins
    )


with filter_column3:
    selected_destination = st.selectbox(
        "Destination",
        ["All"] + destinations
    )
    
filtered_shipments = shipments


if selected_status != "All":
    filtered_shipments = [
        shipment
        for shipment in filtered_shipments
        if shipment["status"] == selected_status
    ]


if selected_origin != "All":
    filtered_shipments = [
        shipment
        for shipment in filtered_shipments
        if shipment["origin"] == selected_origin
    ]


if selected_destination != "All":
    filtered_shipments = [
        shipment
        for shipment in filtered_shipments
        if shipment["destination"] == selected_destination
    ]
       
if filtered_shipments:
    st.dataframe(
        filtered_shipments,
        width="stretch"
    )
else:
    st.info("No shipments match the selected filters.")

st.subheader("Shipments")

if filtered_shipments:
    st.dataframe(
        filtered_shipments,
        width="stretch"
    )
else:
    st.info(
        "No shipments match the selected filters."
    )


st.subheader("Operational Exceptions")
st.subheader("Exception Filter")


selected_severity = st.selectbox(
    "Severity",
    [
        "All",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]
)


filtered_exceptions = exceptions


if selected_severity != "All":
    filtered_exceptions = [
        exception
        for exception in exceptions
        if exception["severity"] == selected_severity
    ]
    
if filtered_exceptions:
    st.dataframe(
        filtered_exceptions,
        use_container_width=True
    )
else:
    st.info(
        "No exceptions match the selected severity."
    )