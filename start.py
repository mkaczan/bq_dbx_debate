"""Runner script to launch the BQ vs Databricks Debate Arena web server."""
import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print(f"==================================================================")
    print(f"🚀⚡🏛️ BigQuery vs Databricks Strategic Debate Arena & Arbiter")
    print(f"🌐 Server starting at http://{HOST}:{PORT}")
    print(f"==================================================================")
    uvicorn.run("app.server.api:app", host=HOST, port=PORT, reload=False)
