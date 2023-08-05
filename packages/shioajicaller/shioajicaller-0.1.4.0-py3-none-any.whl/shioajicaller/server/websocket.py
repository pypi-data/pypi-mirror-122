# -*- coding: utf-8 -*-
import asyncio
import aioredis
import sys,json
import logging
import time
import websockets
from gmqtt import Client as MQTTClient
import uvloop
from ..caller import Caller
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

STOP = asyncio.Event()
ClientS = set()
loop = asyncio.get_event_loop()
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
)
class WebsocketsHandler():
    def SetCallers(self,callers:Caller):
        self._callers = callers
        self._cmdQueue = asyncio.Queue()
        self._eventQueue = asyncio.Queue()
        self._subscribeStocksQueue = asyncio.Queue()
        self._subscribeFuturesQueue = asyncio.Queue()
        self._subscribeClientS = set()

        self._callers.SetEnevtCallBack(self.EnevtCallBack)
        self._callers.SetSubscribeStocksCallBack(self.SubscribeStocksCallBack)
        self._callers.SetSubscribeFuturesCallBack(self.SubscribeFuturesCallBack)

    def _on_connect(self, client, flags, rc, properties):
        logging.info('Mqtt Connected')

    def _on_message(self, client, topic, payload, qos, properties):
        logging.debug('RECV MSG:', payload)

    def _on_disconnect(self, client, packet, exc=None):
        logging.warning('Mqtt Disconnected')

    def _on_subscribe(self, client, mid, qos, properties):
        logging.info('Mqtt subscribed')

    async def SetMqttConnection(self,mqttHost: str,mqttUser: str,mqttPassword: str):
        _timestamp =round(time.time() * 1000)
        self._mqttClient = MQTTClient(f"shioajiCaller-{_timestamp}", receive_maximum=24000, session_expiry_interval=60)
        self._mqttClient.on_connect = self._on_connect
        self._mqttClient.on_message = self._on_message
        self._mqttClient.on_disconnect = self._on_disconnect
        self._mqttClient.on_subscribe = self._on_subscribe

        logging.info(f"SetMqttConnection! {mqttHost} {mqttUser} {mqttPassword}")

        self._mqttClient.set_auth_credentials(mqttUser, mqttPassword)
        await self._mqttClient.connect(mqttHost, keepalive=30)
        await STOP.wait()
        await self._mqttClient.disconnect()

    def SetRedisConnection(self,redisHost: str,redisPort: int,redisDb: str):
        self._redis = aioredis.Redis(
            host=redisHost,
            port=redisPort,
            db=redisDb,
            encoding="utf-8",
            decode_responses=True,
            socket_keepalive=True,
        )
        logging.info(f"SetRedisConnections! {redisHost}:{redisPort}:{redisDb}")

    def EnevtCallBack(self,item):
        loop.call_soon_threadsafe(self._eventQueue.put_nowait, item)

    def SubscribeStocksCallBack(self,item):
        loop.call_soon_threadsafe(self._subscribeStocksQueue.put_nowait, item)

    def SubscribeFuturesCallBack(self,item):
        loop.call_soon_threadsafe(self._subscribeFuturesQueue.put_nowait, item)

    async def CmdWorker(self,name):
        counter = 0
        logging.info(f'{name} start!')
        while True:
            Item = await self._cmdQueue.get()
            logging.debug(f'CmdWorker<< {Item["cmd"]}')
            if Item["cmd"] == 'GetAccount':
                websocket = Item["wsclient"]
                ret = {"type": "response"}
                account = self._callers.GetAccount()
                if (account):
                    ret["account"] = account
                await websocket.send(json.dumps(ret, default=str))
            counter += 1
            self._cmdQueue.task_done()

    async def EnevtWorker(self,name):
        counter = 0
        logging.info(f'{name} start!')
        while True:
            Item = await self._eventQueue.get()
            ret = {"type":"SystemEvent","ret":Item}
            strMsg = json.dumps(ret, default=str)
            logging.debug(f'EnevtWorker<< {strMsg}')
            websockets.broadcast(ClientS, strMsg)
            if hasattr(self,"_redis") or hasattr(self,"_mqttClient"):
                PstrMsg = json.dumps(Item, default=str)
                if hasattr(self,"_redis"):
                    logging.debug(f'Redis publish >> {PstrMsg}')
                    await self._redis.publish("shioaji.system", PstrMsg)
                if hasattr(self,"_mqttClient"):
                    logging.debug(f'Mqtt publish >> {PstrMsg}')
                    mqtttopic = f'Shioaji/v1/system'
                    self._mqttClient.publish(mqtttopic, PstrMsg, qos=1)
            counter += 1
            self._eventQueue.task_done()

    async def SubscribeStocksWorker(self,name):
        counter = 0
        logging.info(f'{name} start!')
        while True:
            Item = await self._subscribeStocksQueue.get()
            if len(self._subscribeClientS)>0:
                ret = {"type":"StocksEvent","ret":Item}
                strMsg = json.dumps(ret, default=str)
                websockets.broadcast(self._subscribeClientS, strMsg)

            if hasattr(self,"_redis") or hasattr(self,"_mqttClient"):
                PstrMsg = json.dumps(Item, default=str)
                if hasattr(self,"_redis"):
                    logging.debug(f'Redis publish >> {PstrMsg}')
                    await self._redis.publish(f'shioaji.stocks.tick.{Item["code"]}', PstrMsg)
                if hasattr(self,"_mqttClient"):
                    logging.debug(f'Mqtt publish >> {PstrMsg}')
                    mqtttopic = f'Shioaji/v1/stocks/tick/{Item["code"]}'
                    self._mqttClient.publish(mqtttopic, PstrMsg, qos=1)
            logging.debug(f'SubscribeStocksWorker<< {Item}')
            counter += 1
            self._subscribeStocksQueue.task_done()

    async def SubscribeFuturesWorker(self,name):
        counter = 0
        logging.info(f'{name} start!')
        while True:
            Item = await self._subscribeFuturesQueue.get()
            if len(self._subscribeClientS)>0:
                ret = {"type":"FuturesEvent","ret":Item}
                strMsg = json.dumps(ret, default=str)
                websockets.broadcast(self._subscribeClientS, strMsg)
            if hasattr(self,"_redis") or hasattr(self,"_mqttClient"):
                PstrMsg = json.dumps(Item, default=str)
                if hasattr(self,"_redis"):
                    logging.debug(f'Redis publish >> {PstrMsg}')
                    await self._redis.publish(f'shioaji.futures.tick.{Item["code"]}', PstrMsg)
                if hasattr(self,"_mqttClient"):
                    logging.debug(f'Mqtt publish >> {PstrMsg}')
                    mqtttopic = f'Shioaji/v1/futures/tick/{Item["code"]}'
                    self._mqttClient.publish(mqtttopic, PstrMsg, qos=1)
            logging.debug(f'SubscribeFuturesWorker<< {Item}')
            counter += 1
            self._subscribeFuturesQueue.task_done()

    async def run(self,websocket,message):
        self._message = message
        self._websocket = websocket
        if (self.checkEmptyMessage()):
            return
        self._data = self.checkFormateMessage(self._message)
        if (self._data == None):
            await websocket.send(json.dumps({"error": "wrong formate message."}))
            return
        logging.info("<< "+ self._message)
        CmdDefault = json.dumps({"type": "respose", "result": f'command not found.'})
        if 'params' not in self._data:
            logging.info(f'cmd{self._data["cmd"]}')
            result = await getattr(self, f'cmd{self._data["cmd"]}', lambda: CmdDefault)(wsclient= websocket)
        else:
            logging.info(f'cmd{self._data["cmd"]}::{self._data["params"]}')
            result = await getattr(self, f'cmd{self._data["cmd"]}', lambda: CmdDefault)(wsclient= websocket,**self._data["params"])
        if type(result) == str:
            await websocket.send(result)

    async def cmdID(self,wsclient):
        # {"cmd":"ID"}
        ret = {"type": "response","ret":True}
        ret["id"] = f'{self._websocket.id}'
        self._subscribeClientS.add(wsclient)
        await wsclient.send(json.dumps(ret, default=str))

    async def cmdGetsubscribEvents(self,wsclient):
        # {"cmd":"GetsubscribEvents"}
        ret = {"type": "response","ret":True}
        self._subscribeClientS.discard(wsclient)
        self._subscribeClientS.add(wsclient)
        await wsclient.send(json.dumps(ret, default=str))

    async def cmdRemovesubscribEvents(self,wsclient):
        # {"cmd":"RemovesubscribEvents"}
        ret = {"type": "response","ret":True}
        self._subscribeClientS.discard(wsclient)
        await wsclient.send(json.dumps(ret, default=str))

    async def cmdGetAccount(self,wsclient):
        # {"cmd":"GetAccount"}
        cmd =  {"cmd":"GetAccount","wsclient":wsclient}
        loop.call_soon_threadsafe(self._cmdQueue.put_nowait, cmd)

    async def cmdSubscribeFutures(self,wsclient,**keyword_params):
        # {"cmd":"SubscribeFutures","params":{"code":"TXFJ1","quote_type":"tick"}}
        ret = {"type": "response", "status": self._callers.SubscribeFutures(**keyword_params)}
        await wsclient.send(json.dumps(ret, default=str))

    async def cmdSubscribeStocks(self,wsclient,**keyword_params):
        # {"cmd":"SubscribeStocks","params":{"code":"2330","quote_type":"tick"}}
        ret = {"type": "response", "status": self._callers.SubscribeStocks(**keyword_params)}
        await wsclient.send(json.dumps(ret, default=str))

    def checkEmptyMessage(self):
        return (len(self._message) <= 0)

    def checkFormateMessage(self,message):
        try:
            return json.loads(message)
        except:
            pass
        finally:
            pass

    def ClientS_event(self):
        return json.dumps({"type": "total connects", "count": len(ClientS)})

