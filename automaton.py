import os.path
import sys
import enum
import time
import random
import getpass
import logging
import threading

logging.basicConfig(format='[%(asctime)s] %(name)s: %(levelname)s: %(message)s', level=logging.INFO)

try:
  import requests
except ImportError:
  logging.error("Package `requests` is required.")
  
  sys.exit(1)

class TaskType(enum.Enum):
  BUY = 1
  CHAIN = 2

class Task:
  def __init__(self, type, *args):
    self.type = type
    self.args = args

class SlavesGame:
  def __init__(self, login=None, password=None, token=None): 
    self.GAME_SERVER_URL = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0"

    if login is None and token is None:
      raise Exception()

    self.access_token = self.auth(login, password) if token is None else token
    
    self.application_url, self.authorization_data = self.get_auth_data()

    self.application_url = self.application_url[:-11]

  def auth(self, login, password):
    url = f"https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}"

    response = requests.get(url).json()
import os.path
import sys
import enum
import time
import random
import getpass
import logging
import threading

logging.basicConfig(format='[%(asctime)s] %(name)s: %(levelname)s: %(message)s', level=logging.INFO)

try:
  import requests
except ImportError:
  logging.error("Package `requests` is required.")
  
  sys.exit(1)

class TaskType(enum.Enum):
  BUY = 1
  CHAIN = 2

class Task:
  def __init__(self, type, *args):
    self.type = type
    self.args = args

class SlavesGame:
  def __init__(self, login=None, password=None, token=None): 
    self.GAME_SERVER_URL = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0"

    if login is None and token is None:
      raise Exception()

    self.access_token = self.auth(login, password) if token is None else token
    
    self.application_url, self.authorization_data = self.get_auth_data()

    self.application_url = self.application_url[:-11]

  def auth(self, login, password):
    url = f"https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}"

    response = requests.get(url).json()

    return response["access_token"]

  def get_auth_data(self):
    url = f"https://api.vk.com/method/execute.resolveScreenName?access_token={self.access_token}&v=5.55&screen_name=app7794757_522020267&owner_id=-176897109&func_v=3"

    response = requests.get(url).json()

    return response["response"]["object"]["mobile_iframe_url"].split("?")
 
  def get(self, data):
    url = f"{self.GAME_SERVER_URL}/{data}"

    response = requests.get(url, headers={"Authorization": f"Bearer {self.authorization_data}", "User-Agent": "Dont ban plz ;3"}).json()

    return response

  def post(self, method, data={}):
    url = f"{self.GAME_SERVER_URL}/{method}"

    response = requests.post(url, json=data, headers={"Authorization": f"Bearer {self.authorization_data}", "User-Agent": "Dont ban plz ;3"}).json()

    return response

  def start(self):
    return self.get("start")

  def users(self, ids):
    return self.post("user", {"ids": ids})

  def top_users(self):
    return self.get("topUsers")  

  def buy_slave(self, id):
    return self.post("buySlave", {"slave_id": id})

  def set_job(self, id, job):
    return self.post("jobSlave", {"slave_id": id, "name": job})

  def user_info(self, id):
    return self.get(f"user?id={id}")

  def buy_fetter(self, id):
    return self.post("buyFetter", {"slave_id": id})

  def sell_slave(self, id):
    return self.post("saleSlave", {"slave_id": id}) 

