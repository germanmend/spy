from statemachine import StateMachine, State


class HitStatusMachine(StateMachine):
    active = State('active', initial=True)
    failed = State('failed')
    completed = State('completed')

    toFailed = active.to(failed)
    toCompleted = active.to(completed)
