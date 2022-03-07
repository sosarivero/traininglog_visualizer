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
    dataframe = pd.read_csv(
        user_file,
        # Strong uses ';' as a separator in their exported csv files, so the pandas read_csv function needs the argument.
        sep=";",
        # Select only the columns necessary for the visualization.
        usecols=["Date", "Exercise Name", "Weight", "Reps"],
    )

    # Gets the info from the lift by searching with the name.
    squat_info = dataframe.loc[dataframe["Exercise Name"] == "Squat (Barbell)"]
    # Creates a new column in which the one-rep max is calculated.
    squat_info["E1RM"] = squat_info["Weight"] / (1.0278 - 0.0278 * squat_info["Reps"])
    bench_info = dataframe.loc[dataframe["Exercise Name"] == "Bench Press (Barbell)"]
    deadlift_info = dataframe.loc[dataframe["Exercise Name"] == "Deadlift (Barbell)"]

    squat_info = squat_info.set_index("Date").to_dict()["E1RM"]

    output_dict = {}
    highest = 0

    for key, value in squat_info.items():
        if value > highest:
            output_dict[key] = int(value)
            highest = value

    st.write(output_dict)