class Automaton:
  def __init__(self, credentials):
    logging.info("Creating a new Game instance.")

    if type(credentials) is str:
      self.game = SlavesGame(token=credentials)
    else:
      self.game = SlavesGame(login=credentials[0], password=credentials[1])

    logging.info("Game instance created.")
      
    self.ids = []
    self.balance = []
    self.my_id = 0
    self.tasks = []
    self.busy = threading.Event()

    self.interval = 30
    self.cooldown = 1.5
    self.attempts = 3

    self.job = "Ave SPAM!"

  @property
  def is_busy(self):
    return self.busy.is_set()
     
  def fetch_ids(self):
    logging.info("Fetching some ids...")
    
    offset = 0
    while True:
      response = requests.get(f"https://api.vk.com/method/friends.get?offset={offset if offset != 0 else 1}&order=random&access_token={self.game.access_token}&v=5.130").json()
      items = response["response"]["items"]
      self.ids.extend(items)

      if len(items) < 5000:
        break

      offset += 5000

    offset = 0
    while True:
      response = requests.get(f"https://api.vk.com/method/users.getFollowers?offset={offset if offset != 0 else 1}&count=1000&access_token={self.game.access_token}&v=5.130").json()
      items = response["response"]["items"]
      self.ids.extend(items)

      if len(items) < 1000:
        break

      offset += 1000

    offset = 0
    while True:
      response = requests.get(f"https://api.vk.com/method/groups.get?offset={offset if offset != 0 else 1}&extended=0&count=1000&access_token={self.game.access_token}&v=5.130").json()
      items = response["response"]["items"]
      self.ids.extend(items)

      if len(items) < 1000:
        break

      offset += 1000
   
    logging.info(f"Fetched {len(self.ids)} id(s).")

  def task_generator(self):
    logging.info("Starting task generator!")

    while True:
      if self.is_busy:
        logging.info(f"Main thread is busy, so task generator is sleeping for {self.interval} second(s)...")

        time.sleep(self.interval)

        continue

      logging.info("Updating game statistics...")

      data = self.game.start()
      balance = data["me"]["balance"]
      my_slaves = data["slaves"]

      logging.info(f"Balance: {balance}.")
      logging.info(f"Slaves count: {len(my_slaves)}.")

      logging.info("Searching for slaves which should be chained again...")
    
      count = 0
      total_price = 0

      for slave in sorted(filter(lambda slave: slave["fetter_to"] == 0 and slave["master_id"] == self.my_id, my_slaves), key=lambda slave: slave["fetter_price"]):
        if total_price >= balance:
          break

        if slave["fetter_price"] < balance:
          fetter_price = slave["fetter_price"]

          task = Task(TaskType.CHAIN, slave["id"], fetter_price)

          self.tasks.append(task)

          total_price += fetter_price
 
          count += 1
          
      logging.info(f"Found {count} slave(s).")

      logging.info("Searching for slaves to purchase...")

      try:
        ids = random.sample(self.ids, 100)
      except ValueError:
        ids = self.ids

        logging.warning("Count of users is below 100.")

      users = self.game.users(ids)["users"]

      logging.info(f"Fetched {len(users)} user(s).")

      count = 0
      total_price = 0

      for slave in sorted(filter(lambda slave: slave["price"] + slave["fetter_price"] < balance and slave["master_id"] != self.my_id, users), key=lambda slave: slave["price"] + slave["fetter_price"]):
        if total_price >= balance:
          break 

        if slave["price"] + slave["fetter_price"] < balance: 
          slave_price = slave["price"] + slave["fetter_price"]

          task = Task(TaskType.BUY, slave["id"], slave_price)

          self.tasks.append(task)

          total_price += slave_price

          count += 1

      logging.info(f"Found {count} user(s).")

      random.shuffle(self.tasks)

      logging.info(f"Task generator is sleeping for {self.interval} second(s)...")

      time.sleep(self.interval)

  def chain(self, id):
    logging.info(f"Chaining id{id}!")

    attempts = 0
    while attempts < self.attempts:
      if "error" in self.game.buy_fetter(id):
        logging.error(f"Can't chain id{id}! :(")
        logging.info(f"Attempt {attempts+1} / {self.attempts}!")

        attempts += 1

        if attempts == self.attempts:
          logging.error("Maximum count of attempts reached.")

          return

        time.sleep(self.cooldown)
       
        continue

      break

    logging.info(f"Chained id{id}!")

    time.sleep(self.cooldown)

  def set_job(self, id, job):
    logging.info(f"Setting job for id{id} to `{job}`!")

    attempts = 0
    while attempts < self.attempts:
      if "error" in self.game.set_job(id, job):
        logging.error(f"Can't set job for id{id}! :(")

        logging.info(f"Attempt {attempts+1} / {self.attempts}!")

        attempts += 1

        if attempts == self.attempts:
          logging.error("Maximum count of attempts reached.")

          return

        time.sleep(self.cooldown)
       
        continue

      break   

    logging.info(f"Job was set for id{id}!")

    time.sleep(self.cooldown)

  def buy(self, id):
    logging.info(f"Buying id{id}!")

    attempts = 0
    while attempts < self.attempts:
      if "error" in self.game.buy_slave(id):
        logging.error(f"Can't buy id{id}! :(")

        logging.info(f"Attempt {attempts+1} / {self.attempts}!")

        attempts += 1

        if attempts == self.attempts:
          logging.error("Maximum count of attempts reached.")

          return

        time.sleep(self.cooldown)
       
        continue

      break   

    logging.info(f"Bought id{id}!")

    time.sleep(self.cooldown)

  def start(self):
    logging.info("Starting!")
    logging.info("Fetching my id...")
   
    response = requests.get(f"https://api.vk.com/method/users.get?access_token={self.game.access_token}&v=5.130").json()
    self.my_id = response["response"][0]["id"]
   
    logging.info(f"My id: {self.my_id}.")

    self.fetch_ids()

    task_generator = threading.Thread(target=self.task_generator)
    task_generator.daemon = True
    task_generator.start()   

    while True:
      if len(self.tasks) < 1: 
        continue

      task = self.tasks.pop()

      logging.info(f"There are/is {len(self.tasks)} task(s) pending.")
 
      self.busy.set()

      if task.type == TaskType.CHAIN:
        self.chain(task.args[0])
      elif task.type == TaskType.BUY:
        id = task.args[0]

        self.buy(id)        
        self.set_job(id, self.job)
        self.chain(id)         

      self.busy.clear()
 