WebsocketsHandler = WebsocketsHandler()

async def root(websocket, path):
    try:
        # Register user
        ClientS.add(websocket)
        websockets.broadcast(ClientS, WebsocketsHandler.ClientS_event())
        # Manage state changes
        async for message in websocket:
            await WebsocketsHandler.run(websocket,message)
    finally:
        # Unregister user
        ClientS.remove(websocket)
        websockets.broadcast(ClientS, WebsocketsHandler.ClientS_event())

async def start_server(port=6789):
    try:
        async with websockets.serve(root, "", port):
            await asyncio.Future()
    except (asyncio.CancelledError, KeyboardInterrupt):
        print('Cancelled task')
        STOP.set()
        sys.exit(0)
    except Exception as ex:
        print('Exception:', ex)
    return None

def __start_wss_server(port:int=6789,callers:Caller=Caller(),pool_size:int=50,debug:int=logging.WARNING,
    with_redis:bool=False,redisHost:str=None,redisPort:int=6379,redisDb:str="0",
    with_mqtt:bool=False,mqttHost:str=None,mqttUser:str="",mqttPassword:str=""):
    WebsocketsHandler.SetCallers(callers)
    if with_redis:
        WebsocketsHandler.SetRedisConnection(redisHost,redisPort,redisDb)
    logger = logging.getLogger()
    logger.setLevel(debug)
    if debug == logging.DEBUG:
        loop.set_debug(True)
    task = None
    try:
        if with_mqtt:
            loop.create_task(WebsocketsHandler.SetMqttConnection(mqttHost,mqttUser,mqttPassword))
        loop.create_task(WebsocketsHandler.EnevtWorker('EnevtWorker-1'))
        loop.create_task(WebsocketsHandler.CmdWorker('CmdWorker-1'))

        for i in range(pool_size):
            loop.create_task(WebsocketsHandler.SubscribeStocksWorker(f'SubscribeStocksWorker-{i}'))
            loop.create_task(WebsocketsHandler.SubscribeFuturesWorker(f'SubscribeFuturesWorker-{i}'))

        task = asyncio.ensure_future(start_server(port))
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        if task:
            print('Interrupted, cancelling tasks')
            task.cancel()
            loop.run_forever()
            task.exception()
    finally:
        loop.close()

if __name__ == "__main__":
    __start_wss_server()