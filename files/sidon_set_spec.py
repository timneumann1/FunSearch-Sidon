"""Finds a maximal set of points with pairwise distinct sums.
On every iteration, improve the priority_v2 function over the priority_v0 and priority_v1 methods from previous iterations.
"""

import itertools

import numpy as np

import funsearch

# @funsearch.run
def evaluate(n: int) -> int:
  """Returns the size of an `n`-dimensional set with pairwise distinct sums."""
  capset = solve(n)
  return len(capset)

def solve(n: int) -> np.ndarray:
  """Returns a large set with pairwise distinct sums in `n` dimensions."""
  all_vectors = np.array(list(itertools.product((0, 1, 2), repeat=n)), dtype=np.int32)

  # Powers in decreasing order for compatibility with `itertools.product`, so
  # that the relationship `i = all_vectors[i] @ powers` holds for all `i`.
  powers = 3 ** np.arange(n - 1, -1, -1)

  # Precompute all priorities.
  priorities = np.array([priority(tuple(vector), n) for vector in all_vectors], dtype = np.float64)
  
  # Build `sidon_set` greedily, using priorities for prioritization.
  sidon_set = np.empty(shape=(0, n), dtype=np.int32)
  while np.any(priorities != -np.inf):
    # Add a vector with maximum priority to `sidon_set`, and set priorities of
    # invalidated vectors to `-inf`, so that they never get selected.
    max_index = np.argmax(priorities)
    vector = all_vectors[None, max_index]  
    blocking = np.einsum('cn,n->c', (- sidon_set - vector) % 3, powers)  
    
    # we block three additional points in order to avoid four points on an affine plane
    for i in range(0,len(sidon_set)-1):
        for j in range(i+1, len(sidon_set)):
            blocking = np.append(blocking, np.inner((-sidon_set[i]+sidon_set[j]+vector)%3,powers))
            blocking = np.append(blocking, np.inner((sidon_set[i]-sidon_set[j]+vector)%3,powers))
            blocking = np.append(blocking, np.inner((sidon_set[i]+sidon_set[j]-vector)%3,powers))
    
    priorities[blocking] = -np.inf
    priorities[max_index] = -np.inf
    sidon_set = np.concatenate([sidon_set, vector], axis=0)

  return sidon_set

# @funsearch.evolve
def priority(el: tuple[int, ...], n: int) -> float:
  """Returns the priority with which we want to add `element` to the set with pairwise distinct sums."""
  return 0.0
