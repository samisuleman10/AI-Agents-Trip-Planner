from project_lib import (
    INCLIMATE_WEATHER_CONDITIONS,
    call_activities_api_mocked,
    call_weather_api_mocked,
)


def filter_activities_by_interests(activities, interests):
    return [
        activity
        for activity in activities
        if any(interest in activity["related_interests"] for interest in interests)
    ]


def filter_activities_by_weather(activities, weather_condition):
    if weather_condition not in INCLIMATE_WEATHER_CONDITIONS:
        return activities

    indoor_keywords = ["indoor", "indoors"]
    filtered = []

    for activity in activities:
        text = f"{activity['description']} {activity['location']}".lower()
        if any(keyword in text for keyword in indoor_keywords):
            filtered.append(activity)

    return filtered


def sort_activities(activities, interests):
    def score(activity):
        interest_score = sum(
            1 for interest in interests if interest in activity["related_interests"]
        )
        return (-interest_score, activity["price"], activity["start_time"])

    return sorted(activities, key=score)


def build_itinerary(selected_activities, weather):
    lines = []
    lines.append("Final Itinerary")
    lines.append("----------------")
    lines.append(
        f"Weather: {weather['condition'].title()}, {weather['temperature']}°{weather['temperature_unit'][0].upper()}"
    )
    lines.append("")

    total_cost = 0

    for index, activity in enumerate(selected_activities, start=1):
        lines.append(f"{index}. {activity['name']}")
        lines.append(f"   Time: {activity['start_time']} - {activity['end_time']}")
        lines.append(f"   Location: {activity['location']}")
        lines.append(f"   Price: €{activity['price']}")
        lines.append("")
        total_cost += activity["price"]

    lines.append(f"Total Cost: €{total_cost}")
    return "\n".join(lines)


def main():
    city = "AgentsVille"
    date = "2025-06-12"
    interests = ["technology", "movies", "music"]

    weather = call_weather_api_mocked(date, city)
    if not weather:
        print("No weather data found.")
        return

    activities = call_activities_api_mocked(date, city)
    if not activities:
        print("No activities found.")
        return

    matched_activities = filter_activities_by_interests(activities, interests)
    weather_filtered_activities = filter_activities_by_weather(
        matched_activities, weather["condition"]
    )
    selected_activities = sort_activities(weather_filtered_activities, interests)[:3]

    if not selected_activities:
        print("No suitable activities found after applying filters.")
        return

    itinerary = build_itinerary(selected_activities, weather)
    print(itinerary)


if __name__ == "__main__":
    main()