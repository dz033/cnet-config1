def argmax(feature_score, R, Q):
    # Initialize variables to keep track of the maximum score, selected path, and selected feature
    max_score = float('-inf')
    selected_path = None
    selected_feature = None

    # Loop through each path in the set of routing paths (R)
    for path in R:
        # Loop through each feature function in the set of feature functions (Q)
        for feature_function in Q:
            # Calculate the score for the current path and feature function
            score = feature_score(path, feature_function)

            # Check if the calculated score is greater than the current maximum score
            if score > max_score:
                # If so, update the maximum score, selected path, and selected feature
                max_score = score
                selected_path = path
                selected_feature = feature_function

    # Return the selected feature and path with the highest score
    return selected_feature, selected_path
