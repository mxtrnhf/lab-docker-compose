CREATE TABLE IF NOT EXISTS library (
    id          SERIAL PRIMARY KEY,
    game_id     INTEGER NOT NULL UNIQUE,
    title       TEXT NOT NULL,
    genre       TEXT NOT NULL,
    min_ram_gb  INTEGER NOT NULL,
    min_cpu_ghz NUMERIC(3,1) NOT NULL,
    min_gpu     TEXT NOT NULL,
    min_disk_gb INTEGER NOT NULL,
    status      TEXT NOT NULL DEFAULT 'planned',
    added_at    TIMESTAMP NOT NULL DEFAULT now()
);

INSERT INTO library (game_id, title, genre, min_ram_gb, min_cpu_ghz, min_gpu, min_disk_gb, status) VALUES
 (1,  'The Witcher 3: Wild Hunt', 'RPG',      6, 2.5, 'GTX 660',   50, 'completed'),
 (11, 'Stardew Valley',           'Simulation', 2, 2.0, 'Intel HD',  1, 'playing')
ON CONFLICT DO NOTHING;
