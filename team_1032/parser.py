from typing import List, Tuple, Union
from collections import defaultdict
import re

class ParseTree:
    def __init__(self, symbol, children=None, value=None):
        self.symbol = symbol 
        self.children = children if children is not None else []  
        self.value = value
    
    def __str__(self):
        return self._to_string()
    
    def _to_string(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.symbol}"
        if self.value is not None and self.value != self.symbol:
            result += f": {self.value}"
        result += "\n"
        for child in self.children:
            result += child._to_string(level + 1)
        return result

class ErrorReport:
    def __init__(self, position: int, message: str):
        self.position = position
        self.message = message

def parser(tokens: List[str]) -> Tuple[bool, Union[ParseTree, ErrorReport]]:
    """
    Returns (True, parse_tree) on success or (False, ErrorReport) on failure.
    Example:
        return True, ParseTree(...)
        return False, ErrorReport(3, "unexpected token 'else'")
    """

    SLR_TABLE = make_table(given_grammar)
    tokens = preprocess_read_tokens(tokens)

    # 초기상태와 EOF 붙이기
    stack = [0]
    tokens += ["$"]
    index = 0

    while True:
        
        if len(stack) == 0:
            return False, ErrorReport(index, "스택이 비어있습니다")
        else:
            current_state = stack[-1]

            action = SLR_TABLE.get(stack[-1], {}).get(tokens[index])

            if action == "acc":  # accept 경우
                return True, stack[1]
            
            elif action is None:  # 테이블 결과가 없는 경우
                expected = list(SLR_TABLE.get(stack[-1], {}).keys())
                return False, ErrorReport(
                    index, 
                    f"unexpected token '{tokens[index]}', expected one of {expected}"
                )

            elif isinstance(action, str):
                if action[0] == "s":  # shift 경우
                    terminal = ParseTree(tokens[index])
                    stack.append(terminal)
                    stack.append(int(action[1:]))
                    index += 1

                elif action[0] == "r":  # reduce 경우
                    rule_index = int(action[1:])
                    lhs, rhs = given_grammar[rule_index]

                    children = []
                    if rhs == ["epsilon"]:
                        pass
                    else:
                        for _ in range(len(rhs)):
                            if len(stack) < 1:  # 상태 pop
                                return False, ErrorReport(
                                    index,
                                    f"reduce 위한 상태 pop 이전에 스택 언더플로우 발생. Rule: {lhs} -> {' '.join(rhs)}",
                                )
                            stack.pop()

                            if len(stack) < 1:  # 노드 pop 
                                return False, ErrorReport(
                                    index,
                                    f"reduce 위한 노드 pop 이전에 스택 언더플로우 발생. Rule: {lhs} -> {' '.join(rhs)}",
                                )
                            node_to_add = stack.pop()  # ParseTree 노드 pop

                            if not isinstance(node_to_add, ParseTree): 
                                return False, ErrorReport(
                                    index,
                                    f"스택의 parseTree위치에 Type이 존재함, got {type(node_to_add)}. Rule: {lhs} -> {' '.join(rhs)}",
                                )
                            children.insert(0, node_to_add)

                    parent_node = ParseTree(lhs, children)

                    # goto
                    prev_state = stack[-1]
                    if not isinstance(prev_state, int):
                        return False, ErrorReport(
                            index,
                            f"Invalid state {prev_state}, 축소후 스택 top에 int가 아닌 값이 있음",
                        )

                    goto = SLR_TABLE.get(prev_state, {}).get(lhs)
                    if goto is None:
                        return False, ErrorReport(
                            index, f"상태 {prev_state} 에서 심볼 {lhs}에 대한 goto가 정의되어 있지 않습니다."
                        )
                    
                    if not isinstance(goto, int):
                        return False, ErrorReport(
                            index, f"현재 goto값 {goto}는 정수가 아님."
                        )

                    stack.append(parent_node)
                    stack.append(goto)

    return False, ErrorReport(index, "SLR parser loop 비정상 종료")


