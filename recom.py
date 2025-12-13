# do the recommendation from here
def final_emotion(emo):
    # Persist the detected emotion so other processes can read it.
    with open("output", "w") as f:
        f.write(emo)
