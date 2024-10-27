from __future__ import annotations

import logging
import time
from datetime import timedelta

import pendulum
from airflow.decorators import task
from airflow.models.dag import dag
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule

logger = logging.getLogger(__name__)

DAG_ID = "hourly_gift_receiver"


@dag(
    dag_id=DAG_ID,
    default_args={"retries": 2},
    description="Receive match-masters gift every 3 hours",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["match-masters"],
)
def HourlyGiftReceiverDag():
    from match_masters.controller.mm_phone_controller import MMPhoneController
    phone_controller = MMPhoneController()

    @task
    def unlock_phone():
        phone_controller.unlock_phone()

    @task
    def run_match_masters():
        phone_controller.open_match_masters()

    @task(
        retries=5,
        retry_delay=timedelta(seconds=5),
    )
    def try_to_enter_shop():
        is_shop_available = phone_controller.try_to_enter_shop()
        if not is_shop_available:
            raise RuntimeError("Could not enter shop")

    @task(
        retries=5,
        retry_delay=timedelta(seconds=5),
    )
    def try_to_init_receive_gift():
        is_init_receive_gift_available = phone_controller.try_to_init_gift_receive()
        if not is_init_receive_gift_available:
            raise RuntimeError("Could not init receive gift")

    @task
    def receive_gift():
        phone_controller.tap_gift()
        time.sleep(4)
        phone_controller.tap_receive_gift()

    @task(
        trigger_rule=TriggerRule.ALL_DONE
    )
    def close_match_masters():
        phone_controller.close_match_masters()

    @task(
        trigger_rule=TriggerRule.ALL_DONE
    )
    def lock_phone():
        phone_controller.lock_phone()

    handle_failure = TriggerDagRunOperator(
        task_id="handle_failure",
        trigger_rule=TriggerRule.ONE_FAILED,
        trigger_dag_id=DAG_ID,
        logical_date=pendulum.now() + timedelta(minutes=1),
    )
    handle_success = TriggerDagRunOperator(
        task_id="handle_success",
        trigger_rule=TriggerRule.ALL_SUCCESS,
        trigger_dag_id=DAG_ID,
        logical_date=pendulum.now() + timedelta(hours=3, minutes=5),
    )


    try_to_enter_shop_task = try_to_enter_shop()
    try_to_init_receive_gift_task = try_to_init_receive_gift()
    receive_gift_task = receive_gift()

    # main flow
    (unlock_phone() >>
     run_match_masters() >>
     try_to_enter_shop_task >>
     try_to_init_receive_gift_task >>
     receive_gift_task >>
     close_match_masters() >>
     lock_phone())

    # handle failure
    try_to_init_receive_gift_task >> handle_failure
    receive_gift_task >> handle_success


HourlyGiftReceiverDag()
