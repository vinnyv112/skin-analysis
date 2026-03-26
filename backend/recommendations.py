# Product recommendations database with ALL combinations
PRODUCTS = {
    # ===== OILY SKIN =====
    "oily_acne": {
        "cleanser": "Salicylic Acid Cleanser (2%) - Controls oil and treats acne",
        "toner": "Niacinamide Toner - Reduces oil production",
        "serum": "Salicylic Acid Serum - Targets acne",
        "moisturizer": "Oil-free Gel Moisturizer - Lightweight hydration",
        "sunscreen": "Mattifying Sunscreen SPF 50 - Oil control",
        "treatment": "Benzoyl Peroxide Spot Treatment - For active acne",
        "mask": "Clay Mask with Salicylic Acid - Use twice a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Treatment → Moisturizer\nWeekly: Clay Mask 2x week"
    },
    
    "oily_pores": {
        "cleanser": "Salicylic Acid Cleanser - Unclogs pores",
        "toner": "Niacinamide Toner - Minimizes pores",
        "serum": "Niacinamide Serum - Tightens pores",
        "moisturizer": "Oil-free Gel Moisturizer",
        "sunscreen": "Mattifying Sunscreen SPF 50",
        "mask": "Charcoal Clay Mask - Use twice a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Moisturizer\nWeekly: Charcoal Mask 2x week"
    },
    
    "oily_pigmentation": {
        "cleanser": "Gentle Salicylic Acid Cleanser",
        "toner": "Niacinamide Toner",
        "serum": "Vitamin C Serum - Brightens dark spots",
        "moisturizer": "Oil-free Gel Moisturizer",
        "sunscreen": "SPF 50 PA++++ Sunscreen - Must for pigmentation",
        "treatment": "Alpha Arbutin Serum - Targets dark spots",
        "mask": "Brightening Vitamin C Mask - Use once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Alpha Arbutin → Moisturizer\nWeekly: Brightening Mask 1x week"
    },
    
    "oily_clear": {
        "cleanser": "Gentle Foaming Cleanser - Maintains oil balance",
        "toner": "Niacinamide Toner",
        "serum": "Lightweight Hydrating Serum",
        "moisturizer": "Oil-free Gel Moisturizer",
        "sunscreen": "Mattifying Sunscreen SPF 50",
        "mask": "Hydrating Gel Mask - Use once a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Moisturizer\nWeekly: Hydrating Mask 1x week"
    },
    
    # OILY SKIN - COMBINATIONS
    "oily_acne_pores": {
        "cleanser": "Salicylic Acid Cleanser (2%) - Unclogs pores and treats acne",
        "toner": "Niacinamide Toner - Controls oil and minimizes pores",
        "serum": "Niacinamide + Salicylic Acid Serum - Targets both concerns",
        "moisturizer": "Oil-free Gel Moisturizer",
        "sunscreen": "Mattifying Sunscreen SPF 50",
        "treatment": "Spot treatment for active acne",
        "mask": "Clay Mask with Salicylic Acid - Use twice a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Treatment → Moisturizer\nWeekly: Clay Mask 2x week"
    },
    
    "oily_acne_pigmentation": {
        "cleanser": "Gentle Salicylic Acid Cleanser",
        "toner": "Niacinamide Toner",
        "serum": "Vitamin C Serum (AM) / Salicylic Acid (PM) - Alternate",
        "moisturizer": "Oil-free Gel Moisturizer",
        "sunscreen": "SPF 50 PA++++ Sunscreen - ABSOLUTELY MUST",
        "treatment": "Alpha Arbutin at night for pigmentation",
        "mask": "Brightening Clay Mask - Use twice a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Salicylic Acid → Alpha Arbutin → Moisturizer\nWeekly: Brightening Mask 2x week"
    },
    
    "oily_pores_pigmentation": {
        "cleanser": "Salicylic Acid Cleanser",
        "toner": "Niacinamide Toner",
        "serum": "Vitamin C (AM) / Niacinamide (PM)",
        "moisturizer": "Oil-free Gel Moisturizer",
        "sunscreen": "SPF 50 PA++++ Sunscreen",
        "treatment": "Alpha Arbutin for pigmentation",
        "mask": "Brightening Clay Mask - Twice a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Niacinamide → Alpha Arbutin → Moisturizer\nWeekly: Brightening Clay Mask 2x week"
    },
    
    "oily_acne_pores_pigmentation": {
        "cleanser": "Salicylic Acid Cleanser with gentle formula",
        "toner": "Niacinamide + PHA Toner - Multi-tasking",
        "serum": "Alternate: Vitamin C (AM), Niacinamide (PM), Salicylic Acid (PM on alternate days)",
        "moisturizer": "Oil-free Gel Moisturizer",
        "sunscreen": "SPF 50 PA++++ Sunscreen - NON-NEGOTIABLE",
        "treatment": "Alpha Arbutin for pigmentation, Spot treatment for acne",
        "mask": "Multi-action Clay Mask - Use twice a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM1: Cleanser → Toner → Salicylic Acid → Moisturizer\nPM2: Cleanser → Toner → Niacinamide → Alpha Arbutin → Moisturizer\nWeekly: Multi-action Mask 2x week"
    },
    
    # ===== DRY SKIN =====
    "dry_acne": {
        "cleanser": "Creamy Hydrating Cleanser - Non-stripping",
        "toner": "Hydrating Toner with Hyaluronic Acid",
        "serum": "Gentle Salicylic Acid Serum (0.5%) - Low concentration",
        "moisturizer": "Rich Ceramide Moisturizer",
        "sunscreen": "Hydrating Sunscreen SPF 50",
        "treatment": "Spot treatment (only on pimples)",
        "mask": "Hydrating Sheet Mask - Use once a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Treatment → Rich Moisturizer\nWeekly: Hydrating Mask 1x week"
    },
    
    "dry_pores": {
        "cleanser": "Creamy Cleanser",
        "toner": "Hydrating Toner",
        "serum": "Niacinamide Serum - Balances skin",
        "moisturizer": "Rich Ceramide Moisturizer",
        "sunscreen": "Hydrating Sunscreen SPF 50",
        "mask": "Gentle Clay Mask - Use once a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Moisturizer\nWeekly: Gentle Clay Mask 1x week"
    },
    
    "dry_pigmentation": {
        "cleanser": "Creamy Hydrating Cleanser",
        "toner": "Hydrating Toner",
        "serum": "Vitamin C + Hyaluronic Acid Serum",
        "moisturizer": "Rich Ceramide Moisturizer",
        "sunscreen": "Hydrating Sunscreen SPF 50 PA++++",
        "treatment": "Kojic Acid Cream - Night time",
        "mask": "Brightening Sheet Mask - Use once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Kojic Acid → Rich Moisturizer\nWeekly: Brightening Mask 1x week"
    },
    
    "dry_clear": {
        "cleanser": "Creamy Hydrating Cleanser",
        "toner": "Hydrating Toner",
        "serum": "Hyaluronic Acid Serum",
        "moisturizer": "Rich Ceramide Moisturizer",
        "sunscreen": "Hydrating Sunscreen SPF 50",
        "mask": "Hydrating Sheet Mask - Use once a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Moisturizer\nWeekly: Hydrating Mask 1x week"
    },
    
    # DRY SKIN - COMBINATIONS
    "dry_acne_pores": {
        "cleanser": "Creamy Cleanser with mild Salicylic Acid",
        "toner": "Hydrating Toner with Niacinamide",
        "serum": "Niacinamide Serum - Balances concerns",
        "moisturizer": "Rich Ceramide Moisturizer",
        "sunscreen": "Hydrating Sunscreen SPF 50",
        "treatment": "Spot treatment for acne (use only on spots)",
        "mask": "Gentle Clay Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Treatment → Moisturizer\nWeekly: Gentle Clay Mask 1x week"
    },
    
    "dry_acne_pigmentation": {
        "cleanser": "Creamy Hydrating Cleanser",
        "toner": "Hydrating Toner",
        "serum": "Vitamin C (AM) / Gentle Salicylic (PM) - Alternate",
        "moisturizer": "Rich Ceramide Moisturizer",
        "sunscreen": "Hydrating SPF 50 PA++++",
        "treatment": "Kojic Acid for pigmentation (night)",
        "mask": "Brightening + Hydrating Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Gentle Salicylic → Kojic Acid → Moisturizer\nWeekly: Brightening Mask 1x week"
    },
    
    "dry_pores_pigmentation": {
        "cleanser": "Creamy Cleanser",
        "toner": "Hydrating Toner with Niacinamide",
        "serum": "Vitamin C (AM) / Niacinamide (PM)",
        "moisturizer": "Rich Ceramide Moisturizer",
        "sunscreen": "Hydrating SPF 50 PA++++",
        "treatment": "Alpha Arbutin for pigmentation",
        "mask": "Brightening Sheet Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Niacinamide → Alpha Arbutin → Moisturizer\nWeekly: Brightening Mask 1x week"
    },
    
    # ===== NORMAL SKIN =====
    "normal_acne": {
        "cleanser": "Gentle Salicylic Acid Cleanser (0.5%) - Mild acne control",
        "toner": "Balancing Toner with Green Tea",
        "serum": "Niacinamide Serum - Soothes and prevents acne",
        "moisturizer": "Lightweight Gel-Cream Moisturizer",
        "sunscreen": "SPF 50 Sunscreen",
        "treatment": "Tea Tree Spot Treatment - Natural alternative",
        "mask": "Neem & Tulsi Clay Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Treatment → Moisturizer\nWeekly: Neem Mask 1x week"
    },
    
    "normal_pores": {
        "cleanser": "Gentle Foaming Cleanser",
        "toner": "Niacinamide Toner",
        "serum": "Niacinamide Serum",
        "moisturizer": "Lightweight Gel Moisturizer",
        "sunscreen": "SPF 50 Sunscreen",
        "mask": "Clay Mask with Niacinamide - Once a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Moisturizer\nWeekly: Clay Mask 1x week"
    },
    
    "normal_pigmentation": {
        "cleanser": "Gentle Creamy Cleanser",
        "toner": "Balancing Toner",
        "serum": "Vitamin C Serum",
        "moisturizer": "Lightweight Moisturizer",
        "sunscreen": "SPF 50 PA++++ Sunscreen",
        "treatment": "Alpha Arbutin Serum (Night)",
        "mask": "Brightening Yogurt Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Alpha Arbutin → Moisturizer\nWeekly: Brightening Mask 1x week"
    },
    
    "normal_clear": {
        "cleanser": "Gentle Milky Cleanser",
        "toner": "Rose Water Toner",
        "serum": "Vitamin C Serum - For daily glow",
        "moisturizer": "Lightweight Gel-Cream Moisturizer",
        "sunscreen": "SPF 50 Sunscreen",
        "mask": "Multani Mitti (Fuller's Earth) Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Moisturizer\nWeekly: Multani Mitti Mask 1x week"
    },
    
    # NORMAL SKIN - COMBINATIONS
    "normal_acne_pores": {
        "cleanser": "Gentle Salicylic Acid Cleanser",
        "toner": "Niacinamide Toner",
        "serum": "Niacinamide Serum - Targets both concerns",
        "moisturizer": "Lightweight Gel-Cream Moisturizer",
        "sunscreen": "SPF 50 Sunscreen",
        "treatment": "Spot treatment for acne",
        "mask": "Clay Mask with Niacinamide - Once a week",
        "routine": "AM: Cleanser → Toner → Serum → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Treatment → Moisturizer\nWeekly: Clay Mask 1x week"
    },
    
    "normal_acne_pigmentation": {
        "cleanser": "Gentle Creamy Cleanser",
        "toner": "Balancing Toner",
        "serum": "Vitamin C (AM) / Niacinamide (PM)",
        "moisturizer": "Lightweight Moisturizer",
        "sunscreen": "SPF 50 PA++++ Sunscreen",
        "treatment": "Alpha Arbutin for pigmentation (night)",
        "mask": "Brightening + Neem Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Niacinamide → Alpha Arbutin → Moisturizer\nWeekly: Multi-action Mask 1x week"
    },
    
    "normal_pores_pigmentation": {
        "cleanser": "Gentle Foaming Cleanser",
        "toner": "Niacinamide Toner",
        "serum": "Vitamin C (AM) / Niacinamide (PM)",
        "moisturizer": "Lightweight Gel Moisturizer",
        "sunscreen": "SPF 50 PA++++ Sunscreen",
        "treatment": "Alpha Arbutin for pigmentation",
        "mask": "Brightening Clay Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Niacinamide → Alpha Arbutin → Moisturizer\nWeekly: Brightening Clay Mask 1x week"
    },
    
    "normal_acne_pores_pigmentation": {
        "cleanser": "Gentle Salicylic Acid Cleanser",
        "toner": "Niacinamide + PHA Toner",
        "serum": "Alternate: Vitamin C (AM), Niacinamide (PM)",
        "moisturizer": "Lightweight Gel-Cream Moisturizer",
        "sunscreen": "SPF 50 PA++++ Sunscreen - ESSENTIAL",
        "treatment": "Alpha Arbutin for pigmentation (night)",
        "mask": "Multi-action Clay Mask - Once a week",
        "routine": "AM: Cleanser → Toner → Vitamin C → Moisturizer → Sunscreen\nPM: Cleanser → Toner → Niacinamide → Alpha Arbutin → Moisturizer\nWeekly: Multi-action Mask 1x week"
    }
}

