from airflow.providers.oracle.hooks.oracle import OracleHook
import logging

def debug_connection():
    try:
        hook = OracleHook(oracle_conn_id="oracle_kpc")
        conn = hook.get_connection("oracle_kpc")
        print(f"--- Connection Details ---")
        print(f"Host: {conn.host}")
        print(f"Port: {conn.port}")
        print(f"Schema (Username): {conn.schema}")
        print(f"Login: {conn.login}")
        # Check extras for service_name or sid
        print(f"Extra: {conn.extra}")
        
        # Test DSN construction logic
        dsn = hook.get_dsn(conn)
        print(f"Constructed DSN: {dsn}")
        
    except Exception as e:
        print(f"Error inspecting connection: {e}")

if __name__ == "__main__":
    debug_connection()
