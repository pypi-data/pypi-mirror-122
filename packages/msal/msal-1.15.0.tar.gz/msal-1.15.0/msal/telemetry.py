import uuid
import logging


logger = logging.getLogger(__name__)

CLIENT_REQUEST_ID = 'client-request-id'
CLIENT_CURRENT_TELEMETRY = "x-client-current-telemetry"
CLIENT_LAST_TELEMETRY = "x-client-last-telemetry"
NON_SILENT_CALL = 0
FORCE_REFRESH = 1
AT_ABSENT = 2
AT_EXPIRED = 3
AT_AGING = 4
RESERVED = 5


def _get_new_correlation_id():
    return str(uuid.uuid4())


class _TelemetryContext(object):
    """It is used for handling the telemetry context for current OAuth2 "exchange"."""
    # https://identitydivision.visualstudio.com/DevEx/_git/AuthLibrariesApiReview?path=%2FTelemetry%2FMSALServerSideTelemetry.md&_a=preview
    _SUCCEEDED = "succeeded"
    _FAILED = "failed"
    _FAILURE_SIZE = "failure_size"
    _CURRENT_HEADER_SIZE_LIMIT = 100
    _LAST_HEADER_SIZE_LIMIT = 350

    def __init__(self, buffer, lock, api_id, correlation_id=None, refresh_reason=None):
        self._buffer = buffer
        self._lock = lock
        self._api_id = api_id
        self._correlation_id = correlation_id or _get_new_correlation_id()
        self._refresh_reason = refresh_reason or NON_SILENT_CALL
        logger.debug("Generate or reuse correlation_id: %s", self._correlation_id)

    def generate_headers(self):
        with self._lock:
            current = "4|{api_id},{cache_refresh}|".format(
                api_id=self._api_id, cache_refresh=self._refresh_reason)
            if len(current) > self._CURRENT_HEADER_SIZE_LIMIT:
                logger.warning(
                    "Telemetry header greater than {} will be truncated by AAD".format(
                    self._CURRENT_HEADER_SIZE_LIMIT))
            failures = self._buffer.get(self._FAILED, [])
            return {
                CLIENT_REQUEST_ID: self._correlation_id,
                CLIENT_CURRENT_TELEMETRY: current,
                CLIENT_LAST_TELEMETRY: "4|{succeeded}|{failed_requests}|{errors}|".format(
                    succeeded=self._buffer.get(self._SUCCEEDED, 0),
                    failed_requests=",".join("{a},{c}".format(**f) for f in failures),
                    errors=",".join(f["e"] for f in failures),
                    )
                }

    def hit_an_access_token(self):
        with self._lock:
            self._buffer[self._SUCCEEDED] = self._buffer.get(self._SUCCEEDED, 0) + 1

    def update_telemetry(self, auth_result):
        if auth_result:
            with self._lock:
                if "error" in auth_result:
                    self._record_failure(auth_result["error"])
                else:  # Telemetry sent successfully. Reset buffer
                    self._buffer.clear()  # This won't work: self._buffer = {}

    def _record_failure(self, error):
        simulation = len(",{api_id},{correlation_id},{error}".format(
            api_id=self._api_id, correlation_id=self._correlation_id, error=error))
        if self._buffer.get(self._FAILURE_SIZE, 0) + simulation < self._LAST_HEADER_SIZE_LIMIT:
            self._buffer[self._FAILURE_SIZE] = self._buffer.get(
                self._FAILURE_SIZE, 0) + simulation
            self._buffer.setdefault(self._FAILED, []).append({
                "a": self._api_id, "c": self._correlation_id, "e": error})

