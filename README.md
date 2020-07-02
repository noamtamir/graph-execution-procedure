# Graph Launch Sequence
## Assumptions 
1. A state node can only have 1 state node connected to it directly (no multiple "next" state nodes).
2. A dependency node can only have other dependency nodes connected to it, but not a state node.
3. In the launch sequence the last dependecy should be launched first.
4. If a dependency has already been launched in a current state, it does not need to be launched once again, in this same state.
5. 's' and 'd' nodes are the only legal node types.