import streamlit as st
import pandas as pd
import altair as alt


st.write(
    """
# Simple lift history visualization app.
"""
)

user_file = st.file_uploader(label="Import your Strong.app data.", type=["csv"])

if user_file is not None:
    df = pd.read_csv(
        user_file,
        # Strong uses ';' as a separator in their exported csv files, so the pandas read_csv function needs the argument.
        sep=";",
        # Select only the columns necessary for the visualization.
        usecols=["Date", "Exercise Name", "Weight", "Reps"],
    )
    # Adds an E1RM to the df.
    df["E1RM"] = df["Weight"] / (1.0278 - 0.0278 * df["Reps"])

    # Reformats the date by deleting the hour timestamp.
    for date in df["Date"]:
        splitted = date.split(" ")
        df["Date"] = splitted[0]

    # Get a set of all the exercise names in the df.
    exercises = set(df["Exercise Name"])
    # Dropdown menus to choose which exercises to analyze
    exercise_one = st.selectbox("Select your primary Squat", exercises)
    exercise_two = st.selectbox("Select your primary Bench Press", exercises)
    exercise_three = st.selectbox("Select your primary Deadlift", exercises)

    # Gets the info from the lift by searching with the name.
    squat_info = df.loc[df["Exercise Name"] == exercise_one]
    # Creates a new column in which the one-rep max is calculated.
    bench_info = df.loc[df["Exercise Name"] == "Bench Press (Barbell)"]
    deadlift_info = df.loc[df["Exercise Name"] == "Deadlift (Barbell)"]

    squat_info = squat_info.set_index("Date").to_dict()["E1RM"]

    output_dict = {}
    highest = 0

    for key, value in squat_info.items():
        if value > highest:
            output_dict[key] = int(value)
            highest = value

    st.write(output_dict)
