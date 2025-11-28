import os
from datetime import datetime
from flask import Flask, request, jsonify
from s3_utils import head_metadata, update_metadata
from ses_utils import send_note_email

app = Flask(__name__)
SALES_NOTES_PUBLIC_URL = os.getenv("SALES_NOTES_PUBLIC_URL")

@app.get("/health")
def health():
    return "ok", 200

@app.post("/notify")
def notify():
    data = request.get_json() or {}
    required = ["email", "folio", "rfc", "s3_key"]
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos"}), 400

    email = data["email"]
    folio = data["folio"]
    s3_key = data["s3_key"]

    metadata = head_metadata(s3_key)
    veces = int(metadata.get("veces-enviado", "0"))
    metadata["veces-enviado"] = str(veces + 1)
    metadata["hora-envio"] = datetime.utcnow().isoformat()
    update_metadata(s3_key, metadata)

    if not SALES_NOTES_PUBLIC_URL:
        return jsonify({"error": "SALES_NOTES_PUBLIC_URL no configurado"}), 500

    download_url = "%s/%s/download" % (SALES_NOTES_PUBLIC_URL.rstrip("/"), folio)

    subject = "Nueva nota de venta %s" % folio
    html = """
    <p>Estimado cliente,</p>
    <p>Se ha generado una nueva nota de venta con folio <strong>%s</strong>.</p>
    <p>Puede descargarla aquí: <a href="%s">%s</a></p>
    """ % (folio, download_url, download_url)

    send_note_email(email, subject, html)
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3003"))
    app.run(host="0.0.0.0", port=port)
