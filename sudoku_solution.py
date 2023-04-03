"""solution methods
cell is vertex
relation is neighbour
board is graph
"""
from __future__ import annotations
# TODO: The import may not be used
# from typing import Any, Tuple

import sudoku_setup as su


# TODO: The constant may not be used
# POSITION = Tuple[int, int]


################################################################################
# Graph Sudoku
################################################################################
class SudokuBoard:  # this is similar to class Graph
    """TODO
    """
    def __init__(self):
        self.n = su.INITIATED_NUMBER  # defult 9 by sudoku_setup
        self.cells = set(range(self.n * self.n))  # similar to self.nodes or self.vertex, but this is `set`
        self.relations = {f: set() for f in self.cells}  # similar to self.neighbours

        # Add row connections
        for r in range(self.n):  # row
            for c1 in range(self.n - 1):  # column 1
                for c2 in range(c1 + 1, self.n):  # column 2
                    self.add_edge(r * self.n + c1, r * self.n + c2)

        # Add column connections
        for c in range(self.n):  # column
            for r1 in range(self.n - 1):  # row 1
                for r2 in range(r1 + 1, self.n):  # row 2
                    self.add_edge(r1 * self.n + c, r2 * self.n + c)

        # Add block connections
        b = su.get_base_number(self.n)  # base number
        for block_r in range(3):  # row of block
            for block_c in range(3):  # column of block
                for i in range(self.n - 1):  # specific digit i
                    for j in range(i + 1, self.n):  # specific digit j
                        r1, c1 = divmod(i, b)
                        r2, c2 = divmod(j, b)
                        r1 += b * block_r
                        c1 += b * block_c
                        r2 += b * block_r
                        c2 += b * block_c
                        self.add_edge(r1 * self.n + c1, r2 * self.n + c2)

    def add_edge(self, u: int, v: int) -> None:
        """This is similar to Graph.add_egde. TODO
        """
        self.relations[u].add(v)
        self.relations[v].add(u)


