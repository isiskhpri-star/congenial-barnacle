"""Krita artist workspace database module.

Provides a SQLite database and Python API for managing Krita artist
workspace data including projects, brushes, palettes, color entries,
layers, and workspace configurations.
"""

import sqlite3
import json
import os
from datetime import datetime, timezone
from typing import Any, Optional


DB_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "krita_workspace.db")


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    file_path   TEXT,
    width       INTEGER,
    height      INTEGER,
    dpi         INTEGER DEFAULT 300,
    color_space TEXT    DEFAULT 'RGBA',
    created_at  TEXT    NOT NULL,
    updated_at  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS brushes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    category    TEXT,
    size        REAL,
    opacity     REAL    DEFAULT 1.0,
    flow        REAL    DEFAULT 1.0,
    blend_mode  TEXT    DEFAULT 'normal',
    settings    TEXT,
    created_at  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS palettes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT,
    created_at  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS palette_colors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    palette_id  INTEGER NOT NULL,
    name        TEXT,
    hex_color   TEXT    NOT NULL,
    position    INTEGER DEFAULT 0,
    FOREIGN KEY (palette_id) REFERENCES palettes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS layers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    layer_type  TEXT    DEFAULT 'paint',
    visible     INTEGER DEFAULT 1,
    locked      INTEGER DEFAULT 0,
    opacity     REAL    DEFAULT 1.0,
    blend_mode  TEXT    DEFAULT 'normal',
    position    INTEGER DEFAULT 0,
    parent_id   INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id)  REFERENCES layers(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS workspaces (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT,
    config      TEXT,
    created_at  TEXT    NOT NULL,
    updated_at  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS tags (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS brush_tags (
    brush_id INTEGER NOT NULL,
    tag_id   INTEGER NOT NULL,
    PRIMARY KEY (brush_id, tag_id),
    FOREIGN KEY (brush_id) REFERENCES brushes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)   REFERENCES tags(id) ON DELETE CASCADE
);
"""


# ---------------------------------------------------------------------------
# Database connection helper
# ---------------------------------------------------------------------------

class KritaDB:
    """Interface to a Krita artist workspace SQLite database."""

    def __init__(self, db_path: str = DB_DEFAULT_PATH) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(SCHEMA_SQL)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # -- generic helpers ----------------------------------------------------

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _row_to_dict(self, row: sqlite3.Row) -> dict:
        return dict(row)

    def _rows_to_list(self, rows: list[sqlite3.Row]) -> list[dict]:
        return [dict(r) for r in rows]

    # -----------------------------------------------------------------------
    # Projects
    # -----------------------------------------------------------------------

    def create_project(
        self,
        name: str,
        file_path: Optional[str] = None,
        width: int = 1920,
        height: int = 1080,
        dpi: int = 300,
        color_space: str = "RGBA",
    ) -> dict:
        now = self._now()
        cur = self.conn.execute(
            """INSERT INTO projects (name, file_path, width, height, dpi,
               color_space, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, file_path, width, height, dpi, color_space, now, now),
        )
        self.conn.commit()
        return self.get_project(cur.lastrowid)

    def get_project(self, project_id: int) -> Optional[dict]:
        row = self.conn.execute(
            "SELECT * FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        return self._row_to_dict(row) if row else None

    def list_projects(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM projects ORDER BY updated_at DESC"
        ).fetchall()
        return self._rows_to_list(rows)

    def update_project(self, project_id: int, **kwargs: Any) -> Optional[dict]:
        allowed = {"name", "file_path", "width", "height", "dpi", "color_space"}
        fields = {k: v for k, v in kwargs.items() if k in allowed}
        if not fields:
            return self.get_project(project_id)
        fields["updated_at"] = self._now()
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [project_id]
        self.conn.execute(
            f"UPDATE projects SET {set_clause} WHERE id = ?", values
        )
        self.conn.commit()
        return self.get_project(project_id)

    def delete_project(self, project_id: int) -> bool:
        cur = self.conn.execute(
            "DELETE FROM projects WHERE id = ?", (project_id,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    # -----------------------------------------------------------------------
    # Brushes
    # -----------------------------------------------------------------------

    def create_brush(
        self,
        name: str,
        category: Optional[str] = None,
        size: Optional[float] = None,
        opacity: float = 1.0,
        flow: float = 1.0,
        blend_mode: str = "normal",
        settings: Optional[dict] = None,
    ) -> dict:
        now = self._now()
        settings_json = json.dumps(settings) if settings else None
        cur = self.conn.execute(
            """INSERT INTO brushes (name, category, size, opacity, flow,
               blend_mode, settings, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, category, size, opacity, flow, blend_mode, settings_json, now),
        )
        self.conn.commit()
        return self.get_brush(cur.lastrowid)

    def get_brush(self, brush_id: int) -> Optional[dict]:
        row = self.conn.execute(
            "SELECT * FROM brushes WHERE id = ?", (brush_id,)
        ).fetchone()
        if not row:
            return None
        d = self._row_to_dict(row)
        if d.get("settings"):
            d["settings"] = json.loads(d["settings"])
        return d

    def list_brushes(self, category: Optional[str] = None) -> list[dict]:
        if category:
            rows = self.conn.execute(
                "SELECT * FROM brushes WHERE category = ? ORDER BY name",
                (category,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM brushes ORDER BY name"
            ).fetchall()
        result = self._rows_to_list(rows)
        for d in result:
            if d.get("settings"):
                d["settings"] = json.loads(d["settings"])
        return result

    def delete_brush(self, brush_id: int) -> bool:
        cur = self.conn.execute(
            "DELETE FROM brushes WHERE id = ?", (brush_id,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    # -----------------------------------------------------------------------
    # Palettes & colors
    # -----------------------------------------------------------------------

    def create_palette(self, name: str, description: Optional[str] = None) -> dict:
        now = self._now()
        cur = self.conn.execute(
            "INSERT INTO palettes (name, description, created_at) VALUES (?, ?, ?)",
            (name, description, now),
        )
        self.conn.commit()
        return self.get_palette(cur.lastrowid)

    def get_palette(self, palette_id: int) -> Optional[dict]:
        row = self.conn.execute(
            "SELECT * FROM palettes WHERE id = ?", (palette_id,)
        ).fetchone()
        if not row:
            return None
        d = self._row_to_dict(row)
        d["colors"] = self._get_palette_colors(palette_id)
        return d

    def list_palettes(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM palettes ORDER BY name"
        ).fetchall()
        return self._rows_to_list(rows)

    def delete_palette(self, palette_id: int) -> bool:
        cur = self.conn.execute(
            "DELETE FROM palettes WHERE id = ?", (palette_id,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def add_palette_color(
        self,
        palette_id: int,
        hex_color: str,
        name: Optional[str] = None,
        position: int = 0,
    ) -> dict:
        cur = self.conn.execute(
            """INSERT INTO palette_colors (palette_id, name, hex_color, position)
               VALUES (?, ?, ?, ?)""",
            (palette_id, name, hex_color, position),
        )
        self.conn.commit()
        return self._row_to_dict(
            self.conn.execute(
                "SELECT * FROM palette_colors WHERE id = ?", (cur.lastrowid,)
            ).fetchone()
        )

    def _get_palette_colors(self, palette_id: int) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM palette_colors WHERE palette_id = ? ORDER BY position",
            (palette_id,),
        ).fetchall()
        return self._rows_to_list(rows)

    # -----------------------------------------------------------------------
    # Layers
    # -----------------------------------------------------------------------

    def create_layer(
        self,
        project_id: int,
        name: str,
        layer_type: str = "paint",
        visible: bool = True,
        locked: bool = False,
        opacity: float = 1.0,
        blend_mode: str = "normal",
        position: int = 0,
        parent_id: Optional[int] = None,
    ) -> dict:
        cur = self.conn.execute(
            """INSERT INTO layers (project_id, name, layer_type, visible, locked,
               opacity, blend_mode, position, parent_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (project_id, name, layer_type, int(visible), int(locked),
             opacity, blend_mode, position, parent_id),
        )
        self.conn.commit()
        return self.get_layer(cur.lastrowid)

    def get_layer(self, layer_id: int) -> Optional[dict]:
        row = self.conn.execute(
            "SELECT * FROM layers WHERE id = ?", (layer_id,)
        ).fetchone()
        return self._row_to_dict(row) if row else None

    def list_layers(self, project_id: int) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM layers WHERE project_id = ? ORDER BY position",
            (project_id,),
        ).fetchall()
        return self._rows_to_list(rows)

    def delete_layer(self, layer_id: int) -> bool:
        cur = self.conn.execute(
            "DELETE FROM layers WHERE id = ?", (layer_id,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    # -----------------------------------------------------------------------
    # Workspaces
    # -----------------------------------------------------------------------

    def create_workspace(
        self,
        name: str,
        description: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> dict:
        now = self._now()
        config_json = json.dumps(config) if config else None
        cur = self.conn.execute(
            """INSERT INTO workspaces (name, description, config,
               created_at, updated_at) VALUES (?, ?, ?, ?, ?)""",
            (name, description, config_json, now, now),
        )
        self.conn.commit()
        return self.get_workspace(cur.lastrowid)

    def get_workspace(self, workspace_id: int) -> Optional[dict]:
        row = self.conn.execute(
            "SELECT * FROM workspaces WHERE id = ?", (workspace_id,)
        ).fetchone()
        if not row:
            return None
        d = self._row_to_dict(row)
        if d.get("config"):
            d["config"] = json.loads(d["config"])
        return d

    def list_workspaces(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM workspaces ORDER BY name"
        ).fetchall()
        result = self._rows_to_list(rows)
        for d in result:
            if d.get("config"):
                d["config"] = json.loads(d["config"])
        return result

    def update_workspace(self, workspace_id: int, **kwargs: Any) -> Optional[dict]:
        allowed = {"name", "description", "config"}
        fields = {k: v for k, v in kwargs.items() if k in allowed}
        if not fields:
            return self.get_workspace(workspace_id)
        if "config" in fields and isinstance(fields["config"], dict):
            fields["config"] = json.dumps(fields["config"])
        fields["updated_at"] = self._now()
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [workspace_id]
        self.conn.execute(
            f"UPDATE workspaces SET {set_clause} WHERE id = ?", values
        )
        self.conn.commit()
        return self.get_workspace(workspace_id)

    def delete_workspace(self, workspace_id: int) -> bool:
        cur = self.conn.execute(
            "DELETE FROM workspaces WHERE id = ?", (workspace_id,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    # -----------------------------------------------------------------------
    # Tags
    # -----------------------------------------------------------------------

    def create_tag(self, name: str) -> dict:
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO tags (name) VALUES (?)", (name,)
        )
        self.conn.commit()
        row = self.conn.execute(
            "SELECT * FROM tags WHERE name = ?", (name,)
        ).fetchone()
        return self._row_to_dict(row)

    def tag_brush(self, brush_id: int, tag_name: str) -> None:
        tag = self.create_tag(tag_name)
        self.conn.execute(
            "INSERT OR IGNORE INTO brush_tags (brush_id, tag_id) VALUES (?, ?)",
            (brush_id, tag["id"]),
        )
        self.conn.commit()

    def get_brush_tags(self, brush_id: int) -> list[str]:
        rows = self.conn.execute(
            """SELECT t.name FROM tags t
               JOIN brush_tags bt ON bt.tag_id = t.id
               WHERE bt.brush_id = ?
               ORDER BY t.name""",
            (brush_id,),
        ).fetchall()
        return [r["name"] for r in rows]

    def find_brushes_by_tag(self, tag_name: str) -> list[dict]:
        rows = self.conn.execute(
            """SELECT b.* FROM brushes b
               JOIN brush_tags bt ON bt.brush_id = b.id
               JOIN tags t ON t.id = bt.tag_id
               WHERE t.name = ?
               ORDER BY b.name""",
            (tag_name,),
        ).fetchall()
        result = self._rows_to_list(rows)
        for d in result:
            if d.get("settings"):
                d["settings"] = json.loads(d["settings"])
        return result


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Use an in-memory database for the demo
    db = KritaDB(":memory:")

    # Create a project
    project = db.create_project(
        "Fantasy Landscape", width=3840, height=2160, dpi=300
    )
    print(f"Project: {project['name']} ({project['width']}x{project['height']})")

    # Add layers
    bg = db.create_layer(project["id"], "Background", layer_type="paint", position=0)
    sky = db.create_layer(project["id"], "Sky", layer_type="paint", position=1)
    trees = db.create_layer(
        project["id"], "Trees", layer_type="paint", position=2, opacity=0.9
    )
    print(f"Layers: {[l['name'] for l in db.list_layers(project['id'])]}")

    # Create brushes
    soft = db.create_brush(
        "Soft Round", category="basic", size=50.0, opacity=0.8,
        settings={"hardness": 0.2, "spacing": 0.1},
    )
    ink = db.create_brush("Ink Pen", category="inking", size=5.0)
    texture = db.create_brush(
        "Texture Brush", category="texture", size=80.0,
        settings={"grain": "canvas", "depth": 0.6},
    )
    print(f"Brushes: {[b['name'] for b in db.list_brushes()]}")

    # Tag brushes
    db.tag_brush(soft["id"], "favorites")
    db.tag_brush(ink["id"], "favorites")
    db.tag_brush(texture["id"], "landscape")
    print(f"Favorite brushes: {[b['name'] for b in db.find_brushes_by_tag('favorites')]}")
    print(f"Ink Pen tags: {db.get_brush_tags(ink['id'])}")

    # Create a palette
    palette = db.create_palette("Sunset Palette", description="Warm sunset tones")
    db.add_palette_color(palette["id"], "#FF6B35", name="Burnt Orange", position=0)
    db.add_palette_color(palette["id"], "#F7C59F", name="Peach", position=1)
    db.add_palette_color(palette["id"], "#EFEFD0", name="Cream", position=2)
    db.add_palette_color(palette["id"], "#004E89", name="Deep Blue", position=3)
    db.add_palette_color(palette["id"], "#1A659E", name="Steel Blue", position=4)
    palette = db.get_palette(palette["id"])
    print(f"Palette '{palette['name']}': {[c['hex_color'] for c in palette['colors']]}")

    # Create a workspace
    ws = db.create_workspace(
        "Digital Painting",
        description="Optimised layout for digital painting",
        config={
            "panels": ["layers", "brushes", "colors", "overview"],
            "canvas_rotation": True,
            "mirror_view": True,
            "toolbar": ["brush", "eraser", "fill", "transform", "selection"],
        },
    )
    print(f"Workspace '{ws['name']}': panels={ws['config']['panels']}")

    # List everything
    print(f"\nAll projects: {len(db.list_projects())}")
    print(f"All brushes:  {len(db.list_brushes())}")
    print(f"All palettes: {len(db.list_palettes())}")
    print(f"All workspaces: {len(db.list_workspaces())}")

    db.close()
    print("\nDone — all operations completed successfully.")
