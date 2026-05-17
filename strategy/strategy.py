# A améliorer plus tard avec d'autres indicateurs en fonction de la stratégie
def calculate_score(price, setup_type, entry_zone, rsi, liquidity_level, last_lows, last_highs, bb_basse, bb_haute, ema50, ema200):
    in_entry_zone = entry_zone[0] <= price <= entry_zone[1]
    if not in_entry_zone:
         return 0
    else:
        score = 2
        if setup_type == "LONG":
            if rsi < 30:
                score += 2
            if ema50 > ema200:
                score += 1
            if price < bb_basse:
                score += 1
            # Regarde si on est sous liquidity_level
            current_low = last_lows.iloc[-1]
            if current_low <= liquidity_level:
                score += 2

        elif setup_type == "SHORT":
            if rsi > 70:
                score += 2
            if ema50 < ema200:
                score += 1
            if price > bb_haute:
                score += 1
            # Regarde si on est au dessus de liquidity_level
            current_high = last_highs.iloc[-1]
            if current_high >= liquidity_level:
                score += 2

        return score


def get_signal(score):
        if score < 2:
            return "NONE"
        elif score >= 2 and score < 6:
            return "POTENTIAL SETUP"
        elif score >= 6:
            return "STRONG SETUP"