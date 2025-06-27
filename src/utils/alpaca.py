import os
import requests


def submit_orders(decisions: dict[str, dict]) -> None:
    """Send trade orders to Alpaca based on portfolio manager decisions."""
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")
    base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

    if not api_key or not secret_key:
        print("Alpaca API keys not configured. Skipping order submission.")
        return

    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key,
        "Content-Type": "application/json",
    }

    action_map = {
        "buy": "buy",
        "sell": "sell",
        "short": "sell",
        "cover": "buy",
    }

    for symbol, decision in decisions.items():
        action = decision.get("action", "").lower()
        qty = int(decision.get("quantity", 0))
        if action == "hold" or qty <= 0:
            continue
        side = action_map.get(action)
        order = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": "market",
            "time_in_force": "day",
        }
        try:
            resp = requests.post(f"{base_url}/v2/orders", json=order, headers=headers)
            if resp.status_code not in (200, 201):
                print(f"Failed to submit order for {symbol}: {resp.text}")
            else:
                print(f"Submitted {side} order for {qty} {symbol}")
        except Exception as e:
            print(f"Error submitting order for {symbol}: {e}")
