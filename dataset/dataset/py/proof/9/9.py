# proof_authorization_delete.py

class Request:
    """
    Minimal imitation of requests.Request
    Only stores headers for this demonstration.
    """
    def __init__(self, headers=None):
        self.headers = headers or {}


class ResolveRedirect:
    """
    Simulates redirect logic inside requests.sessions
    """

    @staticmethod
    def unsafe_strip_auth(prepared_request):
        """Deletes Authorization WITHOUT checking."""
        print("Unsafe redirect handling...")
        headers = prepared_request.headers

        del headers["Authorization"]

        print("Authorization removed safely (but only if it existed).")

    @staticmethod
    def safe_strip_auth(prepared_request):
        """Deletes Authorization WITH safety check (like Requests)."""
        print("Safe redirect handling...")
        headers = prepared_request.headers

        try:
            del headers["Authorization"]
        except KeyError:
            print("Authorization header not present — handled safely.")

        print("Redirect handling continues normally.")


def run_demo():
    # Case 1: Authorization exists
    req_with_auth = Request({
        "User-Agent": "demo-client",
        "Authorization": "Bearer SECRET"
    })

    print("\n=== CASE 1: Authorization exists ===")
    ResolveRedirect.unsafe_strip_auth(req_with_auth)

    # Case 2: Authorization missing
    req_without_auth = Request({
        "User-Agent": "demo-client"
    })

    print("\n=== CASE 2: Authorization missing ===")

    # Show crash
    try:
        ResolveRedirect.unsafe_strip_auth(req_without_auth)
    except KeyError as e:
        print("CRASH OCCURRED:", e)

    # Show safe behavior
    ResolveRedirect.safe_strip_auth(req_without_auth)


if __name__ == "__main__":
    run_demo()