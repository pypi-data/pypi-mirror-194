<h1 align="center">Stable Ethereum RPC</h1>

### Reference
- [Installation](#installation)
- [Usage](#usage)

---

### Installation <a name="installation"></a>

```shell
pip install stable-ethereum-rpc
```

### Usage <a name="usage"></a>

- The simplest example is using [StableWeb3](https://github.com/phamhongphuc1999/stable-ethereum-rpc/blob/main/src/stable_ethereum_rpc/stable_web3/__init__.py)

```python
raw_web3_list = [
    "https://bsc-dataseed.binance.org",
    "https://bsc-dataseed1.binance.org",
    "https://bsc-dataseed1.defibit.io",
    "https://bsc-dataseed2.defibit.io",
    "https://bsc-dataseed1.ninicoin.io",
    "https://bsc-dataseed2.ninicoin.io",
]

def web3_callback_func(web3: Web3Entity, params: object):
    print(f"web3: {web3.provider_url}, result: {params}")

stable_web3 = StableWeb3(web3_list=raw_web3_list, func=web3_callback_func)
print(f"rpc: {stable_web3.web3_entity().provider_url}")
time.sleep(10)
print("Set best web3=========================================")
result1 = stable_web3.set_best_web3(func=web3_callback_func)
_message = f"RPC: {result1['rpc'].provider_url}"
if "currentRpc" in result1:
    _message += f", Current RPC: {result1['currentRpc'].provider_url}"
print(_message)
time.sleep(10)
print("set sufficient web3=========================================")
result = stable_web3.set_sufficient_web3(func=web3_callback_func)
_message = f"RPC: {result['rpc'].provider_url}"
if "currentRpc" in result:
    _message += f", Current RPC: {result['currentRpc'].provider_url}"
print(_message)
```

- You can see complete example in [here](https://github.com/phamhongphuc1999/stable-ethereum-rpc/blob/main/example/simple.py)

- We still support to schedule to check web3

```python
stable_web3 = AvailableStableWeb3(
    web3_list=raw_web3_list,
    func=web3_callback_func,
    callback_func=available_callback_func,
    job_mode="best"
)
print(f"rpc: {stable_web3.web3().provider_url}")
stable_web3.run_job(trigger="interval", args=[], seconds=30, max_instances=2)
signal.pause()
```

- You can see complete example in [here](https://github.com/phamhongphuc1999/stable-ethereum-rpc/blob/main/example/available_example.py)
