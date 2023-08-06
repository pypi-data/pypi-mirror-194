# Laning Faiss

### Example
```python
import laning_faiss

faiss = laning_faiss.Router("http://faiss-svc:8000")

ntotal = faiss.ntotal()
print(ntotal)
# Output: 16

search_res = faiss.range_search([...], 0.8)
print(search_res)
# Output: [[1, 0.8587932], [2, 0.999999]]
```
