# A améliorer plus tard avec d'autres indicateurs en fonction de la stratégie
def calculate_score(price, setup_type, entry_zone, rsi, liquidity_level, bb_basse, bb_haute, ema50, ema200, last_open, last_close, last_low, last_high):

    in_entry_zone = entry_zone[0] <= price <= entry_zone[1]
    if not in_entry_zone:
         return 0
    else:
        score = 2

        if setup_type == "LONG":
            if rsi < 30:
                score += 2
            if last_low < liquidity_level:
                score += 2
            bullish_rejection = (last_low < entry_zone[0] and last_close > entry_zone[0])
            if bullish_rejection:
                score += 2
            if ema50 > ema200:
                score += 1
            if price < bb_basse:
                score += 1

        elif setup_type == "SHORT":
            if rsi > 70:
                score += 2
            if last_high > liquidity_level:
                score += 2
            bearish_rejection = (last_high > entry_zone[1] and last_close < entry_zone[1])
            if bearish_rejection:
                score += 2
            if ema50 < ema200:
                score += 1
            if price > bb_haute:
                score += 1


        return score


def get_signal(score):
        if score < 4:
            return "NONE"
        elif score >= 4 and score < 8:
            return "POTENTIAL SETUP"
        elif score >= 8:
            return "STRONG SETUP"