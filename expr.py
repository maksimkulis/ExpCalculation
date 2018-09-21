class Err(Exception):
    pass


class CalcExpresion:
    """
    Example:

    import expr

    string = '(1 + 2/(2 * (1-5)))'
    body = expr.CalcExpresion()
    print(body.ans(string))

    out: 0.75
    """
    def __init__(self):
        self.lexems = []

    def prepearing(self, string):
        self.lexems = []
        tmp = ''
        state = 0

        for i in string:
            if state == 0:
                if i.isspace():
                    continue
                elif i in ('+', '-', '*', '/', '(', ')'):
                    self.lexems.append(i)
                elif i.isdigit():
                    tmp = i
                    state = 1
            elif state == 1:
                if i.isdigit():
                    tmp += i
                elif i in ('+', '-', '*', '/', '(', ')'):
                    self.lexems.append(tmp)
                    self.lexems.append(i)
                    state = 0
                elif i == '.':
                    tmp += i
                    state = 2
                elif i.isspace():
                    self.lexems.append(tmp)
                    state = 0
                else:
                    raise Err
            elif state == 2:
                if i.isdigit():
                    tmp += i
                elif i in ('+', '-', '*', '/', '(', ')'):
                    self.lexems.append(tmp)
                    self.lexems.append(i)
                    state = 0
                elif i == '.':
                    raise Err
                elif i.isspace():
                    self.lexems.append(tmp)
                    state = 0
                else:
                    raise Err
        if state in (1, 2):
            self.lexems.append(tmp)
        self.lexems.append('end')
        return
    def incr(self):
        self.ind += 1
        if self.ind > len(self.lexems):
            raise Err

    def foo1(self):
        ans = self.foo2()
        while self.lexems[self.ind] in ('+', '-'):
            if self.lexems[self.ind] == '+':
                self.incr()
                ans += self.foo2()
            else:
                self.incr()
                ans -= self.foo2()
        return ans

    def foo2(self):
        ans = self.foo3()
        while self.lexems[self.ind] in ('*', '/'):
            if self.lexems[self.ind] == '*':
                self.incr()
                ans *= self.foo3()
            else:
                self.incr()
                tmp = self.foo3()
                if tmp == 0:
                    raise Err('Zero division')
                ans /= tmp
        return ans

    def foo3(self):
        ans = 0
        sign = 1
        if self.lexems[self.ind] in ('+', '-'):
            if self.lexems[self.ind] == '-':
                sign = -1
            self.incr()
        if self.lexems[self.ind] == '(':
            self.incr()
            ans = self.foo1()
            if self.lexems[self.ind] != ')':
                raise Err
        elif self.lexems[self.ind][0].isdigit():
            ans = float(self.lexems[self.ind])
        else:
            raise Err
        self.incr()
        return sign * ans

    def colculation(self, lexems):
        self.ind = 0
        tmp = self.foo1()
        if self.lexems[self.ind] != 'end':
            raise Err
        return tmp

    def ans(self, s):
        self.prepearing(s)
        return self.colculation(self.lexems)
