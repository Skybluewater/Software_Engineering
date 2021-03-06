import random
from copy import deepcopy
from solve import Solvable
from decimal import Decimal


class BiTree:
    def getoperorder(self, ch):
        if ch in ['+', '-']:
            return 0
        elif ch in ['*']:
            return 2
        elif ch in ['/']:
            return 3
        elif ch == '^':
            return 4

    def __init__(self, node_type=0, val=0):
        self.node_type = node_type
        self.val = val
        self.lchild = None
        self.rchild = None
        if self.node_type == 1:
            self.val = chr(self.val)
            self.this_level = self.getoperorder(self.val)

    def set_lchild(self, lchild):
        self.lchild = lchild

    def set_rchild(self, rchild):
        self.rchild = rchild

    def to_string(self, upper_level=0):
        if self.node_type == 1:
            if upper_level > self.this_level or upper_level == self.this_level == 3 or upper_level == self.this_level \
                    == 4:
                return '(' + self.lchild.to_string(self.this_level) + self.val + self.rchild.to_string(
                    self.this_level + 1) + ')'
            else:
                return self.lchild.to_string(self.this_level) + self.val + self.rchild.to_string(self.this_level + 1)
        if int(self.val) < 0:
            return '(' + str(self.val) + ')'
        return str(self.val)


class QuestGenerator:
    def __init__(self):
        self.output_list = []
        self.deduplicate_set = set()

    def generate(self, quantity=1, operators=7, if_false=False, if_pow=False, if_fraction=False, pow_operator=False,
                 max=9):
        sum = 0
        while sum < quantity:
            filled_ops, unfilled_ops = self.randinit(operators=operators, if_false=if_false, if_pow=if_pow, max=max)
            while len(unfilled_ops):
                i = random.randint(0, len(filled_ops) - 1)
                unfilled_ops[0].set_lchild(filled_ops[i])
                filled_ops.pop(i)
                i = random.randint(0, len(filled_ops) - 1)
                unfilled_ops[0].set_rchild(filled_ops[i])
                filled_ops.pop(i)
                filled_ops.append(unfilled_ops[0])
                unfilled_ops.pop(0)
            if self.deduplicate(filled_ops[-1]):
                print('Duplicated!')
                continue
            string = filled_ops[-1].to_string()
            solve = Solvable()
            k = solve.calculator(string)
            if k == 'not solvable':
                continue
            if not if_fraction:
                k = self.round_up(round(float(k.numerator / k.denominator), 3))
            sum = sum + 1
            string = self.changepowop(string, pow_operator)
            self.output_list.append(string)
            self.output_list.append(str(k))

    def deduplicate(self, root: BiTree):
        inspect = deepcopy(root)
        self.format_expression(inspect)
        if inspect.to_string() in self.deduplicate_set:
            return True
        else:
            self.deduplicate_set.add(inspect.to_string())
            return False

    def randinit(self, operators, if_false, if_pow, max):
        operands = ['+', '-', '*', '/', '^']
        if if_false:
            nums = [BiTree(0, random.randint(-max, max)) for _ in range(operators + 1)]
        else:
            nums = [BiTree(0, random.randint(0, max)) for _ in range(operators + 1)]
        if if_pow:
            ops = [BiTree(1, ord(operands[random.randint(0, 4)])) for _ in range(operators)]
        else:
            ops = [BiTree(1, ord(operands[random.randint(0, 3)])) for _ in range(operators)]
        return nums, ops

    def format_expression(self, node: BiTree):
        if not node.lchild:
            return
        self.format_expression(node.lchild)
        self.format_expression(node.rchild)
        if node.this_level in (0, 2) and node.lchild.to_string() > node.rchild.to_string():
            tmp = node.lchild
            node.lchild = node.rchild
            node.rchild = tmp

    def round_up(self, value):
        return Decimal(value).quantize(Decimal('0.00'), rounding='ROUND_HALF_UP')

    def changepowop(self, string: str, pow_operator):
        if pow_operator:
            return string.replace('^', '**')
        return string
