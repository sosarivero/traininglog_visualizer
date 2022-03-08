import streamlit as st
import pandas as pd


st.write("# Simple lift history visualization app.")

user_file = st.file_uploader(label="Import your Strong.app data.", type=["csv"])

if user_file is not None:
    df = pd.read_csv(
        user_file,
        # Strong uses ';' as a separator in their exported csv files, so the pandas read_csv function needs the argument.
        sep=";",
        # Select only the columns necessary for the visualization.
        usecols=["Date", "Exercise Name", "Weight", "Reps"],
        parse_dates=["Date"],
    )
    # Adds an E1RM to the df.
    df["E1RM"] = df["Weight"] / (1.0278 - 0.0278 * df["Reps"])

    # Reformats the date by deleting the hour timestamp.
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df = df.sort_values("E1RM", ascending=False).drop_duplicates("Date")
    df = df.sort_values("Date")
    df = df.set_index("Date")

    # Get a set of all the exercise names in the df.
    exercises = set(df["Exercise Name"])
    # Dropdown menus to choose which exercises to analyze
    exercise_one = st.selectbox("Select the exercise to show", exercises)

    # Gets the info from the lift by searching with the name.
    squat_info = df.loc[df["Exercise Name"] == exercise_one]

    squat_dict = squat_info["E1RM"].to_dict()
    highest = 0
    pr_dict = {}
    for date, weight in squat_dict.items():
        weight = int(weight)
        if weight > highest:
            highest = weight
            pr_dict[date] = weight

    personal_bests = pd.DataFrame.from_dict(pr_dict, orient="index")

    col1, col2 = st.columns(2)
    st.write("## Line chart of performances.")
    st.line_chart(squat_info["E1RM"])
    st.write("## History of personal bests.")
    st.bar_chart(personal_bests)
