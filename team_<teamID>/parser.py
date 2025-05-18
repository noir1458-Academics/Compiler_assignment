from typing import List, Tuple, Union

# You may define ParseTree and ErrorReport in any way that fits your implementation.
# The below is a placeholder and should be modified.

class ParseTree:
    pass

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
    # TODO: implement your SLR(1) parser using a parsing table and stack
    # This is just a placeholder structure
    return False, ErrorReport(0, "SLR parser not yet implemented")




#개요

# 문법 분석, 모호성 탐지
# 모호성 제거를 위한 문법 재구성
# SLR(1) 파싱 테이블 구축
# 파스 트리 생성 및 오류 보고를 포함한 파서 구현


# 모호성을 제거하고 그 과정을 문서화
# 문법 재구성하고
# 재구성된 문법의 논터미널 대한 first, follow 집합 계산
# slr(1) 파싱 테이블 (action, goto) 구축
# 보고서에는 follow 집합이 shift/reduce, reduce/reduce 충돌 해결하는지 예시 제공

# 파서 구현
#승인시 파스트리 생성, 거부시 토큰 인덱스와 원인 나타내는 상세 오류 보고서 생성

def parser(tokens: List[str]) -> Tuple[bool, Union[ParseTree, ErrorReport]]:
    """
    Returns (True, parse_tree) on success or (False, ErrorReport) on failure.
    Example:
        return True, ParseTree(...)
        return False, ErrorReport(3, "unexpected token 'else'")
    """
    # TODO: implement your SLR(1) parser using a parsing table and stack
    # This is just a placeholder structure
    return False, ErrorReport(0, "SLR parser not yet implemented")



def LexicalAnalyzer(tokens: List[str]) -> List[str]:

    Token_specifications()
    Regular_expression()
    NFA()
    DFA()
    Scanner_code()
    return tokens

def Terminal_symbol_to_RE(Terminal_symbol: str):
    # "epsilon"
    # type
    # id
    # ()
    # {}
    # if
    # else
    # while
    # for
    # ;
    # return
    # =
    # == 
    # + 
    # *
    # -
    # num
    # ,

# 이걸 읽어서 토큰으로 바꾸면 되나??

    return 

def Token_specifications():
    # 토큰 명세 및 정의
    # 토큰 분류 및 용도
    # 토큰 예시
    return

def Regular_expression():
    # 정규 표현식 정의
    # 토큰 분류 및 용도
    # 토큰 예시
    return

def NFA():
    # Thompson's construction
    # 정규 표현식을 NFA로 변환
    # 상태 전이 그래프 표현
    # 시작 상태와 종료 상태
    return

def DFA():
    # subset construction
    # NFA를 DFA로 변환
    # 상태 전이 테이블 표현
    # 시작 상태와 종료 상태
    return

def Scanner_code():
    # 토큰 분석 및 토큰화
    # 토큰화 오류 보고
    # 토큰 반환
    return





def SyntaxAnalyzer(tokens: List[str]) -> Tuple[bool, ParseTree]:
    # 문법 분석 및 파싱 트리 생성
    # 오류 보고
    # 파싱 트리 반환
    return True, ParseTree()


def UsageOfSlrTAble(): # ppt 예제 코드
    ACTION = [[""]]
    GOTO = [[""]]
    a = "first symbol of w"
    while(True):
        s = "state on top of stack"
        if (ACTION[s][a] == "shift t"):
            # push t onto stack
            a = "next input symbol"
        elif (ACTION[s][a] == "reduce A -> beta"):
            # pop abs(beta) symbols from stack
            stateT = "top of stack"
            # push goto(stateT, A) onto stack
            # output the production A -> beta
        elif (ACTION[s][a] == "accept"):
            break # parsing is done
        else:
            # report an error
            return

    return
