if __name__ == "__main__":
    import sys
    from pj_tools import PJAction
    username, password = sys.argv[1], sys.argv[2]
    action = PJAction()
    action.do_action(username, password)