def make_table(raw_grammar):
    # ε 처리 & 인덱스 매핑
    grammar = []
    for lhs, rhs in raw_grammar:
        grammar.append((lhs, [] if rhs == ["epsilon"] else rhs))

    nonterminals = {lhs for lhs, _ in grammar}
    terminals = set(
        sym for _, rhs in grammar for sym in rhs
        if sym not in nonterminals
    ) | {"$"}

    # FIRST
    FIRST = {X: set() for X in nonterminals}
    for t in terminals:
        FIRST[t] = {t}
    FIRST["epsilon"] = {"epsilon"}

    changed = True
    while changed:
        changed = False
        for A, alpha in grammar:
            if not alpha:
                if "epsilon" not in FIRST[A]:
                    FIRST[A].add("epsilon"); changed = True
            else:
                for X in alpha:
                    before = len(FIRST[A])
                    FIRST[A] |= (FIRST[X] - {"epsilon"})
                    if "epsilon" in FIRST[X]:
                        continue
                    break
                else:
                    if "epsilon" not in FIRST[A]:
                        FIRST[A].add("epsilon"); changed = True

    # FOLLOW
    FOLLOW = {A: set() for A in nonterminals}
    FOLLOW["Program'"].add("$")
    changed = True
    while changed:
        changed = False
        for A, alpha in grammar:
            trailer = FOLLOW[A].copy()
            for X in reversed(alpha):
                if X in nonterminals:
                    before = len(FOLLOW[X])
                    FOLLOW[X] |= trailer
                    if len(FOLLOW[X]) != before:
                        changed = True
                    if "epsilon" in FIRST[X]:
                        trailer |= (FIRST[X] - {"epsilon"})
                    else:
                        trailer = FIRST[X] - {"epsilon"}
                else:
                    trailer = {X}

    # LR(0) 아이템·closure·goto 정의
    def closure(items):
        C = set(items)
        while True:
            new = set()
            for A, alpha, dot in C:
                if dot < len(alpha):
                    B = alpha[dot]
                    if B in nonterminals:
                        for lhs, rhs in grammar:
                            if lhs == B:
                                new.add((B, tuple(rhs), 0))
            if new <= C:
                break
            C |= new
        return C

    def goto(I, X):
        moved = {(A, alpha, dot+1) for A, alpha, dot in I if dot < len(alpha) and alpha[dot] == X}
        return closure(moved)

    # 상태 생성
    states = []
    init = closure({("Program'", tuple(grammar[0][1]), 0)})
    states.append(init)
    changed = True
    while changed:
        changed = False
        for I in states:
            for X in nonterminals | terminals:
                J = goto(I, X)
                if J and J not in states:
                    states.append(J)
                    changed = True

    # 상태별 인덱스
    state_ids = {frozenset(s): i for i, s in enumerate(states)}

    # ACTION / GOTO 테이블 생성
    action_table = {}
    goto_table   = {}

    prod_index = { (lhs, tuple(rhs)): i for i, (lhs, rhs) in enumerate(grammar) }

    for I in states:
        i = state_ids[frozenset(I)]
        for A, alpha, dot in I:
            # shift
            if dot < len(alpha):
                a = alpha[dot]
                if a in terminals:
                    j = state_ids[frozenset(goto(I, a))]
                    action_table[(i, a)] = ('shift', j)
            else:
                # accept
                if A == "Program'":
                    action_table[(i, '$')] = ('accept', None)
                else:
                    # reduce
                    idx = prod_index[(A, alpha)]
                    for a in FOLLOW[A]:
                        action_table[(i, a)] = ('reduce', idx)
        # GOTO 채우기
        for A in nonterminals:
            J = goto(I, A)
            if J:
                j = state_ids[frozenset(J)]
                goto_table[(i, A)] = j

    SLR_TABLE = {} # Dict[int, Dict[str, Union[str,int]]]

    # 1) ACTION 항목: shift/reduce/accept
    for (state, term), (kind, val) in action_table.items():
        entry = None
        if kind == 'shift':
            entry = f"s{val}"
        elif kind == 'reduce':
            entry = f"r{val}"
        elif kind == 'accept':
            entry = "acc"
        SLR_TABLE.setdefault(state, {})[term] = entry

    # 2) GOTO 항목: next state 번호 (int)
    for (state, nonterm), dest in goto_table.items():
        SLR_TABLE.setdefault(state, {})[nonterm] = dest

    return SLR_TABLE