################################################################################
# 回溯
################################################################################
class BacktrackingSolution:
    """..."""

    def solve_sudoku(self, board: list[list[str]]) -> None:
        """...
        """

        def dfs(pos: int):
            """...
            """
            nonlocal valid
            if pos == len(spaces):
                valid = True
                return

            i, j = spaces[pos]
            for digit in range(su.INITIATED_NUMBER):
                if row[i][digit] == column[j][digit] == block[i // su.BASE][j // su.BASE][digit] is False:
                    row[i][digit] = column[j][digit] = block[i // su.BASE][j // su.BASE][digit] = True
                    board[i][j] = str(digit + 1)
                    dfs(pos + 1)
                    row[i][digit] = column[j][digit] = block[i // su.BASE][j // su.BASE][digit] = False
                if valid:
                    return

        row = [[False] * su.INITIATED_NUMBER for _ in range(su.INITIATED_NUMBER)]
        column = [[False] * su.INITIATED_NUMBER for _ in range(su.INITIATED_NUMBER)]
        block = [[[False] * su.INITIATED_NUMBER for _a in range(su.BASE)] for _b in range(su.BASE)]
        valid = False
        spaces = []

        for i in range(su.INITIATED_NUMBER):
            for j in range(su.INITIATED_NUMBER):
                if board[i][j] == ".":
                    spaces.append((i, j))
                else:
                    digit = int(board[i][j]) - 1
                    row[i][digit] = column[j][digit] = block[i // su.BASE][j // su.BASE][digit] = True

        dfs(0)
        print(board)


################################################################################
# 位运算优化
################################################################################
class BitwiseSolution:
    """..."""

    def solve_sudoku(self, board: list[list[str]]) -> None:
        """..."""

        def flip(i: int, j: int, digit: int):
            """...
            """
            row[i] ^= (1 << digit)
            column[j] ^= (1 << digit)
            block[i // su.BASE][j // su.BASE] ^= (1 << digit)

        def dfs(pos: int):
            """...
            """
            nonlocal valid
            if pos == len(spaces):
                valid = True
                return

            i, j = spaces[pos]
            mask = ~(row[i] | column[j] | block[i // su.BASE][j // su.BASE]) & 0x1ff
            while mask:
                digit_mask = mask & (-mask)
                digit = bin(digit_mask).count("0") - 1
                flip(i, j, digit)
                board[i][j] = str(digit + 1)
                dfs(pos + 1)
                flip(i, j, digit)
                mask &= (mask - 1)
                if valid:
                    return

        row = [0] * su.INITIATED_NUMBER
        column = [0] * su.INITIATED_NUMBER
        block = [[0] * su.BASE for _ in range(su.BASE)]
        valid = False
        spaces = list()

        for i in range(su.INITIATED_NUMBER):
            for j in range(su.INITIATED_NUMBER):
                if board[i][j] == ".":
                    spaces.append((i, j))
                else:
                    digit = int(board[i][j]) - 1
                    flip(i, j, digit)

        dfs(0)


################################################################################
# 枚举优化
################################################################################
class EnumerationSolution:
    """..."""

    def solve_sudoku(self, board: list[list[str]]) -> None:
        """...
        """

        def flip(i: int, j: int, digit: int):
            """...
            """
            row[i] ^= (1 << digit)
            column[j] ^= (1 << digit)
            block[i // su.BASE][j // su.BASE] ^= (1 << digit)

        def dfs(pos: int):
            """...
            """
            nonlocal valid
            if pos == len(spaces):
                valid = True
                return

            i, j = spaces[pos]
            mask = ~(row[i] | column[j] | block[i // su.BASE][j // su.BASE]) & 0x1ff
            while mask:
                digit_mask = mask & (-mask)
                digit = bin(digit_mask).count("0") - 1
                flip(i, j, digit)
                board[i][j] = str(digit + 1)
                dfs(pos + 1)
                flip(i, j, digit)
                mask &= (mask - 1)
                if valid:
                    return

        row = [0] * su.INITIATED_NUMBER
        column = [0] * su.INITIATED_NUMBER
        block = [[0] * su.BASE for _ in range(su.BASE)]
        valid = False
        spaces = list()


################################################################################
# 十字交叉双向循环链表
################################################################################
class DLX:
    """
    十字交叉双向循环链表
    """

    def __init__(self, n):
        """
        :param n: 数独的阶数
        """
        self.n = n
        self.m = n ** 2 * n ** 2 * 4 + 1  # 总共的列数(标注节点数+头节点)
        self.max_nums = n ** 2 * n ** 2 * n ** 2 * 4 + self.m  # 最大节点编号

        # 用下标表示节点编号，下标0表示节点0（即头节点），下标1表示节点1，以此类推...
        self.u = [0 for _ in range(self.max_nums)]  # 记录节点的上链接点
        self.d = [0 for _ in range(self.max_nums)]  # 记录节点的下链接点
        self.l = [0 for _ in range(self.max_nums)]  # 记录节点的左链接点
        self.r = [0 for _ in range(self.max_nums)]  # 记录节点的右链接点
        self.row = [0 for _ in range(self.max_nums)]  # 记录节点所在的行
        self.col = [0 for _ in range(self.max_nums)]  # 记录节点所在的列

        # 设置首行的上下左右链接关系
        for i in range(self.m):
            self.u[i] = i
            self.d[i] = i
            self.r[i] = i + 1
            self.l[i] = i - 1
            self.row[i] = 0
            self.col[i] = i
        self.head = 0
        self.l[self.head] = self.m - 1
        self.r[self.m - 1] = self.head

        self.s = [0 for _ in range(self.m)]  # 记录每列节点个数，以便搜索时选择节点数最少的列删除（即优化搜索方向）

        self.next_point = self.m  # 下一个节点编号

        self.ans = [0 for _ in range(n ** 2 * n ** 2 * n ** 2)]  # 所有答案的集合
        self.end = 0

    def add_row(self, row, columns):
        """
        :param row: 新增节点所在的行
        :param columns: 新增节点所在的列
        :return:
        """
        first = self.next_point
        self.l[first] = first
        self.r[first] = first

        for c in columns:
            # 先增加新节点对上下左右节点的指向
            self.u[self.next_point] = self.u[c]
            self.d[self.next_point] = c
            self.l[self.next_point] = self.l[first]
            self.r[self.next_point] = first
            self.row[self.next_point] = row
            self.col[self.next_point] = c

            # 然后修改上下左右节点的指向，即指向新节点
            self.r[self.l[first]] = self.next_point
            self.l[first] = self.next_point
            self.d[self.u[c]] = self.next_point
            self.u[c] = self.next_point

            self.s[c] += 1  # 该列节点数+1

            self.next_point += 1  # 节点编号+1

    def remove(self, c):
        """
        删除第c列
        :param c:
        :return:
        """
        self.l[self.r[c]] = self.l[c]
        self.r[self.l[c]] = self.r[c]

        i = self.d[c]
        while i != c:
            j = self.r[i]
            while j != i:
                self.d[self.u[j]] = self.d[j]
                self.u[self.d[j]] = self.u[j]
                self.s[self.col[j]] -= 1
                j = self.r[j]
            i = self.d[i]

    def restore(self, c):
        """
        恢复第c列
        :param c:
        :return:
        """
        i = self.u[c]
        while i != c:
            j = self.l[i]
            while j != i:
                self.d[self.u[j]] = j
                self.u[self.d[j]] = j
                self.s[self.col[j]] += 1
                j = self.l[j]
            i = self.u[i]
        self.l[self.r[c]] = c
        self.r[self.l[c]] = c

    def dance(self, step):
        """
        :param step: 递归深度
        :return:
        """
        if self.r[self.head] == self.head:
            self.end = step
            return True

        c = self.r[self.head]
        j = self.r[self.head]
        # 选择节点数最少的列
        while j != self.head:
            if self.s[j] < self.s[c]:
                c = j
            j = self.r[j]
        self.remove(c)

        i = self.d[c]
        while i != c:
            # 删除节点i所在的行，并将其保存到结果集中
            self.ans[step] = self.row[i]
            j = self.r[i]
            while j != i:
                self.remove(self.col[j])
                j = self.r[j]
            if self.dance(step + 1):  # 搜索成功则返回
                return True

            # 搜索失败，要恢复，回溯
            self.ans[step] = 0
            j = self.l[i]
            while j != i:
                self.restore(self.col[j])
                j = self.l[j]

            i = self.d[i]
        self.restore(c)
        return False

    def transform_input(self, i, j, num):
        """...
        """
        c1 = self.n ** 2 * (i - 1) + j
        c2 = self.n ** 2 * self.n ** 2 + self.n ** 2 * (i - 1) + num
        c3 = self.n ** 2 * self.n ** 2 * 2 + self.n ** 2 * (j - 1) + num
        c4 = self.n ** 2 * self.n ** 2 * 3 + self.n ** 2 * ((i - 1) // self.n * self.n + (j - 1) // self.n) + num
        return c1, c2, c3, c4

    def run(self, input_str):
        """...
        """
        input_matrix = []
        row_index = 1
        for i in range(1, self.n ** 2 + 1):
            for j in range(1, self.n ** 2 + 1):
                if input_str[i - 1][j - 1] != '.':
                    tmp = int(input_str[i - 1][j - 1])
                    input_matrix.append((i, j, tmp))
                    self.add_row(row_index, self.transform_input(i, j, tmp))
                    row_index += 1
                else:
                    for k in range(1, self.n ** 2 + 1):
                        input_matrix.append((i, j, k))
                        self.add_row(row_index, self.transform_input(i, j, k))
                        row_index += 1

        if self.dance(0):
            for i in self.ans[:self.end]:
                input_str[input_matrix[i - 1][0] - 1][input_matrix[i - 1][1] - 1] = str(input_matrix[i - 1][2])
        else:
            print('Impossible')


class DLXSolution:
    """...
    """

    def solve_sudoku(self, board: list[list[str]]) -> None:
        """...
        """
        dlx = DLX(su.BASE)
        dlx.run(board)


################################################################################
################################################################################
if __name__ == "__main__":
    pass
