import re
from typing import List, Iterable, Dict, Tuple, Match, Optional

from i3ipc import Event
from i3ipc.aio import Connection, Con
from i3ipc.events import IpcBaseEvent, WindowEvent

from .config import Config, Symbol, ClientConfig


class Watcher:
    i3: Connection

    def __init__(self, config: Config):
        self.config = config
        self.commands = []

    async def start(self):
        self.i3 = await Connection().connect()
        for case in [Event.WINDOW_MOVE, Event.WINDOW_NEW, Event.WINDOW_TITLE, Event.WINDOW_CLOSE]:
            self.i3.on(case, self.callback)
        await self.rename_all()
        await self.i3.main()

    async def callback(self, conn: Connection, event: IpcBaseEvent):
        if event.change == 'new':
            await self.handle_move(event.container)
        await self.rename_all()

    async def handle_move(self, window: Con):
        conf, _ = self.get_config(window)
        if conf is None or not conf.new_desktop:
            return
        match_identity = conf.match_identity(window)
        tree = await self.i3.get_tree()
        workspaces = tree.workspaces()
        possible_targets = set()
        current_workspace = None
        for workspace in workspaces:
            for leaf in workspace.leaves():
                if leaf.id == window.id:
                    current_workspace = workspace
                    continue
                leaf_conf, _ = self.get_config(leaf)
                if leaf_conf and leaf_conf.match_identity(leaf) == match_identity:
                    possible_targets.add(workspace)
        if current_workspace in possible_targets:
            return
        if possible_targets:
            target = possible_targets.pop()
            await self.i3.command(f'[con_id={window.id}] move container to workspace {target.name}; [con_id={window.id}] focus')

    async def rename_all(self):
        tree = await self.i3.get_tree()
        workspaces = tree.workspaces()
        workspace_symbols: Dict[Con, List[Symbol]] = {w: list(self.get_symbols(w)) for w in workspaces}
        workspace_icons = self.compute_workspace_icons(workspace_symbols)
        for num, workspace in enumerate(workspace_icons.keys()):
            await self.rename_workspace(workspace, num, workspace_icons[workspace])
        await self.commit()

    async def rename_workspace(self, workspace: Con, num: int, new_name: str):
        new_name = f"{num}:{new_name}"
        if workspace.name != new_name:
            workspace_name_san = workspace.name.replace('"', '\\"')
            new_name_san = new_name.replace('"', '\\"')
            self.commands.append(f'rename workspace "{workspace_name_san}" to "{new_name_san}"')

    def compute_workspace_icons(self, workspace_symbols: Dict[Con, List[Symbol]]) -> Dict[Con, str]:
        workspace_icons: Dict[Con, List[str]] = {}
        for workspace, symbols in workspace_symbols.items():
            other_symbols = [ss for w, ss in workspace_symbols.items() if w is not workspace]
            workspace_icons[workspace] = [s.get(other_symbols) for s in symbols]
        for workspace, icons in workspace_icons.items():
            if not icons:
                icons.append(self.config.default_icon)
        return {workspace: self.config.delimiter.join(set(icons)) for workspace, icons in workspace_icons.items()}

    def get_symbols(self, workspace: Con):
        for leaf in workspace.leaves():
            leaf_symbol = self.get_symbol(leaf)
            if leaf_symbol:
                yield leaf_symbol

    def get_symbol(self, leaf: Con):
        conf, match = self.get_config(leaf)
        if conf is None:
            return None
        return conf.get_symbol(leaf, match)

    def get_config(self, leaf: Con) -> Tuple[Optional[ClientConfig], Optional[Match[str]]]:
        for conf in self.config.client_configs.values():
            match = conf.match(leaf)
            if match:
                return conf, match
        return None, None

    async def commit(self):
        await self.i3.command(u';'.join(self.commands))
        self.commands = []


async def start():
    config = Config()
    watcher = Watcher(config)
    await watcher.start()
