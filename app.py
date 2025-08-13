from flask import Flask
import psycopg2.pool
import os
import traceback

app = Flask(__name__)
try:
  pg_pool = psycopg2.pool.SimpleConnectionPool(
    minconn = 1,
    maxconn = 5,
    user = os.getenv('POSTGRES_USERNAME', ''),
    password = os.getenv('POSTGRES_PASSWORD', ''),
    host = os.getenv('POSTGRES_HOST', ''),
    database = os.getenv('POSTGRES_DATABASE', f'chatwoot_{os.getenv("RAILS_ENV", "production")}'),
  )
except:
  traceback.print_exc()
  pg_pool = None

@app.route('/', methods=['GET'])
def index():
  if not pg_pool:
    return 'Database connection not available.', 503

  conn = None
  domains = []

  try:
    conn = pg_pool.getconn()
    with conn.cursor() as cur:
      cur.execute('SELECT custom_domain FROM portals;')
      rows = cur.fetchall()
      domains = [row[0] for row in rows if row[0]]
  except Exception as e:
    return f'Error fetching domains: {str(e)}', 500
  finally:
    if conn:
      pg_pool.putconn(conn)

  return {
    'http': {
      'routers': {
        'chatwoot_rails': {
          'rule': ' || '.join(f'Host(`{domain}`)' for domain in domains),
          'service': 'chatwoot_rails',
          'entryPoints': ['websecure'],
          'tls': {
            'certResolver': 'letsencrypt',
          },
        },
      },
      'services': {
        'chatwoot_rails': {
          'loadBalancer': {
            'servers': [{
              'url': f'http://rails:3000',
            }],
          },
        },
      },
    },
  }
  
"""
Simple health endpoint for Docker.
In case the database connection pool is not initialized, it returns a 503 status code.
"""
@app.route('/health', methods=['GET'])
def health():
  if not pg_pool:
    return '', 503
  return ''