import unittest

import fireworks as fw


class TestWorkflowState(unittest.TestCase):
    def test_completed(self) -> None:
        # all leaves complete
        one = fw.Firework([], state="COMPLETED", fw_id=1)
        two = fw.Firework([], state="COMPLETED", fw_id=2)

        assert fw.Workflow([one, two]).state == "COMPLETED"

    def test_archived(self) -> None:
        one = fw.Firework([], state="ARCHIVED", fw_id=1)
        two = fw.Firework([], state="ARCHIVED", fw_id=2)

        assert fw.Workflow([one, two]).state == "ARCHIVED"

    def test_defused(self) -> None:
        # any defused == defused
        one = fw.Firework([], state="COMPLETED", fw_id=1)
        two = fw.Firework([], state="DEFUSED", fw_id=2)

        assert fw.Workflow([one, two]).state == "DEFUSED"

    def test_paused(self) -> None:
        # any paused == paused
        one = fw.Firework([], state="COMPLETED", fw_id=1)
        two = fw.Firework([], state="PAUSED", fw_id=2)

        assert fw.Workflow([one, two]).state == "PAUSED"

    def test_fizzled_1(self) -> None:
        # WF(Fizzled -> Waiting(no fizz parents)) == FIZZLED
        one = fw.Firework([], state="FIZZLED", fw_id=1)
        two = fw.Firework([], state="WAITING", fw_id=2, parents=one)

        assert fw.Workflow([one, two]).state == "FIZZLED"

    def test_fizzled_2(self) -> None:
        # WF(Fizzled -> Ready(allow fizz parents)) == RUNNING
        one = fw.Firework([], state="FIZZLED", fw_id=1)
        two = fw.Firework([], state="READY", fw_id=2, spec={"_allow_fizzled_parents": True}, parents=one)

        assert fw.Workflow([one, two]).state == "RUNNING"

    def test_fizzled_3(self) -> None:
        # WF(Fizzled -> Completed(allow fizz parents)) == COMPLETED
        one = fw.Firework([], state="FIZZLED", fw_id=1)
        two = fw.Firework([], state="COMPLETED", fw_id=2, spec={"_allow_fizzled_parents": True}, parents=one)

        assert fw.Workflow([one, two]).state == "COMPLETED"

    def test_fizzled_4(self) -> None:
        # one child doesn't allow fizzled parents
        one = fw.Firework([], state="FIZZLED", fw_id=1)
        two = fw.Firework([], state="READY", fw_id=2, spec={"_allow_fizzled_parents": True}, parents=one)
        three = fw.Firework([], state="WAITING", fw_id=3, parents=one)

        assert fw.Workflow([one, two, three]).state == "FIZZLED"

    def test_fizzled_5(self) -> None:
        # leaf is fizzled, wf is fizzled
        one = fw.Firework([], state="COMPLETED", fw_id=1)
        two = fw.Firework([], state="FIZZLED", fw_id=2, parents=one)

        assert fw.Workflow([one, two]).state == "FIZZLED"

    def test_fizzled_6(self) -> None:
        # deep fizzled fireworks, but still RUNNING
        one = fw.Firework([], state="FIZZLED", fw_id=1)
        two = fw.Firework([], state="FIZZLED", fw_id=2, spec={"_allow_fizzled_parents": True}, parents=one)
        three = fw.Firework([], state="READY", fw_id=3, spec={"_allow_fizzled_parents": True}, parents=two)
        assert fw.Workflow([one, two, three]).state == "RUNNING"

    def test_running_1(self) -> None:
        one = fw.Firework([], state="COMPLETED", fw_id=1)
        two = fw.Firework([], state="READY", fw_id=2, parents=one)

        assert fw.Workflow([one, two]).state == "RUNNING"

    def test_running_2(self) -> None:
        one = fw.Firework([], state="RUNNING", fw_id=1)
        two = fw.Firework([], state="WAITING", fw_id=2, parents=one)

        assert fw.Workflow([one, two]).state == "RUNNING"

    def test_reserved(self) -> None:
        one = fw.Firework([], state="RESERVED", fw_id=1)
        two = fw.Firework([], state="READY", fw_id=2, parents=one)

        assert fw.Workflow([one, two]).state == "RESERVED"

    def test_ready(self) -> None:
        one = fw.Firework([], state="READY", fw_id=1)
        two = fw.Firework([], state="READY", fw_id=2, parents=one)

        assert fw.Workflow([one, two]).state == "READY"
