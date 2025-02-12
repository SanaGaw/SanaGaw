# strategies/strategies.py

def pragmatic_strategy(bureaucrats, institution_ic):
    """
    1. Investigate bureaucrats below satisfaction targets (not explicitly modeled here),
       so we can approximate by investigating the top few who have the lowest token count.
    2. Then prioritize high-token confiscation (meaning investigate those with a lot of tokens?).
    This is a simplified placeholder.
    """
    # Sort by tokens in descending order, and pick a subset
    # For demonstration, pick top 3 earners to investigate, if IC allows
    sorted_b = sorted(bureaucrats, key=lambda x: x.tokens, reverse=True)
    return sorted_b[:3]  # investigate top 3

def corruption_minimizing_strategy(bureaucrats, institution_ic):
    """
    Investigate all bureaucrats whose bribe acceptance rate (not fully tracked here) 
    is > 10%. We'll approximate using is_corrupt == True.
    """
    # Investigate all that are corrupt
    to_investigate = [b for b in bureaucrats if b.is_corrupt]
    return to_investigate

def firefighting_strategy(bureaucrats, institution_ic):
    """
    Investigate only if IC < 0.4 or corruption > 30%. 
    We'll approximate corruption > 30% by checking how many are corrupt in the list.
    """
    corrupt_count = sum(1 for b in bureaucrats if b.is_corrupt)
    total = len(bureaucrats)
    if total > 0:
        corruption_rate = corrupt_count / total
    else:
        corruption_rate = 0.0

    if institution_ic < 0.4 or corruption_rate > 0.3:
        # Investigate a random subset or a minimal subset
        return [b for b in bureaucrats if b.is_corrupt]
    else:
        # Otherwise, do nothing (save tokens)
        return []
