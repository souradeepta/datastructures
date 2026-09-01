import pytest

from python.advanced.bst import BST


def test_empty_tree_queries_and_traversals():
    bst = BST()

    assert bst.inorder() == []
    assert bst.preorder() == []
    assert bst.postorder() == []
    assert bst.height() == -1
    assert bst.is_balanced()
    assert not bst.search(10)
    with pytest.raises(ValueError):
        bst.find_min()
    with pytest.raises(ValueError):
        bst.find_max()


def test_insert_search_traversals_and_duplicate_suppression():
    bst = BST()
    for value in (5, 3, 7, 1, 4, 6, 8):
        bst.insert(value)
    bst.insert(3)

    assert bst.inorder() == [1, 3, 4, 5, 6, 7, 8]
    assert bst.preorder() == [5, 3, 1, 4, 7, 6, 8]
    assert bst.postorder() == [1, 4, 3, 6, 8, 7, 5]
    assert bst.find_min() == 1
    assert bst.find_max() == 8
    assert bst.height() == 2
    assert bst.is_balanced()
    assert bst.search(4)
    assert not bst.search(9)


def test_delete_absent_leaf_one_child_and_two_child_nodes():
    bst = BST()
    for value in (5, 3, 7, 1, 4, 6, 8):
        bst.insert(value)

    bst.delete(99)
    assert bst.inorder() == [1, 3, 4, 5, 6, 7, 8]

    bst.delete(1)  # leaf
    assert bst.inorder() == [3, 4, 5, 6, 7, 8]

    one_child = BST()
    for value in (5, 3, 7, 6):
        one_child.insert(value)
    one_child.delete(7)  # one left child
    assert one_child.inorder() == [3, 5, 6]

    two_children = BST()
    for value in (5, 3, 7, 6, 8):
        two_children.insert(value)
    two_children.delete(5)  # root with two children
    assert two_children.inorder() == [3, 6, 7, 8]
    assert two_children.find_min() == 3
    assert two_children.find_max() == 8


def test_sorted_insertion_is_unbalanced():
    bst = BST()
    for value in range(5):
        bst.insert(value)

    assert bst.height() == 4
    assert not bst.is_balanced()
