-- For Character of id = 1
WITH talent_stats AS (
    SELECT 
        tc.talent_category_name,
        tr.talent_id,
        tr.success,
        tr.tap_zfp,
        tr.taw_zfw
    FROM talents_rolls tr
    JOIN talents t ON tr.talent_id = t.talent_id
    JOIN talent_categories tc ON t.talent_category_id = tc.talent_category_id
	INNER JOIN characters as c ON tr.character_id = c.id
	WHERE character_id = 1
)
SELECT 
    talent_category_name,
    COUNT(*) AS roll_count,
    MIN(tap_zfp) AS min_tap_zfp,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY tap_zfp) AS q1_tap_zfp,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY tap_zfp) AS median_tap_zfp,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY tap_zfp) AS q3_tap_zfp,
    MAX(tap_zfp) AS max_tap_zfp,
    MIN(taw_zfw) AS min_taw_zfw,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY taw_zfw) AS q1_taw_zfw,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY taw_zfw) AS median_taw_zfw,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY taw_zfw) AS q3_taw_zfw,
    MAX(taw_zfw) AS max_taw_zfw,
    AVG(success::int) AS success_rate
FROM talent_stats
GROUP BY talent_category_name
ORDER BY talent_category_name;
