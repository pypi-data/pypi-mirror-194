

class LinkedNode(object):

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def traversal_linked_list(root):
    lst = []
    while root:
        lst.append(str(root.value))
        root = root.next

    return lst


def traversal_print_linked_list(root, symbol=None):
    lst = []
    while root:
        lst.append(str(root.value))
        root = root.next

    if symbol:
        print(symbol.join(lst))
    else:
        for i in lst:
            print(i)


def remove_nth_from_end(root, n):
    dummy = LinkedNode(value=0, next=root)
    slow = dummy
    fast = dummy

    while n >= 0:
        fast = fast.next
        n -= 1

    while True:
        if not fast:
            if slow.next:
                slow.next = slow.next.next
            break

        slow = slow.next
        fast = fast.next

    return dummy.next


def linked_list_has_cycle(root):
    slow = root
    fast = root
    while True:
        if fast and fast.next:
            break

        fast = fast.next.next
        slow = slow.next
        if slow == fast:
            return True

    return False


def detect_cycle_linked_node(root):
    if not root or not root.next:
        return None

    slow = root
    fast = root

    while True:
        if not fast or not fast.next:
            return None

        slow = slow.next
        fast = fast.next.next

        if fast == slow:
            break

    fast = root
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return fast


def reverse_linked_list(root: ListNode) -> ListNode:
    prev = None
    curr = root

    while curr:
        nextnode = curr.next
        curr.next = prev

        prev = curr
        curr = nextnode

    return prev


def recursion_reverse_linked_list(root: ListNode) -> ListNode:
    if not root or not root.next:
        return root

    newroot = recursion_reverse_linked_list(root.next)
    root.next.next = root
    root.next = None

    return newhead
