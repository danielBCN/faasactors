from faasactors.actor import Actor, Proxy

N_NODES = 5


class Node(object):

    def init_actor(self, aid):
        self.count = 0
        self.my_id = aid

    def take_token(self, token):
        self.count += 1
        if token != 0:
            next_ = Proxy(Actor(f"node{((self.my_id + 1) % N_NODES)}", Node))
            next_.take_token(token-1)
        else:
            print("FINISHED!")


if __name__ == '__main__':
    from faasactors.client import spawn

    nodes = []
    for i in range(N_NODES):
        nodes.append(spawn(f"node{i}", Node, i))

    nodes[0].take_token(50)
