


# misc

- I found out I could merge _update and _query really easily if I don't care about constant factor performance
    - It's even easier if I care very very little about performance and push every time I enter a node
- "lift" can be used to turn semigroups into monoids. But lifting transfer operations is much harder. I can define a "kernal" of the transfer (value*interval for a sum-set tree) then it's lift(snd)(q, lift1(kernal)(u, istart, iend))

# Interesting segment trees

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