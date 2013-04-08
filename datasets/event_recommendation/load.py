def get_user_events_dict(df):
    user_events_dict = {user: [] for user in df["user"]}

    for i, row in df.iterrows():
        user_events_dict[row["user"]].append(row["event"])

    return user_events_dict
