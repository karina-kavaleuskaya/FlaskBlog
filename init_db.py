import psycopg2

def get_connection(db_name):
    conection = psycopg2.connect(
        dbname=db_name,
        host='****',
        port='***',
        user='***',
        password='****'
    )
    return conection


def main():
    with get_connection('flaskdb') as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS posts(
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                auther VARCHAR(100) 
                )
                """
            )
            conn.commit()

            cursor.execute("""
            INSERT INTO posts(title, content, auther)
            VALUES ('Post 1', 'some content 1', 'auther 1'),
            ('Post 1', 'some content 1', 'auther 1')"""

            )

            conn.commit()


if __name__ == '__main__':
    main()