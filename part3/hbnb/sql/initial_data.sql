INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'User',
    'admin@hbnb.io',
    '$2b$12$d0MY.xc2U2mQHBtX2XGVW.eqMee5TNf64sXI7Hck8p/OLCxiyUn3q',
    TRUE,
    DATETIME('now'),
    DATETIME('now')
);

INSERT INTO amenities (id, name, created_at, updated_at)
VALUES 
    ('de1ef314-01fb-48fb-9680-c7902795abfd', 'WiFi', DATETIME('now'), DATETIME('now')),
    ('d51b27ac-57f3-4377-a693-3cbe825dd3e1', 'Swimming Pool', DATETIME('now'), DATETIME('now')),
    ('d17e106d-3b50-46ff-adb7-fb28838f6e5d', 'Air Conditioning', DATETIME('now'), DATETIME('now'));

