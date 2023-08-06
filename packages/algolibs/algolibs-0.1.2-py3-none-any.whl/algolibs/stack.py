
class MinStack(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []
        self.minstack = []

    def push(self, val: int) -> None:
        self.stack.append(val)

        if not self.minstack or val <= self.get_min():
            self.minstack.append(val)

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.getMin():
            self.minstack.pop()

    def top(self) -> int:
        return self.stack[-1]


    def get_min(self) -> int:
        if self.minstack:
            return self.minstack[-1]

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.get_min()
