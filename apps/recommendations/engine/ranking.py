def rank_recommendations(scored_items, top_n=15):
    scored_items.sort(key=lambda x: x['scores']['final_score'], reverse=True)
    
    ranked_results = []
    for idx, item in enumerate(scored_items[:top_n], start=1):
        item['rank'] = idx
        ranked_results.append(item)

    return ranked_results
