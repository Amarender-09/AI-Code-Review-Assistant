import hashlib
import hmac


def verify_signature(
    payload_body: bytes,
    secret: str,
    signature_header: str | None,
) -> bool:
    if not signature_header:
        return False

    expected_signature = (
        "sha256="
        + hmac.new(
            secret.encode("utf-8"),
            payload_body,
            hashlib.sha256,
        ).hexdigest()
    )

    return hmac.compare_digest(
        expected_signature,
        signature_header,
    )