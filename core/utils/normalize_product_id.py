def normalize_product_id(raw: str) -> str:
    """Канонический product_id: 'Carrot Item ' → 'CARROT_ITEM'."""
    if not isinstance(raw, str):
        return ""
    return raw.strip().upper().replace(' ', '_')