given_grammar = [
    ("Program'", ["Program"]),
    ("Program", ["DeclList"]),
    ("DeclList", ["Decl", "DeclList"]),
    ("DeclList", ["epsilon"]),
    ("Decl", ["VarDecl"]),
    ("Decl", ["FuncDecl"]),
    ("VarDecl", ["type", "id", ";"]),
    ("VarDecl", ["type", "id", "=", "Expr", ";"]),
    ("FuncDecl", ["type", "id", "(", "ParamList", ")", "Block"]),
    ("ParamList", ["Param", ",", "ParamList"]),
    ("ParamList", ["Param"]),
    ("ParamList", ["epsilon"]),
    ("Param", ["type", "id"]),
    ("Block", ["{", "StmtList", "}"]),
    ("StmtList", ["Stmt", "StmtList"]),
    ("StmtList", ["epsilon"]),
    ("Stmt", ["IfStmt"]),
    ("Stmt", ["OtherStmt"]),
    ("IfStmt", ["if", "(", "Expr", ")", "then", "Block", "ElseStmt"]),
    ("ElseStmt", ["else", "Block"]),
    ("ElseStmt", ["epsilon"]),
    ("OtherStmt", ["while", "(", "Expr", ")", "Stmt"]),
    ("OtherStmt", ["for", "(", "Expr", ";", "Expr", ";", "Expr", ")", "Stmt"]),
    ("OtherStmt", ["return", "Expr", ";"]),
    ("OtherStmt", ["VarDecl"]),
    ("OtherStmt", ["ExprStmt"]),
    ("OtherStmt", ["Block"]),
    ("ExprStmt", ["id", "=", "Expr", ";"]),
    ("Expr", ["EqualExpr"]),
    ("EqualExpr", ["EqualExpr", "==", "AddExpr"]),
    ("EqualExpr", ["AddExpr"]),
    ("AddExpr", ["AddExpr", "+", "MulExpr"]),
    ("AddExpr", ["MulExpr"]),
    ("MulExpr", ["MulExpr", "*", "UnaryExpr"]),
    ("MulExpr", ["UnaryExpr"]),
    ("UnaryExpr", ["-", "UnaryExpr"]),
    ("UnaryExpr", ["OtherExpr"]),
    ("OtherExpr", ["id", "(", "ArgList", ")"]),
    ("OtherExpr", ["id"]),
    ("OtherExpr", ["num"]),
    ("OtherExpr", ["(", "Expr", ")"]),
    ("ArgList", ["Expr", ",", "ArgList"]),
    ("ArgList", ["Expr"]),
    ("ArgList", ["epsilon"]),
]


def preprocess_read_tokens(data):
    # 합침
    content = ' '.join(data) if isinstance(data, list) else data

    # '==' 을 우선 한 덩어리로
    content = re.sub(r'==', ' == ', content)

    # 실제 문법에서 쓰는 기호들 띄어쓰기
    # '=' 은 단일 등호만 아래 정규식으로 처리
    for ch in ['+', '*', '-', '(', ')', '{', '}', ',', ';']:
        content = content.replace(ch, f' {ch} ')

    # '=' 토큰 분리
    content = re.sub(r'(?<![=])=(?![=])', ' = ', content)

    return [tok for tok in content.split() if tok]



