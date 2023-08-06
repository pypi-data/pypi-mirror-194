if __name__ == "__main__":
    from config import Config
else:
    from .config import Config

custom_cfg = {
    "pig": {
        "default": None,
        "flags": ["--pig", "-p"],
        "help": "piggy options",
        "nargs": 1
    },
    "cat": {
        "default": "tintin",
        "flags": ["--cat", "-c"],
        "help": "catty option",
        "nargs": 1
    }
}

cfg = Config(custom_entries=custom_cfg)

for k in cfg:
    v = cfg[k]
    print(f"{k}: {v}") 


if cfg["hs_api_key"] == None:
    print('api key is none')

if "hs_api_key" in cfg:
    print('is in config')

print("cat flags:", cfg.get_flags("cat"))
print("cat help:", cfg.get_help("cat"))
print("cat nargs:", cfg.get_nargs("cat"))