def get_recommendations(skin_type, issues):
    """Get product recommendations based on skin type and issues"""
    
    # Clean skin type
    skin_type_lower = skin_type.lower() if skin_type else "normal"
    
    if 'dry' in skin_type_lower:
        skin = 'dry'
    elif 'oily' in skin_type_lower:
        skin = 'oily'
    else:
        skin = 'normal'
    
    # Determine condition(s)
    if not issues or len(issues) == 0:
        condition = "clear"
        key = f"{skin}_{condition}"
        return PRODUCTS.get(key, PRODUCTS[f"{skin}_clear"])
    
    # Collect all detected issues
    detected_issues = []
    for issue_item in issues:
        if isinstance(issue_item, dict):
            issue_text = issue_item.get('issue', '').lower()
        else:
            issue_text = str(issue_item).lower()
        
        if 'acne' in issue_text:
            if 'acne' not in detected_issues:
                detected_issues.append('acne')
        elif 'pore' in issue_text:
            if 'pores' not in detected_issues:
                detected_issues.append('pores')
        elif 'pigment' in issue_text:
            if 'pigmentation' not in detected_issues:
                detected_issues.append('pigmentation')
    
    # Sort for consistency
    detected_issues.sort()
    
    # Create key based on detected issues
    if len(detected_issues) == 0:
        condition = "clear"
    elif len(detected_issues) == 1:
        condition = detected_issues[0]
    elif len(detected_issues) == 2:
        condition = f"{detected_issues[0]}_{detected_issues[1]}"
    else:  # 3 issues
        condition = f"{detected_issues[0]}_{detected_issues[1]}_{detected_issues[2]}"
    
    # Create full key
    key = f"{skin}_{condition}"
    
    # Return recommendations or try fallbacks
    if key in PRODUCTS:
        return PRODUCTS[key]
    
    # Try fallback to most specific combination available
    if len(detected_issues) >= 2:
        # Try two-issue combination
        two_issue_key = f"{skin}_{detected_issues[0]}_{detected_issues[1]}"
        if two_issue_key in PRODUCTS:
            return PRODUCTS[two_issue_key]
    
    # Fallback to first issue only
    if len(detected_issues) >= 1:
        single_key = f"{skin}_{detected_issues[0]}"
        if single_key in PRODUCTS:
            return PRODUCTS[single_key]
    
    # Ultimate fallback
    return PRODUCTS.get(f"{skin}_clear", PRODUCTS["normal_clear"])