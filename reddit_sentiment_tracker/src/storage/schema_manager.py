# Table definitions - 2 needed (top posts, rising posts)
# 2. TABLE DEFINITIONS (SCHEMA)
rising_posts = Table(
    'passwords', metadata,
    Column('id', Integer, primary_key=True),
    Column('service', String(100), nullable=False),
    Column('username', String(100)),
    Column('encrypted_password', String(256), nullable=False),
    Column('url', String(255)),
    Column('notes', String(500)),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('last_updated', DateTime, onupdate=datetime.utcnow),
    Column('is_active', Boolean, default=True)
)

top_posts = Table(
    'passwords', metadata,
    Column('id', Integer, primary_key=True),
    Column('service', String(100), nullable=False),
    Column('username', String(100)),
    Column('encrypted_password', String(256), nullable=False),
    Column('url', String(255)),
    Column('notes', String(500)),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('last_updated', DateTime, onupdate=datetime.utcnow),
    Column('is_active', Boolean, default=True)
)


