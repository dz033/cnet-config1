def argmax(S, weights, feature_functions):
    """
    Greedily select a feature using max(score function).

    Parameters:
    - S: Set of path specifications
    - weights: Dictionary mapping (d, P) to their respective weights
    - feature_functions: List of feature functions

    Returns:
    - Tuple (q, v) representing the selected feature function and feature value
    """
    max_score = float('-inf')
    selected_q = None
    selected_v = None

    for q in feature_functions:
        for spec_set in S:
            for v in spec_set:
                score = feature_score(S, weights, feature_functions, q, v)
                if score > max_score:
                    max_score = score
                    selected_q = q
                    selected_v = v

    return selected_q, selected_v

def feature_score(S, weights, feature_functions, q, v):
    """
    Calculate the feature score for a specific feature function and value.

    Parameters:
    - S: Set of path specifications
    - weights: Dictionary mapping (d, P) to their respective weights
    - feature_functions: List of feature functions
    - q: Selected feature function
    - v: Selected feature value

    Returns:
    - Feature score for the given feature function and value
    """
    score = 0

    for (d, P) in weights:
        path_weight = weights[(d, P)]
        for spec_set in S:
            if q in spec_set and v in spec_set:
                score += path_weight * sum(
                    1 for q in S if q in spec_set and (d, P) in S
                )

    return score

# Example usage
weights = {("d1", "P1"): 1, ("d2", "P2"): 2}
S_E = [{"NYe"}]
S_SP = [{"1sp"}]
S_E_SP = [{"NYe"}, {"LAe", "1sp"}]
feature_functions = [E, SP]

# Greedily select a feature
q, v = argmax(S_E_SP, weights, feature_functions)

# Print the selected feature and value
print("Selected feature function:", q)
print("Selected feature value:", v)