logging.info("Authorization!")
     
if os.path.isfile("./.token"):
  logging.info("Reading credentials from `.token` file.")

  with open("./.token", "r") as token_file:
    credentials = token_file.read()
else:
  logging.info("No `.token` file found. Give your credentials.")

  login = input("login: ")
  password = getpass.getpass("password: ")

  credentials = (login, password)

try:
  automaton = Automaton(credentials)
except:
  import traceback
  traceback.print_exc()
  logging.error("Failed to perform authorization.")

  sys.exit(1)

logging.info("Saving token to `.token` file...")
with open("./.token", "w") as token_file:
  token_file.write(automaton.game.access_token)

try:
  automaton.start()
except KeyboardInterrupt:
  logging.info("Interrupted by user.")

  sys.exit(0)
    return response["access_token"]

  def get_auth_data(self):
    url = f"https://api.vk.com/method/execute.resolveScreenName?access_token={self.access_token}&v=5.55&screen_name=app7794757_522020267&owner_id=-176897109&func_v=3"

    response = requests.get(url).json()

    return response["response"]["object"]["mobile_iframe_url"].split("?")
 
  def get(self, data):
    url = f"{self.GAME_SERVER_URL}/{data}"

    response = requests.get(url, headers={"Authorization": f"Bearer {self.authorization_data}", "User-Agent": "Dont ban plz ;3"}).json()

    return response

  def post(self, method, data={}):
    url = f"{self.GAME_SERVER_URL}/{method}"

    response = requests.post(url, json=data, headers={"Authorization": f"Bearer {self.authorization_data}", "User-Agent": "Dont ban plz ;3"}).json()

    return response

  def start(self):
    return self.get("start")

  def users(self, ids):
    return self.post("user", {"ids": ids})

  def top_users(self):
    return self.get("topUsers")  

  def buy_slave(self, id):
    return self.post("buySlave", {"slave_id": id})

  def set_job(self, id, job):
    return self.post("jobSlave", {"slave_id": id, "name": job})

  def user_info(self, id):
    return self.get(f"user?id={id}")

  def buy_fetter(self, id):
    return self.post("buyFetter", {"slave_id": id})

  def sell_slave(self, id):
    return self.post("saleSlave", {"slave_id": id}) 

