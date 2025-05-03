def format_personality_traits(traits: list):
    return ", ".join(traits)


def summarize_personality(personality: dict):
    return (
        f"{personality.get('tone', 'neutral')}, "
        f"{personality.get('energy', 'medium')} energy, "
        f"interests: {personality.get('interests', 'general curiosity')}"
    )
