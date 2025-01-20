import json
import bitstamp.client
import websocket
from bitstamp.client import trading
import credencial


def cliente():
    return bitstamp.client.Trading(username=credencial.USERNAME, key =credencial.KEY,secret =credencial.SECRET)

def comprar(quantidade):
    trading_client =  cliente()
    trading_client.buy_market_order(quantidade)

def vender(quantidade):
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)


def ao_brir(ws):
    print("Online!")
    json_subscribe = """
    {
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
"""
    ws.send(json_subscribe)

def ao_fechar(ws):
    print("Offilne!")

def erro(ws, erro):
    print("Error!")
    print(f"Detalhes do erro: {erro}")

def ao_receber_mensagem(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    amount = mensagem['data']['amount_str']
    print(f"Preço $:{price:.2f}, Quantidade:{amount}")
    if price > 9000:
        vender()
    elif price > 8000:
        comprar()
    else:
        print("Aguardar")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=ao_brir,
                                on_close=ao_fechar,
                                on_message=ao_receber_mensagem,
                                on_error=erro)
ws.run_forever()