class Automaton:
  def __init__(self, credentials):
    logging.info("Creating a new Game instance.")

    if type(credentials) is str:
      self.game = SlavesGame(token=credentials)
    else:
      self.game = SlavesGame(login=credentials[0], password=credentials[1])

    logging.info("Game instance created.")
      
    self.ids = []
    self.balance = []
    self.my_id = 0
    self.tasks = []
    self.busy = threading.Event()

    self.interval = 30
    self.cooldown = 1.5
    self.attempts = 3

    self.job = "Ave SPAM!"

  @property
  def is_busy(self):
    return self.busy.is_set()
     
  def fetch_ids(self):
    logging.info("Fetching some ids...")
    
    offset = 0
    while True:
      response = requests.get(f"https://api.vk.com/method/friends.get?offset={offset if offset != 0 else 1}&order=random&access_token={self.game.access_token}&v=5.130").json()
      items = response["response"]["items"]
      self.ids.extend(items)

      if len(items) < 5000:
        break

      offset += 5000

    offset = 0
    while True:
      response = requests.get(f"https://api.vk.com/method/users.getFollowers?offset={offset if offset != 0 else 1}&count=1000&access_token={self.game.access_token}&v=5.130").json()
      items = response["response"]["items"]
      self.ids.extend(items)

      if len(items) < 1000:
        break

      offset += 1000

    offset = 0
    while True:
      response = requests.get(f"https://api.vk.com/method/groups.get?offset={offset if offset != 0 else 1}&extended=0&count=1000&access_token={self.game.access_token}&v=5.130").json()
      items = response["response"]["items"]
      self.ids.extend(items)

      if len(items) < 1000:
        break

      offset += 1000
   
    logging.info(f"Fetched {len(self.ids)} id(s).")

  def task_generator(self):
    logging.info("Starting task generator!")

    while True:
      if self.is_busy:
        logging.info(f"Main thread is busy, so task generator is sleeping for {self.interval} second(s)...")

        time.sleep(self.interval)

        continue

      logging.info("Updating game statistics...")

      data = self.game.start()
      balance = data["me"]["balance"]
      my_slaves = data["slaves"]

      logging.info(f"Balance: {balance}.")
      logging.info(f"Slaves count: {len(my_slaves)}.")

      logging.info("Searching for slaves which should be chained again...")
    
      count = 0
      total_price = 0

      for slave in sorted(filter(lambda slave: slave["fetter_to"] == 0 and slave["master_id"] == self.my_id, my_slaves), key=lambda slave: slave["fetter_price"]):
        if total_price >= balance:
          break

        if slave["fetter_price"] < balance:
          fetter_price = slave["fetter_price"]

          task = Task(TaskType.CHAIN, slave["id"], fetter_price)

          self.tasks.append(task)

          total_price += fetter_price
 
          count += 1
          
      logging.info(f"Found {count} slave(s).")

      logging.info("Searching for slaves to purchase...")

      try:
        ids = random.sample(self.ids, 100)
      except ValueError:
        ids = self.ids

        logging.warning("Count of users is below 100.")

      users = self.game.users(ids)["users"]

      logging.info(f"Fetched {len(users)} user(s).")

      count = 0
      total_price = 0

      for slave in sorted(filter(lambda slave: slave["price"] + slave["fetter_price"] < balance and slave["master_id"] != self.my_id, users), key=lambda slave: slave["price"] + slave["fetter_price"]):
        if total_price >= balance:
          break 

        if slave["price"] + slave["fetter_price"] < balance: 
          slave_price = slave["price"] + slave["fetter_price"]

          task = Task(TaskType.BUY, slave["id"], slave_price)

          self.tasks.append(task)

          total_price += slave_price

          count += 1

      logging.info(f"Found {count} user(s).")

      random.shuffle(self.tasks)

      logging.info(f"Task generator is sleeping for {self.interval} second(s)...")

      time.sleep(self.interval)

  def chain(self, id):
    logging.info(f"Chaining id{id}!")

    attempts = 0
    while attempts < 3:
      if "error" in self.game.buy_fetter(id):
        logging.error(f"Can't chain id{id}! :(")
        logging.info(f"Attempt {attempts+1} / {self.attempts}!")

        attempts += 1

        time.sleep(self.cooldown)
       
        continue

      break

    logging.info(f"Chained id{id}!")

    time.sleep(self.cooldown)

  def set_job(self, id, job):
    logging.info(f"Setting job for id{id} to `{job}`!")

    attempts = 0
    while attempts < 3:
      if "error" in self.game.set_job(id, job):
        logging.error(f"Can't set job for id{id}! :(")

        logging.info(f"Attempt {attempts+1} / {self.attempts}!")

        attempts += 1

        time.sleep(self.cooldown)
       
        continue

      break   

    logging.info(f"Job was set for id{id}!")

    time.sleep(self.cooldown)

  def buy(self, id):
    logging.info(f"Buying id{id}!")

    attempts = 0
    while attempts < 3:
      if "error" in self.game.buy_slave(id):
        logging.error(f"Can't buy id{id}! :(")

        logging.info(f"Attempt {attempts+1} / {self.attempts}!")

        attempts += 1

        time.sleep(self.cooldown)
       
        continue

      break   

    logging.info(f"Bought id{id}!")

    time.sleep(self.cooldown)

  def start(self):
    logging.info("Starting!")
    logging.info("Fetching my id...")
   
    response = requests.get(f"https://api.vk.com/method/users.get?access_token={self.game.access_token}&v=5.130").json()
    self.my_id = response["response"][0]["id"]
   
    logging.info(f"My id: {self.my_id}.")

    self.fetch_ids()

    task_generator = threading.Thread(target=self.task_generator)
    task_generator.daemon = True
    task_generator.start()   

    while True:
      if len(self.tasks) < 1: 
        continue

      task = self.tasks.pop()

      logging.info(f"There are/is {len(self.tasks)} task(s) pending.")
 
      self.busy.set()

      if task.type == TaskType.CHAIN:
        self.chain(task.args[0])
      elif task.type == TaskType.BUY:
        id = task.args[0]

        self.buy(id)        
        self.set_job(id, self.job)
        self.chain(id)         

      self.busy.clear()
 
logging.info("Authorization!")
     
if os.path.isfile("./.token"):
  logging.info("Reading credentials from `.token` file.")

  with open("./.token", "r") as token_file:
    credentials = token_file.read()
else:
  logging.info("No `.token` file found. Give your credentials.")

  login = input("login: ")
  password = getpass.getpass("password: ")

  credentials = (login, password)

try:
  automaton = Automaton(credentials)
except:
  logging.error("Failed to perform authorization.")

  sys.exit(1)

logging.info("Saving token to `.token` file...")
with open("./.token", "w") as token_file:
  token_file.write(automaton.game.access_token)

try:
  automaton.start()
except KeyboardInterrupt:
  logging.info("Interrupted by user.")

  sys.exit(0)
