def feature_score(S, weights, feature_function):
    """
    Calculate the feature score for a set of specifications.

    Parameters:
    - S: Set of path specifications
    - weights: Dictionary mapping (d, P) to their respective weights
    - feature_function: Function representing the feature function (e.g., E, SP)

    Returns:
    - Feature score for the given set of specifications
    """
    score = 0

    for (d, P) in weights:
        path_weight = weights[(d, P)]
        for spec_set in S:
            if feature_function(d, P) in spec_set:
                score += path_weight * sum(
                    1 for q in S if feature_function(d, P) in q and (d, P) in S
                )

    return score


# Example feature functions (replace with actual feature functions)
def E(d, P):
    # Replace with your actual E feature function
    return "NYe" if d == "d1" else "LAe"


def SP(d, P):
    # Replace with your actual SP feature function
    return "1sp" if P == "P1" else "1sp"


# Example usage
weights = {("d1", "P1"): 1, ("d2", "P2"): 2}
S_E = [{"NYe"}]
S_SP = [{"1sp"}]
S_E_SP = [{"NYe"}, {"LAe", "1sp"}]

# Calculate feature scores
score_E = feature_score(S_E, weights, E)
score_SP = feature_score(S_SP, weights, SP)
score_E_SP = feature_score(S_E_SP, weights, lambda d, P: E(d, P) + SP(d, P))

# Print the results
print("Feature score for E:", score_E)
print("Feature score for SP:", score_SP)
print("Feature score for E and SP:", score_E_SP)
