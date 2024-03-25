from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from enum import StrEnum

from statemachine import StateMachine
from statemachine import State
from statemachine.states import States


class Boundary(StrEnum):
    WAIT_FOR_PAYMENT = "wait_for_payment"
    PAYMENTS_ENOUGH = "payments_enough"
    PAYMENT_RECEIVED = "payment_received"

class Action(StrEnum):
    ADD_TO_ORDER = "add_to_order"
    RECEIVE_PAYMENT = "receive_payment"
    PROCESS_ORDER = "process_order"
    SHIP_ORDER = "ship_order"


class Order:

    def __init__(self) -> None:
        self.order_total = 0
        self.payments = []
        self.payment_received = False

    def payments_enough(self, amount: float) -> bool:
        return sum(self.payments) + amount >= self.order_total

    def before_add_to_order(self, amount: float) -> float:
        self.order_total += amount
        return self.order_total

    def on_receive_payment(self, amount: float) -> list[float]:
        self.payments.append(amount)
        return self.payments

    def after_receive_payment(self) -> None:
        self.payment_received = True

    def wait_for_payment(self) -> None:
        self.payment_received = False


class OrderControl(StateMachine):
    # States
    waiting_for_payment = State(initial=True, enter=Boundary.WAIT_FOR_PAYMENT)
    processing = State()
    shipping = State()
    completed = State(final=True)

    # Actions
    add_to_order = waiting_for_payment.to(waiting_for_payment)
    receive_payment = (
        waiting_for_payment.to(processing, cond=Boundary.PAYMENTS_ENOUGH) |
        waiting_for_payment.to(waiting_for_payment, unless=Boundary.PAYMENTS_ENOUGH)
    )
    process_order = processing.to(shipping, cond=Boundary.PAYMENT_RECEIVED)
    ship_order = shipping.to(completed)


if __name__ == '__main__':
    from devtools import debug

    order = Order()
    control = OrderControl(order)

    control.send(Action.ADD_TO_ORDER, 6.0)
    control.send(Action.ADD_TO_ORDER, 10.0)

    control.send(Action.RECEIVE_PAYMENT, 12.0)
    debug(control)
    control.send(Action.RECEIVE_PAYMENT, 4.0)
    debug(control)

    control.send(Action.PROCESS_ORDER)
    debug(control)

    control.send(Action.SHIP_ORDER)
    debug(control)
