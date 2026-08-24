"""
Auto Module Loader.
- Bot modules: register(bot)
- Userbot modules: register_userbot(client)
"""

import importlib
import pkgutil
from pathlib import Path
from typing import List, Any, Callable
from Uidol.core.logger import log

_loaded_modules: List[Any] = []


def load_modules(bot: Any = None) -> List[str]:
    global _loaded_modules
    loaded_names = []
    package_name = "Uidol.modules"
    package_path = Path(__file__).resolve().parent.parent.parent / "modules"

    if not package_path.exists():
        log.warning("Modules directory not found")
        return loaded_names

    _loaded_modules = []

    for module_info in pkgutil.iter_modules([str(package_path)]):
        name = module_info.name
        if name.startswith("_"):
            continue

        full_name = f"{package_name}.{name}"
        try:
            mod = importlib.import_module(full_name)
            _loaded_modules.append(mod)
            loaded_names.append(name)
            log.info(f"Module loaded: {name}")

            if bot is not None and hasattr(mod, "register") and callable(mod.register):
                mod.register(bot)
                log.info(f"Module registered (bot): {name}")

        except Exception as e:
            log.error(f"Failed to load module {name}: {e}")

    return loaded_names


def register_userbot_modules(userbot: Any) -> None:
    for mod in _loaded_modules:
        if hasattr(mod, "register_userbot") and callable(mod.register_userbot):
            try:
                mod.register_userbot(userbot)
            except Exception as e:
                log.error(f"register_userbot failed in {mod.__name__}: {e}")


def get_userbot_register_hook() -> Callable:
    return register_userbot_modules
