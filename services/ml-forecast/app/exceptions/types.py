class AppException(Exception):

    status_code = 400
    error_code = "app_error"

    def __init__(self, message: str, *, status_code: int | None = None, error_code: str | None = None):
        super().__init__(message)
        if status_code:
            self.status_code = status_code
        if error_code:
            self.error_code = error_code
        self.message = message


class KafkaConnectionError(AppException):
    status_code = 500
    error_code = "kafka_connection_error"


class DatabaseError(AppException):
    status_code = 500
    error_code = "database_error"


class AvroDecodeError(AppException):
    status_code = 500
    error_code = "avro_decode_error"
