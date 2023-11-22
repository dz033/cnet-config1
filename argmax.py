def argmax(feature_score, R, Q):
  max_score = float('-inf')
  selected_path = None
  selected_feature = None
  
  for path in R:
    for feature_function in Q:
      score = feature_score(path, feature_function)
      if score > max_score: 
        max_score = score    
        selected_path = path
        selected_feature = feature_function
        return selected_feature, selected_path
