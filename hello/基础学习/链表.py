#!usr/bin/python
# -*- coding:utf-8 -*-

class Node(object):
    def __init__(self, data, pnext=None):
        # 初始化节点
        self.data = data
        self.next = pnext

    def __repr__(self):
        # 打印节点信息
        return str(self.data)


class LinkList(object):
    def __init__(self):
        self.length = 0
        self.head = None

    def isEmpty(self):
        # 判断是否为空
        return self.length == 0

    def append(self, dataOrNode):
        # 尾插
        item = None
        # 判断参数信息
        if isinstance(dataOrNode, Node):
            item = dataOrNode
        else:
            item = Node(dataOrNode)

        if not self.head:
            # 头指针为空
            self.head = item
            self.length += 1
        else:
            # 指向头指针所指地址
            node = self.head
            while node._next:
                node = node._next
            node._next = item
            self.length += 1

    def insert(self, value, index):
        # 插入节点
        if type(index) is int:
            if index > self.length or index < 0:
                print("index is out of index")
                return
            else:
                if index == 0:
                    self.head = Node(value, self.head)
                else:
                    current_node = self.head
                    while index - 1:
                        current_node = current_node.next
                        index -= 1
                    iNode = Node(value, current_node.next)
                    current_node.next = iNode
                self.length += 1
                return
        else:
            print("Index is invaliable")

    def delete(self, index):
        # 删除索引位置结点
        if type(index) is int:
            if index >= self.length or index < 0:
                print("index is out of index")
                return
            else:
                if 0 == index:
                    self.head = self.head.next
                else:
                    node = self.head
                    while index - 1:
                        node = node.next
                        index -= 1
                    node.next = node.next.next
                self.length -= 1
                return
        else:
            print("Index is not int")

    def update(self, value, index):
        # 更新结点
        if type(index) is int:
            if index >= self.length or index < 0:
                print("index is out of index")
                return
            else:
                node = self.head
                while index:
                    node = node.next
                    index -= 1
                node.data = value
                return
        else:
            return

    def get_value(self, index):
        # 获取结点value
        if type(index) is int:
            if index >= self.length or index < 0:
                print("index is out of index")
                return
            else:
                node = self.head
                while index:
                    node = node.next
                    index -= 1
                return node.data
        else:
            return

    def get_length(self):
        # 获取长度
        node = self.head
        length = 0
        while node:
            length += 1
            node = node.next
        print("length is ", length)
        print("self.length is ", self.length)

    def clear(self):
        # 清空链表
        self.head = None
        self.length = 0
        print("Clear!")

    def print_list(self):
        # 打印链表
        if self.isEmpty():
            print("Link is empty")
        else:
            node = self.head
            while node:
                print node.data, "-->",
                node = node.next
            print


def swapPairs(head):
    # 链表交换
    if head != None and head.next != None:
        next = head.next
        head.next = swapPairs(next.next)
        next.next = head
        return next
    return head


if __name__ == "__main__":
    # 测试部分
    linklist = LinkList()
    linklist.append(Node(1))
    linklist.insert(2, 1)
    linklist.insert(3, 2)
    linklist.insert(0, 0)

    print linklist.print_list()
    print linklist.head
    linklist.head = swapPairs(linklist.head)  # 链表交换
    print linklist.print_list()


    # l = LinkList()
    # print(l.isEmpty())
    # ele = Node(2)
    # l.append(ele)
    # print(l.isEmpty())
    # l.insert(0,0)
    # l.insert(1,1)
    # l.insert(3,2)
    # l.print_list()
    # l.get_length()
    # # l.clear()
    # # l.get_length()
    # # l.print_list()
    # # l.head = swapPairs(l.head)
    # # l.print_list()
    # l.delete(2)
    # l.update("000",0)
    # l.update("Asdasda", 2)
    # l.get_length()
    # l.print_list()
    # print(l.get_value(0))
    # print(l.get_value(1))
    # print(l.get_value(2))
