import sys
import copy
from typing import Iterable, List, Callable
from dataclasses import dataclass


@dataclass
class Instruction:
    op_code: str
    argument: int
    has_run: bool = False


@dataclass
class Registers:
    acc1: int = 0


def parse_instructions(filename: str) -> Iterable[Instruction]:
    with open(filename) as f:
        for l in f:
            yield(Instruction(l[:3], int(l[4:])))


def acc_op(registers: Registers, instruction: Instruction) -> int:
    registers.acc1 += instruction.argument
    instruction.has_run = True
    return 1


def jmp_op(registers: Registers, instruction: Instruction) -> int:
    instruction.has_run = True
    return instruction.argument


def no_op(registers: Registers, instruction: Instruction) -> int:
    instruction.has_run = True
    return 1


def term_op(registers: Registers, instruction: Instruction) -> int:
    instruction.has_run = True
    return 0

# TODO: look into typing-extensions/Protocol/__call__ PEP 544 vs. Callable?


def run_until(instructions: List[Instruction], registers: Registers, condition: Callable[[Instruction], bool]) -> Instruction:
    i_ptr = 0
    while True:
        inst = instructions[i_ptr]
        if condition(inst):
            break
        i_ptr += op_code_handlers[inst.op_code](registers, inst)


op_code_handlers = {'nop': no_op,    'acc': acc_op,
                    'jmp': jmp_op, 'term': term_op}


def has_run_condition(instruction: Instruction) -> bool:
    return instruction.has_run


def part1(filename: str):
    instructions = list(parse_instructions(filename))
    registers = Registers()

    # Part 1
    run_until(instructions, registers, has_run_condition)
    assert registers.acc1 == 1723
    print(f'Registers: {registers}')


def part2(filename: str):
    instructions = list(parse_instructions(filename))
    # Part 2
    # brute force walk it from the begining each time.
    for i_ptr, instruction in enumerate(instructions):
        if instruction.op_code == 'nop' or instruction.op_code == 'jmp':
            registers = Registers()
            candidate_instructions = copy.deepcopy(instructions)
            term_instruction = Instruction('term', 0)  # sentinel at end
            candidate_instructions.append(term_instruction)

            if instruction.op_code == 'nop':
                candidate_instructions[i_ptr].op_code = 'jmp'
            else:
                candidate_instructions[i_ptr].op_code = 'nop'

            run_until(candidate_instructions,
                      registers, has_run_condition)
            if term_instruction.has_run:
                break
    print(
        f'done: altered op[{i_ptr}]: {candidate_instructions[i_ptr]}: registers: {registers}')
    assert registers.acc1 == 846
    assert i_ptr == 196


if __name__ == "__main__":
    part1(sys.argv[1])
    part2(sys.argv[1])
