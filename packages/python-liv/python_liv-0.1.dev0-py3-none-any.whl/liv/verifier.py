from contextlib import redirect_stdout
from typing import Dict

from coveriteam.actors.analyzers import ProgramVerifier
from coveriteam.language.actor import Actor
from coveriteam.language.artifact import BehaviorSpecification, CProgram
from coveriteam.util import set_cache_directories, set_cache_update

from liv.util import capture_stdout

Actor.trust_tool_info = True  # type: ignore
# Actor.allow_cgroup_access = False


class Verifier:
    def verify(self, program, data_model, specification) -> Dict[str, str]:
        return {"verdict": "unknown"}


def get_verifier(args):
    return CVTVerifier(args.verifier, version=args.verifierversion or None)


class CVTVerifier(Verifier):
    def __init__(self, actordef, version=None):
        # coveriteam writes information about actor downloads to stdout, ignore that:
        self.verifier, _ = capture_stdout(lambda: ProgramVerifier(actordef, version))

    def verify(self, program, data_model, specification) -> Dict[str, str]:
        prog = CProgram(program, data_model)
        spec = BehaviorSpecification(specification)
        inputs = {
            "program": prog,
            "spec": spec,
        }
        res = self.verifier.act_and_save_xml(**inputs)
        return res
