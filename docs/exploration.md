# Part C: Systems & Engineering Exploration
**Author:** Qudrat Ullah | **Trainee ID:** TRN-2026-000363

---

## C1. Optimized Query System of a Social Media Feed
- **Why Naive Fan-Out-on-Read Fails at Scale:** Joining `follows` and `posts` at read time (`SELECT * FROM posts WHERE author_id IN (...) ORDER BY created_at DESC LIMIT 20`) scans and sorts millions of rows per page load when a user follows hundreds of accounts.
- **Composite Indexing `(author_id, created_at DESC)`:** Allows SQLite/B-tree engines to jump directly to each followed author's newest posts in index order without a full table scan (`SCAN` becomes `SEARCH USING INDEX`).
- **Fan-Out-on-Write vs. Fan-Out-on-Read:** Precomputing timelines into a Redis cache on write gives $O(1)$ reads for normal users, whereas celebrity accounts (millions of followers) use hybrid fan-out-on-read to avoid write amplification.

### SQLite Index Benchmark Experiment
```sql
CREATE TABLE posts (post_id INTEGER PRIMARY KEY, author_id INTEGER, created_at INTEGER, likes INTEGER);
-- Unindexed query plan: SCAN posts / USE TEMP B-TREE FOR ORDER BY
EXPLAIN QUERY PLAN SELECT post_id FROM posts WHERE author_id IN (12, 45, 89) ORDER BY created_at DESC LIMIT 10;

CREATE INDEX idx_author_time ON posts(author_id, created_at DESC);
-- Indexed query plan: SEARCH posts USING COVERING INDEX idx_author_time (author_id=?)
EXPLAIN QUERY PLAN SELECT post_id FROM posts WHERE author_id IN (12, 45, 89) ORDER BY created_at DESC LIMIT 10;