* Sort contacts in bucket by time last seen (least-recently seen at head, most-recently at tail)
* Split buckets at congruent mod 5 (Something in spec 4.2)
* Spec 4.2 also specifies a bucket considering multiple bits rather than 1, how does this make the routing table larger though?
* Keep a replacement node cache for nodes not being able to be inserted
* Update nodes as they are contacted, evict after being stale and replace with a node from the replacement cache
* Mark node as stale after failing contact five times in a row (five being a variable)
* Add method to find closest node to id
* Implement the lookup algorithm
* Implement maintenance task to update stale buckets