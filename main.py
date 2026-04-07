from project_lib import call_weather_api_mocked, call_activities_api_mocked


def main():

    city = "Berlin"
    date = "2025-06-10"

    # Step 1: Get weather data
    weather = call_weather_api_mocked(date, city)

    # Step 2: Get activities
    activities = call_activities_api_mocked(date, city)

    # Print results
    print("=== Travel Planner ===\n")

    print(f"City: {city}")
    print(f"Date: {date}\n")

    print("Weather:")
    print(weather)

    print("\nAvailable Activities:")
    for activity in activities:
        print(f"- {activity['name']} ({activity['category']})")


if __name__ == "__main__":
    main()