"""Эмулятор веб-сервиса каталога видеоигр: поиск по жанру и минимальным системным требованиям."""
from flask import Flask, jsonify, request

app = Flask(__name__)

# id, title, genre, min_ram_gb, min_cpu_ghz, min_gpu, min_disk_gb, gpu_tier (1..6)
_RAW = [
    (1, "The Witcher 3: Wild Hunt", "RPG", 6, 2.5, "GTX 660", 50, 3),
    (2, "Cyberpunk 2077", "RPG", 12, 3.0, "GTX 1060", 70, 4),
    (3, "Elden Ring", "RPG", 12, 3.0, "GTX 1060", 60, 4),
    (4, "Doom Eternal", "Shooter", 8, 3.0, "GTX 970", 80, 4),
    (5, "Counter-Strike 2", "Shooter", 8, 2.8, "GTX 1050", 30, 3),
    (6, "Half-Life 2", "Shooter", 1, 1.7, "Intel HD", 6, 1),
    (7, "Civilization VI", "Strategy", 4, 2.5, "GTX 650", 12, 2),
    (8, "Age of Empires II: DE", "Strategy", 8, 2.4, "GTX 650", 50, 2),
    (9, "Factorio", "Strategy", 4, 2.0, "Intel HD", 3, 1),
    (10, "Hollow Knight", "Platformer", 4, 2.0, "GeForce 9800", 9, 1),
    (11, "Stardew Valley", "Simulation", 2, 2.0, "Intel HD", 1, 1),
    (12, "Cities: Skylines", "Simulation", 4, 2.5, "GTX 260", 4, 2),
    (13, "Microsoft Flight Simulator", "Simulation", 8, 3.0, "GTX 770", 150, 5),
    (14, "Forza Horizon 5", "Racing", 8, 3.0, "GTX 970", 110, 4),
    (15, "Need for Speed: Heat", "Racing", 8, 3.0, "GTX 760", 50, 3),
    (16, "Celeste", "Platformer", 2, 2.0, "Intel HD", 2, 1),
    (17, "Minecraft", "Sandbox", 4, 2.0, "Intel HD 4000", 2, 1),
    (18, "Terraria", "Sandbox", 2, 2.0, "Intel HD", 1, 1),
    (19, "Hades", "Roguelike", 4, 2.0, "GTX 650", 15, 2),
    (20, "Dead Cells", "Roguelike", 4, 2.0, "Intel HD", 2, 1),
    (21, "Resident Evil 4 Remake", "Horror", 16, 3.2, "GTX 1070", 60, 5),
    (22, "Amnesia: The Dark Descent", "Horror", 2, 2.0, "GeForce 6", 5, 1),
    (23, "Red Dead Redemption 2", "Adventure", 8, 3.0, "GTX 770", 150, 4),
    (24, "Portal 2", "Puzzle", 2, 2.0, "Intel HD", 8, 1),
    (25, "Baldur's Gate 3", "RPG", 8, 3.0, "GTX 970", 150, 4),
]
GAMES = [
    {"id": i, "title": t, "genre": g, "min_ram_gb": r, "min_cpu_ghz": c,
     "min_gpu": gpu, "min_disk_gb": d, "gpu_tier": tier}
    for i, t, g, r, c, gpu, d, tier in _RAW
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/genres")
def genres():
    return jsonify(sorted({g["genre"] for g in GAMES}))


@app.get("/games")
def games():
    """Фильтры: genre, ram (ГБ ОЗУ у пользователя), cpu (ГГц), disk (ГБ), gpu_tier (1..6), q (подстрока названия)."""
    genre = request.args.get("genre")
    q = (request.args.get("q") or "").lower()
    ram = request.args.get("ram", type=float)
    cpu = request.args.get("cpu", type=float)
    disk = request.args.get("disk", type=float)
    tier = request.args.get("gpu_tier", type=int)

    result = []
    for g in GAMES:
        if genre and g["genre"].lower() != genre.lower():
            continue
        if q and q not in g["title"].lower():
            continue
        if ram is not None and g["min_ram_gb"] > ram:
            continue
        if cpu is not None and g["min_cpu_ghz"] > cpu:
            continue
        if disk is not None and g["min_disk_gb"] > disk:
            continue
        if tier is not None and g["gpu_tier"] > tier:
            continue
        result.append(g)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
