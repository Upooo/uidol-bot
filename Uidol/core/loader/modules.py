"""
Auto Module Loader for Uidol.
Just drop a .py file inside Uidol/modules/ and it will be loaded automatically.
Each module can optionally expose a `register(bot)` function.
"""

import importlib
import pkgutil
from pathlib import Path
from typing import List, Any
from Uidol.core.logger import log


def load_modules(bot: Any = None) -> List[str]:
    """
    Discover and import all modules inside Uidol.modules package.
    If a module has a `register(bot)` function and bot is provided, call it.
    Returns list of successfully loaded module names.
    """
    loaded = []
    package_name = "Uidol.modules"
    package_path = Path(__file__).resolve().parent.parent.parent / "modules"

    if not package_path.exists():
        log.warning("Modules directory not found")
        return loaded

    for module_info in pkgutil.iter_modules([str(package_path)]):
        name = module_info.name
        if name.startswith("_"):
            continue

        full_name = f"{package_name}.{name}"
        try:
            mod = importlib.import_module(full_name)
            loaded.append(name)
            log.info(f"Module loaded: {name}")

            # Auto-register if the module provides a register function
            if bot is not None and hasattr(mod, "register") and callable(mod.register):
                mod.register(bot)
                log.info(f"Module registered: {name}")

        except Exception as e:
            log.error(f"Failed to load module {name}: {e}")

    return loaded
