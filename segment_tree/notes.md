# Interface options for a Segment Tree
[x] Range updates 
  [ ] Element updates
[x] Range queries 
  [ ] Element queries
[x] generalise over many query-update pairs
[ ] multiple updators, multipler queries
[ ] lazy construction
  [x] strict
[ ] superlazy updates (updates don't propogate at all until queried)
[x] Commutative (supports dfs traversal for Offline dynamic connectivity)
  [ ] Non-Commutative
[ ] Persistent
[ ] 2-dimensional
[ ] N-dimensional

# Implementation choices for a Segment Tree
- singleton vs null leaves
  [ ] null
  [x] singleton
[x] no push on commutative trees
  [x] query values fully resolved
  [ ] no redundant information (need both qarr[i] and uarr[i] to evaluate segment i)
- query out-of-bounds
  [ ] Monoid query, return mempty
  [x] Semigroup query => Monoid (Maybe query), return Nothing
  [ ] MonadFail, MonadThrow
  [ ] throw an error
  [ ] chop query intervals to match the segments, and error if they go slightly out
[x] construction defined for strict intervals
  [ ] build :: [Int] -> RT -- where RT has an EmptyTree constructor
  [ ] build :: [Int] -> RT a
      - buildNonEmpty :: NonEmpty Int -> RT HasStuff
      - buildEmpty :: RT Empty
  [ ] build :: [Int] -> Maybe RT
  [ ] build :: NonEmpty Int -> RT
[ ] splitting defined for lazy intervals
  [ ] discarding subtrees under idempotent updates (Allows me to not store query value, instead trust lazy queries)
  [ ] support quering homogenous ranges - if a query hits an unbuilt node, it should ask the node above it what the function is and infer what it would be. Requires interval intersection. law: 
  ```hs
  eval intervalA upd + eval intervalB upd = eval (intervalA <> intervalB) upd
  ```
[ ] ability to have a different internal segment representation than (interval, query, update), and the ability to combine them without extracting the query and reconstructing it



# things to test
- initially built tree works correctly and can be queried
- updates are not sent to nodes outside the range
- queries do not include nodes outside the range
- entire updated nodes are evaluated correctly
- A query can punch through an updated segment to a node below and the update is pushed correctly. The update is passed to both children.
- after being punched through, the segment can still be queried correctly
- an update on a segment above a previously update node
- an update on a node above a previously updated node
- parents can be queried and the updates from below are correctly calculated and propogated up
- queries that cross multiple segments are correctly combined
- queries do not change the answer to future queries (don't change the evaluation of segments)

- the update/queries are actually lazy and stop at the largest segments that are contained within it
- updates are pushed by updates and queries (non-Comm)

- make a way to test tree structure at intermediate stages, and add that to the list of query outputs

# misc

- I found out I could merge _update and _query really easily if I don't care about constant factor performance
    - It's even easier if I care very very little about performance and push every time I enter a node
- "lift" can be used to turn semigroups into monoids. But lifting transfer operations is much harder. I can define a "kernel" of the transfer (value*interval for a sum-set tree) then it's lift(snd)(q, lift1(kernal)(u, istart, iend))
- Only Commutative trees deal with the problem of redundant information in a segment, and needing to update both the query and the update values. Since normal trees push frequently, they can just put updates into the update values and let it shift to the query values by the time it's used.
- in multidimenionsal segtrees, I need to update every path from the root to the node being upgraded, so that every affected sub/super/overlapping segment can access the information of the update somewhere.

# Interesting segment trees

- sum_set, sum_mul and sum_add all have different implementation details worth considering.
    - sum_set
        - cannot be commutative (pushless)
    - sum_mul: 
        - query_id is 0 but an array initialised to it can never be updated
    - sum_add:
        - can be commutative, but the update (+) does not distribute over the query (+).
- update = multiply, query = minimum
    - if the multiplication is by a negative number, you need to store the range maximum as well so that you can flip it.
- strict over an array, updates are "set every second tile over given range to 0/1 " and queries are "longest consecutive run of 1s in range"
    - implementation: Each tile is Even or Odd, and the iteration stops at pairs of tiles. 
        - Each segment tracks:
            - Whether all the odd tiles are filled
            - Whether all the even tiles are filled
                - implicitly, whether the whole segment is filled
            - the longest odd chain connected to the left
            - the longest even chain connected to the left
                - implictly the longest chain connected to the left
            - the longest odd chain connected to the right
            - the longest even chain connected to the right
                - implictly the longest chain connected to the right
            - the longest odd chain anywhere inside the segment
            - the longest even chain anywhere inside the segment
            - the longest chain anywhere inside the segment
        - operations are
            - qq:
                - left chain = left left chain <| left segment filled => len(left) + right left chain
                - right chain = right right chain <| right segment filled => len(right) + left right chain
                - anywhere = max(left anywhere, right anywhere, left chain, right chain)
            - uu:
                - set
            - uq:
                - 
    - I could treat it as 2 separate trees (odd, even) that I need to traverse over simultaneously. Segment tree addition?
- range tree where the interval is defined over a lexicographical ordering of strings
- a range tree with query "what is the k'th letter in the string concatenation of this range" and update "add this letter to the end of every string in this range". Idea is to return functions, and compose functions into one mega function. The function would implement a binary-searchable structure
