CREATE TABLE IF NOT EXISTS news (
                                title text,
                                link text UNIQUE,
                                full_date text,
                                date text,
                                source text,
                                description text,
                                image text, url text);