from statemachine import StateMachine, State


class HitmanIsActiveMachine(StateMachine):
    true = State('true', initial=True)
    false = State('false')

    deactivate = true.to(false)
