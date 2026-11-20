-- Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
-- Purpose: Rank top 10 political parties by total votes and constituency wins (1970-2024)

WITH SeatWinners AS (
    SELECT
        Year,
        Constituency,
        Party,
        Votes,
        RANK() OVER (
            PARTITION BY Year, Constituency
            ORDER BY Votes DESC
        ) AS vote_rank
    FROM elections
)
SELECT
    Party,
    COUNT(*) AS total_candidacies,
    SUM(CASE WHEN vote_rank = 1 THEN 1 ELSE 0 END) AS seats_won,
    ROUND(SUM(Votes), 0) AS total_votes,
    ROUND(AVG(Votes), 1) AS avg_votes_per_candidate
FROM SeatWinners
GROUP BY Party
ORDER BY total_votes DESC
LIMIT 10;