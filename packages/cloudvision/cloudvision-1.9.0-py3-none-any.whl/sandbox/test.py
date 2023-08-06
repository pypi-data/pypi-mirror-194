from cloudvision.cvlib import (
    Action,
    ActionContext,
    Context,
    Device,
    Execution,
    User,
    Logger,
    LoggingLevel
)

user = User("test_user", "123")

device = Device(ip="123.456.789", deviceId="JP123456",
                deviceMac="00-B0-D0-63-C2-26")

action = Action(
    name="test_action",
    context=ActionContext.ChangeControl,
    actionId="1234"
)

execution = Execution(executionId="2")

ctx_high_logging = Context(
    user=user,
    device=device,
    action=action,
    execution=execution
)


def alog(a, b, c, d):
    pass


def log_high(a, b):
    print(b)


logger_high = Logger(
    alog=alog,
    trace=log_high,
    debug=log_high,
    info=log_high,
    warning=log_high,
    error=log_high,
    critical=log_high
)
ctx_high_logging.logger = logger_high

ctx_high_logging.debug("Test 1")
ctx_high_logging.activateDebugMode()
ctx_high_logging.debug("Test 2")
ctx_high_logging.deactivateDebugMode()
ctx_high_logging.debug("Test 3")
