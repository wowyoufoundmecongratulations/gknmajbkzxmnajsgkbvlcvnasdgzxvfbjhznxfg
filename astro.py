import datetime, os, uuid, re, asyncio, random, requests, aiohttp, json, time, json, sys, websockets, platform, locale, hashlib, subprocess, discord
from discord.ext import commands
from typing import Dict
from pytz import timezone
tz = timezone('America/Sao_Paulo')

class bucket:
    def __init__(self, max_tokens: int, refill_interval: float):
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refill_interval = refill_interval
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        self.last_refill_time = asyncio.get_event_loop().time()

    async def take(self, tokens: int):
        await self.refill()
        while tokens > self.tokens:
            await asyncio.sleep(self.refill_interval - (asyncio.get_event_loop().time() - self.last_refill_time))
            await self.refill()
        self.tokens -= tokens

    async def refill(self):
        if not asyncio.get_event_loop().is_running():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        if asyncio.get_event_loop().time() - self.last_refill_time >= self.refill_interval:
            self.tokens = self.max_tokens
            self.last_refill_time = asyncio.get_event_loop().time()

class Sniper:
    def __init__(self) -> None:
            # if jsmgklagoalrkartv is None:
            #     print('LMAOOOOOOOOOOOOOOOOO')
            #     sys.exit(0)

            self.websocket = None
            
            self._config = None

            self.start_time = time.time()

            self.ratelimit = bucket(max_tokens=60, refill_interval=60)

            self.checks = 0
            self.buys = 0
            self.last_time = 0
            self.errors = 0

            self.time = 0

            self.items = self.load_item_list

            self.soldOut = []

            self.logs = {}

            self.accounts = {}

            self.item_info = {}

            self.allowed_users = [account['user_id'] for account in self.config.get('accounts')]
            self.staff_users = self.config.get('staff')

            self.run_bot()

    def get_total_ram(self):
        if platform.system() == 'Darwin':
            output = subprocess.check_output(['sysctl', '-n', 'hw.memsize']).decode().strip()
            return int(output)
        elif platform.system() == 'Windows':
            output = subprocess.check_output(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory']).decode().strip()
            return int(output.split('\n')[1])
        else:
            return 0

    def hwid(self):
        os_info = {
            'cpu': platform.processor(),
            'ram': self.get_total_ram(),
            'os': os.name,
            'arch': platform.architecture()[0],
            'platform': platform.system(),
            'release': platform.release(),
            'locale': locale.getlocale()[0],
            'timezone': time.tzname[0]
        }

        return hashlib.sha256(str(os_info).encode('utf-8')).hexdigest()

    async def connect_websocket(self):
        try:
            uri = "ws://astro.facal.me:4313"
            while True:
                try:
                    async with websockets.connect(uri) as websocket:
                        self.websocket = websocket
                        await self.websocket_connected()
                        async for data_message in websocket:
                            try:
                                data = json.loads(data_message)
                            except:
                                continue

                            event = data.get('event')

                            if event == 'aejbntakehnbrahbwhra':
                                await self.on_connected()

                            if event == 'majnekfnawlkfasdkemaen':
                                await self.on_invalid_credentials()

                            if event == 'aekhbaehjkbraehrabht':
                                await self.on_ban()

                            if event == 'okasdkoaskosdaoksadok':
                                await self.on_new_item(data)

                            if event == 'jtajmarjhalkkralwjrna':
                                await self.on_add_item(data)
                            

                except (websockets.ConnectionClosedError, ConnectionRefusedError):
                    print(f"{await self.get_time()} Autosearch is offline! Retrying in 5 seconds...")
                    await asyncio.sleep(5)
        except Exception as e:
            print(e, "Error connecting to autosearch! Retrying in 5 seconds...")
            await asyncio.sleep(5)
            await self.connect_websocket()


    async def websocket_msg(self, data):
        if self.websocket and self.websocket.open:
            await self.websocket.send(json.dumps(data))

    async def websocket_connected(self):
        hwid = self.hwid()
        ip = requests.get('https://checkip.amazonaws.com').text.strip()
        await self.websocket_msg({'event': 'amsklçouinasçekfmangas', 'discord_id': self.discord, 'ip': ip, 'hwid': hwid, 'key': self.key, 'jsmgklagoalrkartv': jsmgklagoalrkartv})

    async def on_add_item(self, data):
        item_id = data.get('item_id')
        if int(item_id) not in self.items:
            self.add_item(int(item_id))

    async def new_item(self, data):
        await self.websocket_msg({'event': 'okasdkoaskosdaoksadok', 'item': data})

    async def on_new_item(self, data):
        item_name = data.get('item_name')
        raw_id = data.get('raw_id')
        if int(raw_id) in self.soldOut:
            return
        print(f"{await self.get_time()} Autosearch | {item_name} | {raw_id} | Buying item")
        coroutines = [
                self.buy_item(
                    account=f"{i+1}",
                    item_id=data.get('item_id'),
                    item_name=data.get('item_name'),
                    price=data.get('price'),
                    totalQuantity=data.get('totalQuantity'),
                    quantityLimitPerUser=data.get('quantityLimitPerUser'),
                    creator_id=data.get('creator_id'),
                    product_id=data.get('product_id'),
                    raw_id=data.get('raw_id'),
                    assetType=data.get('assetType'),
                    method="Autosearch"
                ) for i, _ in enumerate(self.accounts) for _ in range(1)
            ]

        await asyncio.gather(*coroutines)

    async def on_connected(self):
        print(f"{await self.get_time()} Connected to autosearch!")

    async def on_invalid_credentials(self):
        print(f"{await self.get_time()} Invalid credentials. Exiting...")
        os._exit(0)

    async def on_bought(self, raw_id):
        await self.websocket_msg({'event': 'iakdlarknamhtuiaismfng', 'raw_id': raw_id})

    async def on_sold_out(self, raw_id, serials):
        await self.websocket_msg({'event': 'klmafkanfajfdfakmfakfna', 'raw_id': raw_id, 'serials': serials})
        

    def run_bot(self):
        bot = commands.Bot(command_prefix=self.config.get('bot')['prefix'], intents=discord.Intents.all())

        @bot.command(name="exit")
        async def exit(ctx):
            message = f"Exiting..."
            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)
            os._exit(0)

        @bot.command(name="restart")
        async def restart(ctx):
            message = f"Restarting..."
            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)
            os.execv(sys.executable, ['python'] + sys.argv + [f'--token={token}'])

        @bot.command(name="accounts", aliases=["acc"])
        async def accounts(ctx):
            message = f"**Accounts** ({len(self.accounts)})\n"
            for i, account in enumerate(self.accounts):
                message += f"{i+1}. {self.accounts[account]['displayName']} (@{self.accounts[account]['name']})\n"

            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)

        @bot.command(name="uptime", aliases=["up"])
        async def uptime(ctx):
            check_time = time.time() - self.start_time
            m, s = divmod(check_time, 60)
            h, m = divmod(m, 60)
            if h > 0:
                message = f"Uptime: {int(h)}h {int(m)}m {int(s)}s"
            elif m > 0:
                message = f"Uptime: {int(m)}m {int(s)}s"
            else:
                message = f"Uptime: {int(s)}s"
            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)

        @bot.command(name="info")
        async def info(ctx):
            account_info = None
            for acc in self.accounts.values():
                if acc['user_id'] == ctx.author.id:
                    account_info = acc
                    break

            id = account_info['id']
            name = f"{account_info['displayName']} (@{account_info['name']})"
            thumbnail = account_info['thumbnail']

            await self.account_info(ctx=ctx, user_id=id, username=name, thumbnail=thumbnail)

        @bot.command(name="stats", aliases=["s"])
        async def stats(ctx):
            message = f"""
            buys: {self.buys}/{self.errors}
            items: {len(self.items)}
            checks: {self.checks}/{self.last_time}ms
            """
            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)

        @bot.command(name="queue", aliases=["q"])
        async def queue(ctx):
            if not self.items:
                message = f"Item list is empty."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            message = f"**Item List** ({len(self.items)})\n"
            for i, item in enumerate(self.items):
                message += f"{i+1}. {item}\n"

            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)

        @bot.command(name="add")
        async def add(ctx, item_id=None):
            if item_id is None:
                message = f"Please provide an item ID."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            match = re.search(r'https?://www.roblox.com/catalog/(\d+)', item_id)
            if match:
                item_id = match.group(1)

            if not item_id.isdigit():
                message = f"Please provide a valid item ID."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            if int(item_id) not in self.items:
                self.add_item(int(item_id))

                message = f"Item `{item_id}` added to the list."
                embed = discord.Embed(description=message, color=0x2B2D31)
                await ctx.send(embed=embed)
            else:
                message = f"Item `{item_id}` already in the list."
                embed = discord.Embed(description=message, color=0x2B2D31)
                await ctx.send(embed=embed)

        @bot.command(name="remove")
        async def remove(ctx, item_id=None):
            if item_id is None or not item_id.isdigit():
                message = f"Please provide an item ID or index."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            item_id = int(item_id)
            if item_id in self.items:
                self.remove_item(item_id)
                message = f"Item `{item_id}` removed from the list."
                embed = discord.Embed(description=message, color=0x2B2D31)
                await ctx.send(embed=embed)
            elif 1 <= item_id <= len(self.items):
                item = self.items.pop(item_id - 1)
                message = f"Item `{item}` removed from the list."
                embed = discord.Embed(description=message, color=0x2B2D31)
                await ctx.send(embed=embed)
            else:
                message = f"Item `{item_id}` not found in the list."
                embed = discord.Embed(description=message, color=0x2B2D31)
                await ctx.send(embed=embed)

        @bot.command(name="clear")
        async def clear(ctx):
            self.items.clear()
            self.clear_items()

            message = f"All items removed from the list."
            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)

        @bot.command(name="link")
        async def link(ctx, index):
            if index.lower() == "all":
                if not self.items:
                    message = "Item list is empty."
                    embed = discord.Embed(description=message, color=0x2B2D31)
                    return await ctx.send(embed=embed)

                item_urls = [f"https://www.roblox.com/catalog/{item_id}" for item_id in self.items]
                message = '\n'.join(item_urls)
                await ctx.send(message)
            else:
                try:
                    index = int(index)
                except ValueError:
                    message = f"Please provide a valid index between 1 and {len(self.items)} or 'all'."
                    embed = discord.Embed(description=message, color=0x2B2D31)
                    return await ctx.send(embed=embed)

                if index < 1 or index > len(self.items):
                    message = f"Please provide a valid index between 1 and {len(self.items)}."
                    embed = discord.Embed(description=message, color=0x2B2D31)
                    return await ctx.send(embed=embed)

                item_id = self.items[index - 1]
                await ctx.send(f"https://www.roblox.com/catalog/{item_id}")

        @bot.command(name="add-cookie")
        async def add_cookie(ctx, cookie=None, user_id=None):
            if cookie is None or user_id is None:
                message = f"Please provide a cookie."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            response = await self._get_user_id(cookie)
            response2 = await self._get_xcsrf_token(cookie)
            if not response or not response2:
                message = f"Invalid cookie."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            with open("config.json", "r") as file:
                config = json.load(file)
            config['accounts'].append({"user_id": user_id, "cookie": cookie})
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)

            self.accounts = await self._setup_accounts()

            message = f"Cookie added to the list."
            embed = discord.Embed(description=message, color=0x2B2D31)
            return await ctx.send(embed=embed)

        @bot.command(name="remove-cookie")
        async def remove_cookie(ctx, index=None):
            if index is None or not index.isdigit():
                message = f"Invalid index. Please provide an index between 1 and {len(self.accounts)}."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            index = int(index) - 1
            if index < 0 or index >= len(self.accounts):
                message = f"Invalid index. Please provide an index between 1 and {len(self.accounts)}."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            with open("config.json", "r") as file:
                config = json.load(file)
            del config['accounts'][index]
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)

            self.accounts = await self._setup_accounts()

            message = f"Succesfully removed cookie."
            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)

        @bot.command(name="modify-cookie")
        async def modify_cookie(ctx, index=None, new_cookie=None):
            if index is None or not index.isdigit() or new_cookie is None:
                message = f"Invalid index or new cookie. Please provide an index between 1 and {len(self.accounts)} and a new cookie."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            index = int(index) - 1
            if index < 0 or index >= len(self.accounts):
                message = f"Invalid index. Please provide an index between 1 and {len(self.accounts)}."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            response = await self._get_user_id(new_cookie)
            response2 = await self._get_xcsrf_token(new_cookie)
            if not response or not response2:
                message = f"Invalid cookie."
                embed = discord.Embed(description=message, color=0x2B2D31)
                return await ctx.send(embed=embed)

            with open("config.json", "r") as file:
                config = json.load(file)
            config['accounts'][index]['cookie'] = new_cookie
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)

            self.accounts = await self._setup_accounts()

            message = f"Succesfully modified cookie."
            embed = discord.Embed(description=message, color=0x2B2D31)
            await ctx.send(embed=embed)

        @bot.event
        async def on_ready():
            print(f"{await self.get_time()} {bot.user.name} is ready!")
            self.accounts = await self._setup_accounts()

            print(f"{await self.get_time()} Astro is ready!")

            await self.start()

        @bot.event
        async def on_message(message):
            if not await self.staff_verify(str(message.author.id)):
                return
            
            await bot.process_commands(message)

        bot.run(self.config.get('bot')['token'])
        # bot.run(self.config.get('bot')['token'], log_handler=None)

    @property
    def config(self):
        with open("config.json") as file:
            self._config = json.load(file)
        return self._config
    
    @property
    def discord(self): return self.config.get("info", {}).get("discord_id", None)

    @property
    def key(self): return self.config.get("info", {}).get("key", None)

    @property
    def clear(self): return "cls" if os.name == 'nt' else "clear"

    @property
    def webhookBought(self): return self.config.get("webhook", None)

    @property
    def log(self): return self.config.get("logs", None)

    @property
    def experience_only(self): return self.log.get("experience_only", False)

    @property
    def expensive_price(self): return self.log.get("expensive_price", False)

    @property
    def offsale(self): return self.log.get("off_sale", False)

    @property
    def bought(self): return self.log.get("bought", False)

    @property
    def load_item_list(self): return self._load_items()

    async def get_time(self):
        now = datetime.datetime.now(tz)
        formatted_date_time = now.strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]
        return f"[{formatted_date_time}]"

    async def staff_verify(self, user_id):
        if user_id in self.staff_users:
            return True
        else:
            return False

    def add_item(self, item_id: int):
        self.items.append(item_id)
        with open("config.json", "r") as file:
            config = json.load(file)
        config['items'].append(item_id)
        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)

    def remove_item(self, item_id: int):

        if item_id in self.items:
            self.items.remove(item_id)
            with open("config.json", "r") as file:
                config = json.load(file)
            config['items'].remove(item_id)
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)

    def clear_items(self):
        self.items.clear()

        with open("config.json", "r") as file:
            config = json.load(file)
        config['items'].clear()
        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)

    def send_embed(self, webhook_url=str, embed=None, discord_id=None):
        embed_dict = embed.to_dict()
        if discord_id:
            return requests.post(webhook_url, json={"content": f"<@{discord_id}>", "embeds": [embed_dict]})
        return requests.post(webhook_url, json={"embeds": [embed_dict]})

    def send_message(self, webhook_url=str, message=str):
        return requests.post(webhook_url, json={"content": message})

    async def get_item_info(self, item_id: int) -> None:
        async with aiohttp.ClientSession() as client:
            try:
                async with client.get(
                        f"https://thumbnails.roblox.com/v1/assets?assetIds={item_id}&size=512x512&format=Png&isCircular=false",
                        headers={"Accept-Encoding": "gzip, deflate"},
                        ssl=False,
                    ) as response:

                    response.raise_for_status()
                    thumbnail_data = json.loads(await response.text())["data"][0]
                    thumbnail_url = thumbnail_data["imageUrl"]

                    return thumbnail_url
            except Exception as e:
                print(e)
                thumbnail_url = "https://i.imgur.com/rHqF5AD.png"

                return thumbnail_url

    async def account_info(
        self,
        ctx,
        user_id: int,
        username: str,
        thumbnail: str
    ):

        total_bought = 0
        item_info_list = []
        if user_id in self.logs:
            for raw_id, item_info in self.logs[user_id]["items"].items():
                total_bought += item_info["bought"]
                serials_str = ', '.join(item_info["serials"])
                item_info_list.append(f"{item_info['bought']}x {item_info['name']} ({serials_str})")

        item_info_list.reverse()

        items = None

        if item_info_list:
            items = '\n'.join(item_info_list)
        else:
            items = "Nothing..."

        embed = discord.Embed(
            color=0x2B2D31
        )

        embed.add_field(name=f"Purchased Items ({total_bought:,})", value=f"```{items}```", inline=True)

        embed.set_author(name=username, url=f"https://www.roblox.com/users/{user_id}/profile", icon_url=thumbnail)

        return await ctx.send(embed=embed)

    async def embed_item_info(
            self,
            webhook: str,
            item_id: int,
            name: str,
            price: int,
            total: int,
            limit: int,
            message: None,
            username: None,
            user_id: None,
            discord_id: None,
            thumbnail: None,
            assetType: int,
            purchase_count: int,
            headers: dict,
            cookies: dict,
            method: str,
        ):

        thumbnail_url = await self.get_item_info(item_id)

        if assetType:
            await asyncio.sleep(10)
            async with aiohttp.ClientSession() as client:
                async with client.get(
                        f"https://inventory.roblox.com/v2/users/{user_id}/inventory/{assetType}?cursor=&limit=10&sortOrder=Desc",
                        headers=headers,
                        cookies=cookies,
                        ssl=False,
                    ) as response:

                    response.raise_for_status()
                    data = json.loads(await response.text())["data"]
                    for item in data:
                        if item["assetId"] == item_id:
                            self.logs[user_id]["items"][item_id]["serials"].append(item['serialNumber'])
                            break

                    await self.on_sold_out(item_id, serials)

                    serials = self.logs[user_id]["items"][item_id]["serials"]
                    serials.sort(key=lambda x: int(x))
                    serials_str = [f"#{serial}" for serial in serials]
                    serials_str = ', '.join(serials_str)
                    message = f"Purchased: {purchase_count}x\n\nSerial: {serials_str}"


        embed = discord.Embed(
            title=name,
            url=f"https://www.roblox.com/catalog/{item_id}",
            description=f"```{message}```",
            color=0x2B2D31
        )
        embed.set_thumbnail(url=thumbnail_url)
        embed.add_field(name="Price", value=f"Free" if price == 0 else f"{price}", inline=True)
        embed.add_field(name="Total Quantity", value=f"{total:,}", inline=True)
        embed.add_field(name="Quantity p/user", value=f"{limit}" if limit >= 1 else "Unlimited", inline=True)
        if username and user_id and thumbnail:
            embed.set_author(name=username, url=f"https://www.roblox.com/users/{user_id}/profile", icon_url=thumbnail)
        embed.set_footer(text = f"Astro - {method}", icon_url = "https://i.imgur.com/qK50XYd.jpg")

        if discord_id:
            if not self.bought:
                return
            return self.send_embed(webhook_url=webhook, embed=embed, discord_id=discord_id)
        return self.send_embed(webhook_url=webhook, embed=embed)

    def _load_cookies(self) -> dict:
            lines = self.config['accounts']
            my_dict = {}
            for i, line in enumerate(lines):
                my_dict[str(i+1)] = {}
                my_dict[str(i+1)] = {"cookie": line['cookie']}
            return my_dict

    async def _setup_accounts(self) -> Dict[str, Dict[str, str]]:
        cookies = self._load_cookies()
        invalid_cookies = []
        for i in cookies:
            response = await self._get_user_id(cookies[i]["cookie"])
            response2 = await self._get_xcsrf_token(cookies[i]["cookie"])

            if not response or not response2:
                print(f"#{i} Invalid cookie.")
                invalid_cookies.append(i)
                continue

            response3 = await self._get_thumbnail_user(response["id"])

            cookies[i]["user_id"] = self.config['accounts'][int(i)-1]['user_id']
            cookies[i]["id"] = response["id"]
            cookies[i]["name"] = response["name"]
            cookies[i]["displayName"] = response["displayName"]
            cookies[i]["thumbnail"] = response3
            cookies[i]["xcsrf_token"] = response2["xcsrf_token"]
            cookies[i]["created"] = response2["created"]
            cookies[i]["purchase_count"] = 0

            print(f"{await self.get_time()} #{i} {cookies[i]['displayName']} (@{cookies[i]['name']})")

            with open('config.json', 'r') as f:
                config = json.load(f)
            config['accounts'][int(i)-1]['name'] = response["name"]
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)

        for i in invalid_cookies:
            del cookies[i]

        return cookies

    async def _get_user_id(self, cookie) -> str:
       async with aiohttp.ClientSession(cookies={".ROBLOSECURITY": cookie}) as client:
           response = await client.get("https://users.roblox.com/v1/users/authenticated", ssl = False)
           data = await response.json()
           if data.get('id') == None:
              return False
           return data

    async def _get_xcsrf_token(self, cookie) -> dict:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None), timeout=aiohttp.ClientTimeout(total=None), cookies={".ROBLOSECURITY": cookie}) as client:
            response = await client.post("https://accountsettings.roblox.com/v1/email", ssl = False)
            xcsrf_token = response.headers.get("x-csrf-token")
            await client.close()
            if xcsrf_token is None:
                return False
            return {"xcsrf_token": xcsrf_token, "created": datetime.datetime.now()}

    async def _get_thumbnail_user(self, user_id) -> str:
        async with aiohttp.ClientSession() as client:
            try:
                async with client.get(
                        f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false",
                        headers={"Accept-Encoding": "gzip, deflate"},
                        ssl=False,
                    ) as response:

                    response.raise_for_status()
                    thumbnail_data = json.loads(await response.text())["data"][0]
                    thumbnail_url = thumbnail_data["imageUrl"]
            except Exception as e:
                thumbnail_url = "https://i.imgur.com/rHqF5AD.png"

            return thumbnail_url

    async def auto_xtoken(self):
        while True:
            await self._check_xcsrf_token()
            await asyncio.sleep(60)

    async def _check_xcsrf_token(self) -> bool:
        for i in self.accounts:
            if self.accounts[i]["xcsrf_token"] is None or \
                datetime.datetime.now() > (self.accounts[i]["created"] + datetime.timedelta(minutes=4)):
                try:
                    response = await self._get_xcsrf_token(self.accounts[i]["cookie"])
                    self.accounts[i]["xcsrf_token"] = response["xcsrf_token"]
                    self.accounts[i]["created"] = response["created"]
                except Exception as e:
                    print(f"{e.__class__.__name__}: {e}")
                    return False
        return True

    async def given_id_sniper(self) -> None:
            try:
                await self.search()
            except aiohttp.ServerDisconnectedError:
                return

    async def search(self) -> None:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None), timeout=aiohttp.ClientTimeout(total=None)) as session:

                self.t0 = 0

                while True:
                    try:
                        if len(self.items) == 0:
                            await asyncio.sleep(1)
                            continue
                        else:
                            for item_id in self.items:
                                if item_id in self.soldOut:
                                    self.remove_item(int(item_id))
                                    continue

                            self.t0 = asyncio.get_event_loop().time()

                            await self.ratelimit.take(1)

                            currentAccount = self.accounts[str(random.randint(1, len(self.accounts)))]

                            async with session.post(
                                "https://catalog.roblox.com/v1/catalog/items/details",
                                json={"items": [{"itemType": "Asset", "id": id} for id in self.items]},
                                headers={
                                    "x-csrf-token": currentAccount['xcsrf_token'],
                                    'Accept': "application/json",
                                    "Accept-Encoding": "gzip, deflate"
                                },
                                cookies={".ROBLOSECURITY": currentAccount["cookie"]},
                                ssl=False
                            ) as response:

                                response.raise_for_status()

                                response_text = await response.text()

                                json_response = json.loads(response_text)['data']

                                for i in json_response:
                                    raw_id = i.get('id')
                                    creator = i.get('creatorTargetId')
                                    item_name = i.get('name', 'Unknown')
                                    price = i.get('price', 0)
                                    productid_data = None
                                    collectibleItemId = i.get("collectibleItemId")
                                    totalQuantity = i.get("totalQuantity", 0)
                                    quantityLimitPerUser = i.get("quantityLimitPerUser", 0)
                                    assetType = i.get("assetType")
                                    saleLocationType = i.get("saleLocationType")
                                    
                                    if saleLocationType == "ExperiencesDevApiOnly":
                                        print(f"{await self.get_time()} Watcher | {item_name} | {raw_id} | Experience only")
                                        self.soldOut.append(int(raw_id))
                                        self.remove_item(int(raw_id))
                                        self.checks += 1
                                        t1 = asyncio.get_event_loop().time()
                                        self.last_time = round(t1 - self.t0, 3)
                                        if not self.expensive_price:
                                            continue

                                        await self.embed_item_info(
                                            webhook=self.webhookBought,
                                            item_id=raw_id,
                                            name=item_name,
                                            price=price,
                                            total=totalQuantity,
                                            limit=quantityLimitPerUser,
                                            message="Experience Only",
                                            username=None,
                                            user_id=None,
                                            discord_id=None,
                                            thumbnail=None,
                                            assetType=None,
                                            purchase_count=None,
                                            headers=None,
                                            cookies=None,
                                            method="Watcher"
                                        )
                                        continue

                                    if price > 0:
                                        print(f"{await self.get_time()} Watcher | {item_name} | {raw_id} |  Expensive price (${price})")
                                        self.soldOut.append(int(raw_id))
                                        self.remove_item(int(raw_id))
                                        self.checks += 1
                                        t1 = asyncio.get_event_loop().time()
                                        self.last_time = round(t1 - self.t0, 3)
                                        if not self.expensive_price:
                                            continue

                                        await self.embed_item_info(
                                            webhook=self.webhookBought,
                                            item_id=raw_id,
                                            name=item_name,
                                            price=price,
                                            total=totalQuantity,
                                            limit=quantityLimitPerUser,
                                            message=f"Expensive Price",
                                            username=None,
                                            user_id=None,
                                            discord_id=None,
                                            thumbnail=None,
                                            assetType=None,
                                            purchase_count=None,
                                            headers=None,
                                            cookies=None,
                                            method="Watcher"
                                        )
                                        continue

                                    if not (i.get("priceStatus") != "Off Sale" and i.get('unitsAvailableForConsumption', 0) > 0):
                                        if i.get('unitsAvailableForConsumption', 1) == 0:
                                            print(f"{await self.get_time()} Watcher | {item_name} | {raw_id} | Off sale")
                                            self.soldOut.append(int(raw_id))
                                            self.remove_item(int(raw_id))
                                            self.checks += 1
                                            t1 = asyncio.get_event_loop().time()
                                            self.last_time = round(t1 - self.t0, 3)
                                            if not self.offsale:
                                                continue

                                            await self.embed_item_info(
                                                webhook=self.webhookBought,
                                                item_id=raw_id,
                                                name=item_name,
                                                price=price,
                                                total=totalQuantity,
                                                limit=quantityLimitPerUser,
                                                message="Off Sale",
                                                username=None,
                                                user_id=None,
                                                discord_id=None,
                                                thumbnail=None,
                                                assetType=None,
                                                purchase_count=None,
                                                headers=None,
                                                cookies=None,
                                                method="Watcher"
                                                )
                                        continue

                                    await self.ratelimit.take(1)
                                    async with await session.post("https://apis.roblox.com/marketplace-items/v1/items/details",
                                        json={"itemIds": [collectibleItemId]},
                                        headers={"x-csrf-token": currentAccount["xcsrf_token"],
                                                    'Accept': "application/json",
                                                    "Accept-Encoding": "gzip, deflate"},
                                        cookies={".ROBLOSECURITY": currentAccount["cookie"]},
                                        ssl=False) as productid_response:

                                        productid_response.raise_for_status()

                                        productid_text = await productid_response.text()

                                        productid_data = json.loads(productid_text)[0]['collectibleProductId']

                                        await self.new_item({
                                            'item_id': collectibleItemId,
                                            'item_name': item_name,
                                            'price': price,
                                            'totalQuantity': totalQuantity,
                                            'quantityLimitPerUser': quantityLimitPerUser,
                                            'creator_id': creator,
                                            'product_id': productid_data,
                                            'raw_id': raw_id,
                                            'assetType': assetType
                                        })
                                        
                                        print(f"{await self.get_time()} Watcher | {item_name} | {raw_id} | Buying item")

                                        coroutines = [
                                            self.buy_item(
                                                account=f"{i+1}",
                                                item_id=collectibleItemId,
                                                item_name=item_name,
                                                price=price,
                                                totalQuantity=totalQuantity,
                                                quantityLimitPerUser=quantityLimitPerUser,
                                                creator_id=creator,
                                                product_id=productid_data,
                                                raw_id=raw_id,
                                                assetType=assetType,
                                                method="Watcher"
                                            ) for i, _ in enumerate(self.accounts) for _ in range(1)
                                        ]

                                    await asyncio.gather(*coroutines)

                    except aiohttp.ClientConnectorError as e:
                        self.errors += 1
                    except AssertionError as e:
                        continue
                    except aiohttp.ContentTypeError as e:
                        self.errors += 1
                    except aiohttp.ClientResponseError as e:
                        status_code = int(str(e).split(',')[0])
                        if status_code == 429:
                            await asyncio.sleep(0.5)
                    except asyncio.CancelledError:
                        return
                    except asyncio.TimeoutError as e:
                        self.errors += 1
                    except aiohttp.ServerDisconnectedError:
                        return
                    finally:
                        if len(self.items) != 0:
                            self.checks += len(self.items)
                            t1 = asyncio.get_event_loop().time()
                            self.last_time = round(t1 - self.t0, 3)
                        await asyncio.sleep(1)

    async def buy_item(
        self,
        account: str,
        item_id: int,
        item_name: str,
        price: int,
        totalQuantity: int,
        quantityLimitPerUser: int,
        creator_id: int,
        product_id: int,
        raw_id: int,
        assetType: int,
        method: str
    ) -> None:

        if int(raw_id) in self.soldOut:
            return
        
        self.soldOut.append(int(raw_id))
        self.remove_item(int(raw_id))

        user = self.accounts[account]

        user_id = user['id']
        cookie = user['cookie']
        x_token = user['xcsrf_token']

        data = {
            "collectibleItemId": item_id,
            "expectedCurrency": 1,
            "expectedPrice": price,
            "expectedPurchaserId": user_id,
            "expectedPurchaserType": "User",
            "expectedSellerId": creator_id,
            "expectedSellerType": "User",
            "idempotencyKey": "",
            "collectibleProductId": product_id
        }

        async with aiohttp.ClientSession() as client:
            while True:

                data["idempotencyKey"] = str(uuid.uuid4())

                async with client.post(f"https://apis.roblox.com/marketplace-sales/v1/item/{item_id}/purchase-item",
                                json=data,
                                headers={"Accept-Encoding": "gzip, deflate",
                                            "x-csrf-token": x_token},
                                cookies={".ROBLOSECURITY": cookie},
                                ssl=False) as response:

                    if response.status == 429:
                        await asyncio.sleep(0.5)
                        continue

                    try:
                        json_response = await response.json()
                    except aiohttp.ContentTypeError as e:
                        self.errors += 1
                        continue

                    if json_response["purchaseResult"] == "Purchase transaction is failed, Robux will be rolled back soon.":
                        print(f"{await self.get_time()} {user['displayName']} (@{user['name']}) | {item_name} | Robux will be rolled back soon lmao")

                    if json_response["errorMessage"] == "QuantityExhausted":
                        self.soldOut.append(int(raw_id))
                        self.remove_item(int(raw_id))

                        if user['purchase_count'] == 0:
                            print(f"{await self.get_time()} {method} | {item_name} | {raw_id} Sold out")

                            return await self.embed_item_info(
                                webhook=self.webhookBought,
                                item_id=raw_id,
                                name=item_name,
                                price=price,
                                total=totalQuantity,
                                limit=quantityLimitPerUser,
                                message="Sold out",
                                username=f"{user['displayName']} (@{user['name']})",
                                user_id=user['id'],
                                discord_id=user['user_id'],
                                thumbnail=user['thumbnail'],
                                assetType=None,
                                purchase_count=user['purchase_count'],
                                headers={"x-csrf-token": x_token},
                                cookies={".ROBLOSECURITY": cookie},
                                method=method
                            )

                        break

                    if not json_response["purchased"]:
                        self.errors += 1

                    else:
                        user['purchase_count'] += 1
                        self.buys += 1

                        if user_id not in self.logs:
                            self.logs[user_id] = {"items": {}}
                        if raw_id in self.logs[user_id]["items"]:
                            self.logs[user_id]["items"][raw_id]["bought"] = user['purchase_count']
                        else:
                            self.logs[user_id]["items"][raw_id] = {"name": item_name, "bought": user['purchase_count'], "serials": []}

                        print(f"{await self.get_time()} {user['displayName']} (@{user['name']}) | Bought {item_name}")

                        self.on_bought(raw_id)

                        if quantityLimitPerUser > 0 and user['purchase_count'] >= quantityLimitPerUser:
                            self.soldOut.append(int(raw_id))
                            self.remove_item(int(raw_id))

                            await self.embed_item_info(
                                webhook=self.webhookBought,
                                item_id=raw_id,
                                name=item_name,
                                price=price,
                                total=totalQuantity,
                                limit=quantityLimitPerUser,
                                message=f"Purchased: {user['purchase_count']}x",
                                username=f"{user['displayName']} (@{user['name']})",
                                user_id=user['id'],
                                discord_id=user['user_id'],
                                thumbnail=user['thumbnail'],
                                assetType=assetType,
                                purchase_count=user['purchase_count'],
                                headers={"x-csrf-token": x_token},
                                cookies={".ROBLOSECURITY": cookie},
                                method=method
                            )

                            user['purchase_count'] = 0
                            break


    async def start(self):
            coroutines = []
            coroutines.append(self.connect_websocket())
            coroutines.append(self.given_id_sniper())
            coroutines.append(self.auto_xtoken())
            await asyncio.gather(*coroutines)

    def _load_items(self) -> list:
        return self.config["items"]

Sniper()
