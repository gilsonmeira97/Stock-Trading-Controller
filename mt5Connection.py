from dotenv import dotenv_values
import MetaTrader5 as mt5

config_mt5 = dotenv_values(".env")

if not mt5.initialize(login=int(config_mt5["LOGIN"]), password=config_mt5["PASSWORD"], server=config_mt5["SERVER"]):
    print("Falha ao inicializar!")
    mt5.shutdown()
else:
    print("Connected!")