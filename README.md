# Graph Launch Sequence
## Assumptions 
1. A dependency node can only have other dependency nodes connected to it, but not a state node.
2. In the launch sequence the last dependecy should be launched first.
3. If a dependency has already been launched in a current state, it does not need to be launched once again, in this same state.
4. 's' and 'd' nodes are the only legal node types.