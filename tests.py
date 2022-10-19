import unittest
from stack import Stack, CustomNode

class CustomNodeTestCases(unittest.TestCase):

    def testSettingText(self):
        node = CustomNode()
        node.text = "Testing Message"
        self.assertEqual(node.text, "Testing Message")

    def testSettingcursorPosition(self):
        # Positions in the form of "{linePosition}.{characterPosition}"

        node = CustomNode()
        node.cursorPosition = "1.5"
        self.assertEqual(node.cursorPosition, "1.5")

class StackTestCases(unittest.TestCase):

    def testStackPointerWhenEmpty(self):
        # Test pointer when stack is empty but still popping. Should remain as -1.

        stack = Stack()
        for x in range(3):
            stack.pop()
        self.assertEqual(stack.pop(), None)

    def testStackPointerRealScenario(self):
        # Test pointer when multiple pops and pushes.

        stack = Stack()
        stack.pop()
        stack.push(1)
        stack.push(2)
        stack.pop()
        stack.push(3)
        stack.push(4)
        stack.push(5)
        stack.pop()
        stack.pop()

        self.assertEqual(stack.pointer, 1)

    def testStackPush(self):
        stack = Stack()
        stack.push(5)
        self.assertEqual(stack.stack[0], 5)

    def testStackPop(self):
        stack = Stack()
        stack.push(4)
        stack.push(3)
        self.assertEqual(stack.pop(), 3)


if __name__ == "__main__":
    unittest.main()